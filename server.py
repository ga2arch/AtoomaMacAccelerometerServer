import webapp2, json, cgi

from google.appengine.api import urlfetch
from google.appengine.ext import ndb

api_key = 'AIzaSyCVS7M926mJ74sRRBAxwhrph42r9a9LL2E'

class User(ndb.Model):
    google_id    = ndb.StringProperty()
    gcm_token    = ndb.StringProperty()
    status       = ndb.IntegerProperty()

class Tokens(webapp2.RequestHandler):
    def post(self):
        id_token = cgi.escape(self.request.get('id_token'))
        gcm_token = cgi.escape(self.request.get('gcm_token'))

        url = "https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=" + id_token
        google_id = json.loads(urlfetch.fetch(url).content)['sub']

        user = User.query(User.google_id == google_id).get()
        if user:
            user.gcm_token = gcm_token
            user.put()
        else:
            user = User(google_id=google_id, gcm_token=gcm_token, status=-1)
            user.put()

class Tilted(webapp2.RequestHandler):
    def post(self):
        access_token = cgi.escape(self.request.get('access_token'))
        
        url = "https://www.googleapis.com/oauth2/v3/tokeninfo?access_token=" + access_token
        google_id = json.loads(urlfetch.fetch(url).content)['sub']
        
        user = User.query(User.google_id == google_id).get()
        
        if user:
            gcm_url = 'https://gcm-http.googleapis.com/gcm/send'
            headers = { 'Authorization':'key='+api_key, 'Content-Type':'application/json'}
            data = { 'data': {'status': 1 }, 'to': user.gcm_token }

            r = urlfetch.fetch(url=gcm_url,
                    payload=json.dumps(data),
                    method=urlfetch.POST,
                    headers=headers)
            print r.content
        else:
            print "No User"
            self.response.write('No user')

app = webapp2.WSGIApplication([
    ('/tokens', Tokens),
    ('/tilted', Tilted)
], debug=True)