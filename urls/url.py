from app import db


class URL(db.Model):
    __tablename__ = 'urls'

    id = db.Column(db.BigInteger, primary_key=True, index=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    url = db.Column(db.String(length=500))
    seed = db.Column(db.BigInteger, nullable=True, unique=True, index=True)

    def __init__(self, user_id: int, url: str, seed=None):
        self.user_id = user_id
        self.url = url
        self.seed = seed
