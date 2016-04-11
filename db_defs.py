from google.appengine.ext import ndb

class Message(ndb.Model):
	message = ndb.StringProperty(required=True)

class Profile(ndb.Model):
	email = ndb.StringProperty(required=True)
	firstname = ndb.StringProperty(required=True)
	lastname = ndb.StringProperty(required=True)
	gender = ndb.StringProperty(required=True)
	age = ndb.IntegerProperty(required=True)
	agreement = ndb.BooleanProperty(default=False)

class EdInterests(ndb.Model):
	name = ndb.StringProperty(required=True)
	interests = ndb.StringProperty(repeated=True)