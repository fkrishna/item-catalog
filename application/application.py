from flask import *
from utils import *
import models, time
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alchemysetup import Base, Category, Item

app = Flask(__name__)
app.secret_key = '_5#y2L"F4Q8znx/'

ROUTE_PREFIX = '/catalog/'

@app.context_processor
def utility_processor():
	return dict(authenticated = authenticated)

@app.template_filter()
def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
	return value.strftime(format)



##############
# APP ROUTES #
##############

#
# PUBLIC ROOT
# Sign in a new user through a third party provider 
# using OAuth Protocol 
# Route: /login
#
@app.route('/login')
def login():
	if authenticated():
		return redirect(url_for('index'))	

	session['logged'] = True;
	notif = 'You were successfully logged in'		
	flash(notif)
	time.sleep(1)
	return redirect(url_for('index'))


#
# PUBLIC ROOT
# Sign up a new user through a third party provider 
# using OAuth Protocol 
# Route: /logout
#
@app.route('/signup')
def signup():
	if authenticated():
		return redirect(url_for('index'))	

	session.pop('logged', None)
	time.sleep(1)
	return redirect(url_for('index'))


#
# PRIVATE ROOT
# Logout an authenticated user
# Route: /logout
#
@app.route('/logout')
def logout():
	if not authenticated():
		return redirect(url_for('home'))	

	session.pop('logged', None)
	time.sleep(1)
	return redirect(url_for('index'))


#
# PUBLIC ROOT
# Get latest posts
# Route: / OR /home
#
@app.route('/')
@app.route('/home')
def index():
	return render_template('tmpl/catalog.html', title = "latest post")


#
# PRIVATE ROOT
# Add a new item in database
# Route: /catalog/add/
#
@app.route(ROUTE_PREFIX + 'add',  methods = ['POST', 'GET']) 	
def add_item():
	if not authenticated():
		return redirect(url_for('index'))	
	
	if request.method == 'GET':
		vars = {
			"title": "add new item",
			"categories": models.Categories.get_all()
		}
		return render_template('tmpl/item-form.html', vars=vars)

	if request.method == 'POST':
		if not valid_form():
			flash('all fields are required')
			return redirect(url_for('add_item'))

		item = Item(
			name = request.form['item-name'], 
			description = request.form['description'],
			category_id = request.form['category_id'],
			post_date = date.today()
		)

		models.Items.add(item)
		flash('item has been successfully added');
		return redirect(url_for('get_item', item_name=item.name))


#
# PUBLIC ROOT 
# Get all categories from database
# Route: /catalog/categories/
#
@app.route(ROUTE_PREFIX + 'categories/')
def get_categories():
	categories = models.Categories.get_all()
	if categories != None:
		return render_template('tmpl/categories.html', categories=categories)


#
# PUBLIC ROOT
# Get all items from a given category
# Route: /catalog/category/category-name/
#
@app.route(ROUTE_PREFIX + 'category/<string:catego_title>/') 
def get_items(catego_title):
	category = models.Categories.get(catego_title)
	if category != None:
		items = models.Items.get_all(category.id)
		return render_template('tmpl/catalog.html', title=category.title, items=items)
	else:
		abort(404)


#
# PUBLIC ROOT
# Get detail about a specific item
# Route: /catalog/item-name/
#
@app.route(ROUTE_PREFIX + '<string:item_name>')
def get_item(item_name):
	item = models.Items.get(item_name)
	if item != None:
		return render_template('tmpl/item-detail.html', item=item)
	else:
		abort(404)

#
# PRIVATE ROOT
# Edit a specific item
# Route: /catalog/item-name/edit
#
@app.route(ROUTE_PREFIX + '<string:item_name>/edit', methods = ['POST', 'GET'])
def edit_item(item_name):
	if not authenticated():
		return redirect(url_for('index'))

	item = models.Items.get(item_name)

	if item == None:
		abort(404)

	if request.method == 'GET':
		vars = {
			"title": "edit %s" %item_name,
			"item": item,
			"categories": models.Categories.get_all()
		}
		return render_template('tmpl/item-form.html', vars=vars)
		
	if request.method == 'POST':
		if not valid_form():
			flash('all fields are required')
			return redirect(url_for('edit_item', item_name=item.name))

		item.name = request.form['item-name']
		item.description = request.form['description']
		item.category_id = int(request.form['category_id'])
		models.Items.update(item)
		flash('item has been successfully updated');
		return redirect(url_for('get_item', item_name=item.name))


#
# PRIVATE ROOT
# Delete a specific item
# Route: /catalog/item-name/delete
#
@app.route(ROUTE_PREFIX + '<string:item_name>/delete', methods = ['POST', 'GET'])
def delete_item(item_name):
	if not authenticated():
		return redirect(url_for('index'))

	item = models.Items.get(item_name)
	
	if item == None:
		abort(404)

	if request.method == 'GET':
		return render_template('tmpl/item-del.html', item=item)
		
	if request.method == 'POST':
		models.Items.remove(item)
		flash('item has been successfully deleted');
		return redirect(url_for('index'))


#
# PUBLIC ROOT
# Categories JSON Endpoint
# Route: /catalog/item-name/
#
@app.route(ROUTE_PREFIX + 'JSON')
def categories_endpoint():
	categories = models.Categories.get_all()
	items = models.Items.get_all()
	json_categories = [i.serialize for i in categories]
	json_items = [i.serialize for i in items]
	return jsonify(categories=json_categories, items=json_items)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404


def main(): 
	print('server init...')
	app.debug = True
	app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
	main()
