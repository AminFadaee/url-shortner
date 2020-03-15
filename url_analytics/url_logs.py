from datetime import datetime

from app.database import db


class URLLog(db.Model):
    __tablename__ = 'url_logs'

    id = db.Column(db.BigInteger, primary_key=True, index=True)
    url_id = db.Column(db.BigInteger, db.ForeignKey('urls.id'), nullable=False, index=True)
    timestamp = db.Column(db.DateTime, nullable=False, index=True)
    os = db.Column(db.String(length=30), nullable=True, index=True)
    platform = db.Column(db.String(length=30), nullable=True, index=True)
    browser = db.Column(db.String(length=30), nullable=True, index=True)

    def __init__(self, url_id, os, platform, browser):
        self.url_id = url_id
        self.os = os
        self.platform = platform
        self.browser = browser
        self.timestamp = datetime.utcnow()
