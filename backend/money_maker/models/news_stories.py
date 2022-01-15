from money_maker.extensions import db
from sqlalchemy import TIMESTAMP, Column, Integer, Text, func


class NewsStories(db.Model):
    __tablename__ = 'news_stories'

    story_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Text)
    short_description = Column(Text)
    url = Column(Text)
    image_url = Column(Text)
    article_updated = Column(Text)
    last_updated = Column(TIMESTAMP, server_default=func.now(), server_onupdate=func.utc_timestamp()) # type: ignore
