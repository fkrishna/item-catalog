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
4. Launch terminal to clone the project
```
git clone https://github.com/fkrishna/item-catalog.git
```
```
cd item-catalog
```
5. You will need to register the app as a web-based application through the google dev console and download the client secrets json file. visit this <a href="http://example.com/" target="_blank">link</a>for more information.
6. Put the client secrets json file at the root and run the following commands to boot the vagrant machine
```
vagrant up
```
7. Get access to the shell
```
vagrant ssh 
```
```
cd /vagrant/application 
```
8. Execute the app.py file
```
python app.py
```

