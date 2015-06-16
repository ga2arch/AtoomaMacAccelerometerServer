from google.appengine.ext import ndb

class User(ndb.Model):
    google_id    = ndb.StringProperty()
    gcm_token    = ndb.StringProperty()
    status       = ndb.IntegerProperty()