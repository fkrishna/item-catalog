from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alchemysetup import Base, Category, Item, User
from sqlalchemy.exc import * 

engine = create_engine('postgresql+psycopg2://vagrant:root@/catalog')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Categories Model
class Categories():

	results = None

	@staticmethod
	def get_all():
		Categories.results = None
		try:
			Categories.results = session.query(Category).all()
		except SQLAlchemyError as e:
			print(e)

		return Categories.results

	@staticmethod
	def get(category_title):
		Categories.results = None
		try:
			Categories.results = session.query(Category).filter(Category.title == category_title).one()
		except SQLAlchemyError as e:
			print(e)

		return Categories.results


# Categories Model
class Users():

	results = None

	@staticmethod
	def get(user_id):
		Users.results = None
		try:
			Users.results = session.query(User).filter(User.id == user_id).one()
		except SQLAlchemyError as e:
			print(e)

		return Users.results

	@staticmethod
	def get_by_email(user_mail):
		Users.results = None
		try:
			Users.results = session.query(User).filter(User.email == user_mail).one()
		except SQLAlchemyError as e:
			print(e)

		return Users.results

	@staticmethod
	def occur(email):
		exist = False
		try:
			res = session.query(User).filter(User.email == email).count()
			exist = True if res == 1 else False
		except SQLAlchemyError as e:
			print(e)

		return exist

	@staticmethod
	def add(user):
		Users.results = None
		try:
			Users.results = session.add(user)
			session.commit()
		except SQLAlchemyError as e:
			print(e)

		return Users.results


# Items Model
class Items():

	results = None

	@staticmethod
	def get_latest():
		Items.results = None
		try:
			Items.results = session.query(Item).order_by(Item.id.desc()).limit(4).all()
		except SQLAlchemyError as e:
			print(e)

		return Items.results

	@staticmethod
	def get_all(category_id = None):
		Items.results = None
		try:
			if category_id != None:
				Items.results = session.query(Item).filter(Item.category_id == category_id).all()	
			else:
				Items.results = session.query(Item).all()
		except SQLAlchemyError as e:
			print(e)

		return Items.results

	@staticmethod
	def get(name):
		Items.results = None
		try:
			Items.results = session.query(Item).filter(Item.name == name).one()
		except SQLAlchemyError as e:
			print(e)

		return Items.results

	@staticmethod
	def add(item):
		Items.results = None
		try:
			Items.results = session.add(item)
			session.commit()
		except SQLAlchemyError as e:
			print(e)

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
		except SQLAlchemyError as e:
			print(e)

		return Items.results		

