# Item Catalog
Udacity Project for the Full Stack Web Developer Nanodegree Program

# About
A data driven app that presents a list of items in 5 different categories, to Perform any CRUD operation on those items user must authenticate with a gmail account<br>
Categories: Food, Animals, Sports, City, Fashion

# Stack
- Server: Python
- FWK: Flask
- RDBMS: PostgreSQL
- ORM: SQLAlchemy
- Oauth Provider: Google

# Installation
1. Download <a href="https://git-scm.com/downloads" target="_blank">Git</a>, <a href="https://www.virtualbox.org/wiki/Downloads" target="_blank">VirtualBox</a> and <a href="https://www.vagrantup.com/downloads.html" target="_blank">Vagrant</a>
2. Launch terminal and run the following commands
```
git clone https://github.com/fkrishna/item-catalog.git
```
```
cd item-catalog
```
3. You will need to register the app as a web-based application through the google dev console and download the client secrets json file and place it at the root of the directory.<br>

Checkout this <a href="https://developers.google.com/adwords/api/docs/guides/authentication#webapp" target="_blank">link</a> for more information on how to register the app.

# How to use
1. Bring up the vagrant environment then login via ssh
```
1. vagrant up
2. vagrant ssh 
``` 
Then go to the application directory
```
cd /vagrant/application 
```
3. Populate the database
```
python seed.py
```
4. Execute the app.py file
```
python app.py
```
5. Open your browser 
```
http://localhost:5000/
```

If you are getting this error "Missing require parameter: redirect_uri" this <a href="https://github.com/googleapis/oauth2client/issues/16#issuecomment-312719251" target="_blank">link</a> will help you solve this problem with you client secrets json file

# Json Endpoints

|   Endpoints  	| 	 Action 	|
| ------------- | ------------- |
| Content Cell  | Content Cell  |
| Content Cell  | Content Cell  |


