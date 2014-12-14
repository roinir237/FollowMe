from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
import urllib

class Tweet(declarative_base()):
    __tablename__ = 'tweets'

    id = Column('id', Integer, primary_key=True)
    title = Column('title', Text, nullable=False)
    url = Column('url', String(100))
    likes = Column('likes', Integer)
    posted = Column('posted', DateTime)

    def fromdict(self, values):
        for c in self.__table__.columns:
            if c.name in values:
                setattr(self, c.name, values[c.name])
        return self

    def post_to_twitter(self,api):
        urllib.urlretrieve(self.url, "temp.jpg")
        api.PostMedia(self.title[:140], "temp.jpg")

    def __repr__(self):
        return "<tweet(id='%s', title='%s', url='%s', likes='%s', posted='%s')>" % (
                self.id, self.title, self.url, self.likes, self.posted)