import webapp2
import os
import jinja2
import base_page
from google.appengine.ext import ndb
import db_defs

JINJA_ENVIRONMENT = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + '/templates'),
  extensions=['jinja2.ext.autoescape'],
  autoescape=True
  )
  
class Edit(base_page.DynamicPage):
	def __init__(self, request, response):
		self.initialize(request, response)
		self.template_values = {}

	def get(self):
		if self.request.get('type') == 'profile':
			profile_key = ndb.Key(urlsafe=self.request.get('key'))
			profile = profile_key.get()
			allProfiles = db_defs.Profile.query(ancestor=ndb.Key(db_defs.Profile, self.app.config.get('default-group')))
			profiles_boxes = []
			for element in allProfiles:
				profiles_boxes.append({'email':element.email,'firstname':element.firstname,'lastname':element.lastname,'gender':element.gender,'age':element.age})
				
			self.template_values['profiles'] = profiles_boxes
		self.render('edit.html',self.template_values)
	
	def render(self, page, template_values={}):
		self.template_values['email'] = [{'email':x.email,'key':x.key.urlsafe()} for x in db_defs.Profile.query(ancestor=ndb.Key(db_defs.Profile, self.app.config.get('default-group'))).fetch()]
		self.template_values['firstname'] = [{'firstname':x.firstname,'key':x.key.urlsafe()} for x in db_defs.Profile.query(ancestor=ndb.Key(db_defs.Profile, self.app.config.get('default-group'))).fetch()]
		self.template_values['lastname'] = [{'lastname':x.lastname,'key':x.key.urlsafe()} for x in db_defs.Profile.query(ancestor=ndb.Key(db_defs.Profile, self.app.config.get('default-group'))).fetch()]
		self.template_values['gender'] = [{'gender':x.gender,'key':x.key.urlsafe()} for x in db_defs.Profile.query(ancestor=ndb.Key(db_defs.Profile, self.app.config.get('default-group'))).fetch()]
		self.template_values['age'] = [{'age':x.age,'key':x.key.urlsafe()} for x in db_defs.Profile.query(ancestor=ndb.Key(db_defs.Profile, self.app.config.get('default-group'))).fetch()]

		template = JINJA_ENVIRONMENT.get_template('edit.html')
		self.response.write(template.render(self.template_values))