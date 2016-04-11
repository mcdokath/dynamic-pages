import webapp2
import base_page
from google.appengine.ext import ndb

class Message(ndb.Model):
	message = ndb.StringProperty(required=True)

class Profile(ndb.Model):
	username = ndb.StringProperty(required=True)
	firstname = ndb.StringProperty(required=True)
	lastname = ndb.StringProperty(required=True)
	gender = ndb.StringProperty(required=True)
	age = ndb.IntegerProperty(required=True)
	edinterests = ndb.StringProperty(repeated=True)

class Admin(base_page.DynamicPage):
	def __init__(self, request, response):
		self.initialize(request, response)
		self.template_values = {}
		
	def render(self, page):
		self.template_values['username'] = [{'name':x.name,'key':x.key.urlsafe()} for x in admin.Profile.query(ancestor=ndb.Key(admin.Profile, self.app.config.get('default-group'))).fetch()]
		self.template_values['firstname'] = [{'name':x.name,'key':x.key.urlsafe()} for x in admin.Profile.query(ancestor=ndb.Key(admin.Profile, self.app.config.get('default-group'))).fetch()]
		self.template_values['lastname'] = [{'name':x.name,'key':x.key.urlsafe()} for x in admin.Profile.query(ancestor=ndb.Key(admin.Profile, self.app.config.get('default-group'))).fetch()]
		self.template_values['gender'] = [{'name':x.name,'key':x.key.urlsafe()} for x in admin.Profile.query(ancestor=ndb.Key(admin.Profile, self.app.config.get('default-group'))).fetch()]
		self.template_values['age'] = [{'name':x.name,'key':x.key.urlsafe()} for x in admin.Profile.query(ancestor=ndb.Key(admin.Profile, self.app.config.get('default-group'))).fetch()]
		self.template_value['edinterests'] = [{'name':x.name,'key':x.key.urlsafe()} for x in admin.Profile.query(ancestor=ndb.Key(admin.Profile, self.app.config.get('default-group'))).fetch()]
		base_page.DynamicPage.render(self, page, self.template_values)
		
	def get(self):
		self.render('index.html')
	
	def post(self):
		action = self.request.get('action')
		if action == 'add_profile':
			k = ndb.Key(admin.Profile, self.app.config.get('default-group'))
			prof = admin.Profile(parent=k)
			prof.uname = self.request.get('username')
			prof.fname = self.request.get('first-name')
			prof.lname = self.request.get('last-name')
			prof.gender = self.request.get('gender')
			prof.age = self.request.get('age')
			prof.edinterests = [ndb.Key(urlsafe=x) for x in self.request.get_all('ed-interests[]')]
			prof.put()
			self.template_values['message'] = 'Added profile ' + prof.fname + ' ' + prof.lname + ' to the database.'
		else:
			self.template_values['message'] = 'Action ' + action + ' is unknown.'
		self.template_values['username'] = admin.Profile.query(ancestor=ndb.Key(admin.Profile, self.app.config.get('default-group')))
		self.render('index.html')