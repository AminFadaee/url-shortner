from urllib.parse import urlparse

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from app.database import db
from urls.abstracts import Encoder
from urls.url import URL


class URLCrud:
    def __init__(self, encoder: Encoder):
        self.encoder = encoder

    def create_url(self, user_id: int, url_str: str, custom_representation: str = None):
        parsed_url = urlparse(url_str)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            raise ValueError('Url is not formatted correctly!')
        if custom_representation is None:
            url = URL(user_id, url_str)
            db.session.add(url)
            db.session.commit()
        else:
            custom_seed = self.encoder.decode(custom_representation)
            try:
                url = self._handle_custom_representation(user_id, url_str, custom_seed)
            except IntegrityError:
                db.session.rollback()
                url = self._handle_conflicting_custom_representation(user_id, url_str, custom_seed)
        representation = self.encoder.encode(url.seed or url.id)
        return url, representation

    def retrieve_url(self, short_representation: str):
        try:
            seed = self.encoder.decode(short_representation)
        except ValueError:
            return None
        url = URL.query.filter(func.coalesce(URL.seed, URL.id) == seed).one_or_none()
        return url

    def _handle_conflicting_custom_representation(self, user_id, url_str, custom_seed):
        while True:
            similar_seeds_min, similar_seeds_max = self.encoder.generate_similar_seeds_range(custom_seed)
            urls = URL.query. \
                filter(func.coalesce(URL.seed, URL.id) <= similar_seeds_max). \
                filter(similar_seeds_min <= func.coalesce(URL.seed, URL.id)). \
                order_by(func.coalesce(URL.seed, URL.id)). \
                all()
            current_seed = similar_seeds_min
            for url in urls:
                seed = url.seed or url.id
                if seed != current_seed:
                    break
                current_seed += 1
            if current_seed <= similar_seeds_max:
                return self._handle_custom_representation(user_id, url_str, current_seed)
            custom_seed = similar_seeds_min

    def _handle_custom_representation(self, user_id, url_str, custom_seed):
        url = URL(user_id, url_str, seed=custom_seed)
        db.session.add(url)
        db.session.commit()
        return url
