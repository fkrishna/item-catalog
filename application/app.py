from flask import *
from utils import *
import models, time, random, string
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alchemysetup import Base, Category, Item
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests

app = Flask(__name__)
app.secret_key = '_5#y2L"F4Q8znx/'

ROUTE_PREFIX = '/catalog/'

@app.context_processor
def utility_processor():
	return dict(authenticated=authenticated)

@app.context_processor
def utility_processor():
	return dict(get_stateToken=get_state_token)

@app.template_filter()
def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
	return value.strftime(format)



CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']
APP_NAME = "Item Catalog"



##############
# APP ROUTES #
##############

#
# PUBLIC ROOT
# Sign in a new user through a google
# using OAuth Protocol 
# Route: /gconnect
#
@app.route('/gconnect', methods=['POST'])
def login():
	# Validate state token
    if request.args.get('state') != session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response


    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = session.get('access_token')
    stored_gplus_id = session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    session['access_token'] = credentials.access_token
    session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    session['picture'] = data['picture']
    session['email'] = data['email']

    notif = 'You were successfully logged in'
    flash(notif)	

    response = make_response(json.dumps("logged successfully"), 200)
    response.headers['Content-Type'] = 'application/json'
    return response


#
# PRIVATE ROOT
# Logout an authenticated user
# Route: /logout
#
@app.route('/logout')
def logout():
 	if not authenticated():
 		flash('current user not connected')
 		return redirect(url_for('index'))

	url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % session.get('access_token')
	h = httplib2.Http()
	result = h.request(url, 'GET')[0]
	
	if result['status'] == '200':
		del session['access_token']
		del session['email']
		del session['picture']
		flash('Successfully disconnected.')
 		return redirect(url_for('index'))
	else:
	    response = make_response(json.dumps('Failed to revoke token for given user.', 400))
	    response.headers['Content-Type'] = 'application/json'
	    return response


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
# Get latest posts
# Route: / OR /home
#
@app.route('/')
@app.route('/home')
def index():
	# Anti Forgery State Token 
	state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
	session['state'] = state

	profile = session.get('picture')
	items = models.Items.get_latest()
	return render_template('tmpl/catalog.html', title="latest post", profile=profile, items=items)


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
# PUBLIC ROOT
# Catalog JSON Endpoint
# Route: /catalog/JSON
#
@app.route(ROUTE_PREFIX + 'JSON')
def catalog_endpoint():
	categories = models.Categories.get_all()
	items = models.Items.get_all()
	json_categories = [i.serialize for i in categories]
	json_items = [i.serialize for i in items]
	return jsonify(categories=json_categories, items=json_items)

#
# PUBLIC ROOT
# Categories JSON Endpoint
# Route: /catalog/categories/JSON
#
@app.route(ROUTE_PREFIX + 'categories/JSON')
def categories_endpoint():
	categories = models.Categories.get_all()
	json_categories = [i.serialize for i in categories]
	return jsonify(categories=json_categories)

#
# PUBLIC ROOT
# Items JSON Endpoint
# Route: /catalog/categories/JSON
#
@app.route(ROUTE_PREFIX + 'items/JSON')
def items_endpoint():
	items = models.Items.get_all()
	json_items = [i.serialize for i in items]
	return jsonify(items=json_items)



@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404


def main(): 
	print('server init...')
	app.debug = True
	app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
	main()
