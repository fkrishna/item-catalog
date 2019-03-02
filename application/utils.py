from flask import session, request

def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
    return value.strftime(format)


def authenticated():
	return True if session.get('access_token') else False
	


def valid_form():
	valid = True;

	if not request.form['item-name'] or not request.form['description']:
		valid = False

	try:
		int(request.form['category_id'])
	except Exception as e:
		valid = False
	
	return valid

