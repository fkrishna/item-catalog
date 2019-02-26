from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alchemysetup import Base, Category, Item
from sqlalchemy.exc import * 

engine = create_engine('postgresql+psycopg2://vagrant:root@/catalog')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class Categories():

	"""docstring for ClassName"""

	results = None

	@staticmethod
	def get_all():
		Categories.results = None
		try:
			Categories.results = session.query(Category).all()
		except SQLAlchemyError:
			pass

		return Categories.results

	@staticmethod
	def get(category_title):
		Categories.results = None
		try:
			Categories.results = session.query(Category).filter(Category.title == category_title).one()
		except SQLAlchemyError:
			pass

		return Categories.results


class Items():

	"""docstring for ClassName"""

	results = None

	@staticmethod
	def get_all(category_id = None):
		Items.results = None
		try:
			if category_id != None:
				Items.results = session.query(Item).filter(Item.category_id == category_id).all()	
			else:
				Items.results = session.query(Item).all()
		except SQLAlchemyError:
			pass

		return Items.results

	@staticmethod
	def get(name):
		Items.results = None
		try:
			Items.results = session.query(Item).filter(Item.name == name).one()
		except SQLAlchemyError:
			pass

		return Items.results

	@staticmethod
	def add(item):
		Items.results = None
		try:
			Items.results = session.add(item)
			session.commit()
		except SQLAlchemyError:
			pass

		return Items.results

	@staticmethod
	def update(item):
		return Items.add(item)

	@staticmethod
	def remove(item):
		Items.results = None
		try:
			Items.results = session.delete(item)
			session.commit()
		except SQLAlchemyError:
			pass

		return Items.results		

