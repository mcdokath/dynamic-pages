import webapp2
import os
import jinja2
from google.appengine.ext import ndb
import db_defs

JINJA_ENVIRONMENT = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + '/templates'),
  extensions=['jinja2.ext.autoescape'],
  autoescape=True
  )

class DynamicPage(webapp2.RequestHandler):
	template_variables = {}
	
	def __init__(self, request, response):
		self.initialize(request, response)
		self.template_values = {}
		
	def get(self):
		self.template_variables['profile_contents'] = {}
		template = JINJA_ENVIRONMENT.get_template('index.html')
		for i in self.request.arguments():
			self.template_variables['profile_contents'][i] = self.request.get(i)
		self.render('index.html', self.template_variables)
	
	def post(self):
		self.template_variables['profile_contents'] = {}
		template = JINJA_ENVIRONMENT.get_template('index.html')
		for i in self.request.arguments():
			self.template_variables['profile_contents'][i] = self.request.get(i)
			
		action = self.request.get('action')
		if action == 'add_profile':
			k = ndb.Key(db_defs.Profile, self.app.config.get('default-group'))
			prof = db_defs.Profile(parent=k)
			prof.email = self.request.get('email')
			prof.firstname = self.request.get('first-name')
			prof.lastname = self.request.get('last-name')
			prof.gender = self.request.get('gender')
			prof.age = int(self.request.get('age'))
			if self.request.get('agreement') == u'on':
				prof.agreement = True
			prof.edinterests = [ndb.Key(urlsafe=x) for x in self.request.get_all('edinterests[]')]
			prof.put()
			self.template_values['message'] = 'Added profile ' + prof.email + ' to the database.'
		elif action == 'add_interest':
			k = ndb.Key(db_defs.EdInterests, self.app.config.get('default-group'))
			ai = db_defs.EdInterests(parent=k)
			ai.name = self.request.get('interest-name')
			ai.put()
			self.template_values['message'] = 'Added interest ' + ai.name + ' to the database.'
		else:
			self.template_values['message'] = 'Action ' + action + ' is unknown.'
		self.template_values['email'] = db_defs.Profile.query(ancestor=ndb.Key(db_defs.Profile, self.app.config.get('default-group')))
		self.render('index.html', self.template_variables)
		
	def render(self, page, template_values={}):
		self.template_values['email'] = [{'email':x.email,'key':x.key.urlsafe()} for x in db_defs.Profile.query(ancestor=ndb.Key(db_defs.Profile, self.app.config.get('default-group'))).fetch()]
		self.template_values['firstname'] = [{'firstname':x.firstname,'key':x.key.urlsafe()} for x in db_defs.Profile.query(ancestor=ndb.Key(db_defs.Profile, self.app.config.get('default-group'))).fetch()]
		self.template_values['lastname'] = [{'lastname':x.lastname,'key':x.key.urlsafe()} for x in db_defs.Profile.query(ancestor=ndb.Key(db_defs.Profile, self.app.config.get('default-group'))).fetch()]
		self.template_values['gender'] = [{'gender':x.gender,'key':x.key.urlsafe()} for x in db_defs.Profile.query(ancestor=ndb.Key(db_defs.Profile, self.app.config.get('default-group'))).fetch()]
		self.template_values['age'] = [{'age':x.age,'key':x.key.urlsafe()} for x in db_defs.Profile.query(ancestor=ndb.Key(db_defs.Profile, self.app.config.get('default-group'))).fetch()]
		self.template_values['edinterests'] = [{'name':x.name,'key':x.key.urlsafe()} for x in db_defs.EdInterests.query(ancestor=ndb.Key(db_defs.EdInterests, self.app.config.get('default-group'))).fetch()]

		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(self.template_values))
		
class View(webapp2.RequestHandler):
	template_variables = {}
	
	def __init__(self, request, response):
		self.initialize(request, response)
		self.template_values = {}
		
	def get(self):
		self.template_variables['profile_contents'] = {}
		template = JINJA_ENVIRONMENT.get_template('view.html')
		for i in self.request.arguments():
			self.template_variables['profile_contents'][i] = self.request.get(i)
		self.render('view.html', self.template_variables)
	
	def post(self):
		self.template_variables['profile_contents'] = {}
		template = JINJA_ENVIRONMENT.get_template('view.html')
		for i in self.request.arguments():
			self.template_variables['profile_contents'][i] = self.request.get(i)
		self.render('view.html', self.template_variables)
		
	def render(self, page, template_values={}):
		self.template_values['email'] = [{'email':x.email,'key':x.key.urlsafe()} for x in db_defs.Profile.query(ancestor=ndb.Key(db_defs.Profile, self.app.config.get('default-group'))).fetch()]
		self.template_values['firstname'] = [{'firstname':x.firstname,'key':x.key.urlsafe()} for x in db_defs.Profile.query(ancestor=ndb.Key(db_defs.Profile, self.app.config.get('default-group'))).fetch()]
		self.template_values['lastname'] = [{'lastname':x.lastname,'key':x.key.urlsafe()} for x in db_defs.Profile.query(ancestor=ndb.Key(db_defs.Profile, self.app.config.get('default-group'))).fetch()]
		self.template_values['gender'] = [{'gender':x.gender,'key':x.key.urlsafe()} for x in db_defs.Profile.query(ancestor=ndb.Key(db_defs.Profile, self.app.config.get('default-group'))).fetch()]
		self.template_values['age'] = [{'age':x.age,'key':x.key.urlsafe()} for x in db_defs.Profile.query(ancestor=ndb.Key(db_defs.Profile, self.app.config.get('default-group'))).fetch()]
		self.template_values['edinterests'] = [{'name':x.name,'key':x.key.urlsafe()} for x in db_defs.EdInterests.query(ancestor=ndb.Key(db_defs.EdInterests, self.app.config.get('default-group'))).fetch()]

		template = JINJA_ENVIRONMENT.get_template('view.html')
		self.response.write(template.render(self.template_values))