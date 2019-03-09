from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Category(Base):

    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title
        }


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(255), nullable=False)
    email = Column(String, nullable=False)


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(String, nullable=False)
    post_date = Column(DateTime, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'date': self.post_date,
            'cid': self.category_id,
        }


engine = create_engine("postgresql+psycopg2://vagrant:root@/catalog")

Base.metadata.create_all(engine)
