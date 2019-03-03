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
1. Download <a href="https://git-scm.com/downloads" target="_blank">Git</a>
2. Download <a href="https://www.virtualbox.org/wiki/Downloads" target="_blank">VirtualBox</a>
3. Download <a href="https://www.vagrantup.com/downloads.html" target="_blank">Vagrant</a>
4. Launch terminal and run the following commands
```
git clone https://github.com/fkrishna/item-catalog.git
```
```
cd item-catalog
```
5. You will need to register the app as a web-based application through the google dev console and download the client secrets json file and place it at the root of the directory.<br>
checkout this <a href="https://developers.google.com/adwords/api/docs/guides/authentication#webapp" target="_blank">link</a> for more information on how to register the app.

# How to use
1. Bring up the vagrant environment
```
vagrant up
```
2. Get access to the shell
```
vagrant ssh 
```
```
cd /vagrant/application 
```
3. Execute the app.py file
```
python app.py
```
# Json Endpoints
* /catalog
* /catalog/categories
* /catalog/items