import webapp2
import base_page
from google.appengine.ext import ndb
import db_defs

class Edit(base_page.DynamicPage):
	def __init__(self, request, response):
		self.initialize(request, response)
		self.template_values = {}

	def get(self):
		if self.request.get('type') == 'profile':
			profile_key = ndb.Key(urlsafe=self.request.get('key'))
			profile = profile_key.get()
			allProfiles = db_defs.Profile.query(ancestor=ndb.Key(db_defs.Profile, self.app.config.get('default-group)))
			profiles_boxes = []
			for element in allProfiles:
				profiles_boxes.append({'email':element.email,'firstname':element.firstname,'lastname':element.lastname,'gender':element.gender,'age':element.age})
				
			self.template_values['profiles'] = profiles_boxes
		self.render('edit.html',self.template_values)