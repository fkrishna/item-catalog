from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alchemysetup import Base, Category, Item
from datetime import date
from mock import catalog
import lipsum

engine = create_engine('postgresql+psycopg2://vagrant:root@/catalog')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# populate categories and items tables
def execute():
	
	items = []

	print('populating the categories table...')
	for category in catalog.keys():
		session.add( Category(title = category) )
		session.commit()

	print('populating the items table...')
	for i, category in enumerate(catalog.keys()):
		for c_item in catalog[category]:
			items.append( 
				Item(
					name = c_item,
					description = lipsum.generate_paragraphs(), 
					post_date = date.today(),
					category_id = session.query(Category).filter(Category.title == category).first().id
				)
			)
	session.add_all(items)
	session.commit()
	print('Done...')


if __name__ == '__main__':
	execute()
	

	
