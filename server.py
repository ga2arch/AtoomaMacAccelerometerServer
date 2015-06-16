import webapp2, cgi

from models.users import User
from utils.validate import *

class Tokens(webapp2.RequestHandler):
    def post(self):
        id_token = cgi.escape(self.request.get('id_token'))
        gcm_token = cgi.escape(self.request.get('gcm_token'))

        google_id = validate_id_token(id_token)

        if google_id:
            user = User.query(User.google_id == google_id).get()
            if user:
                user.gcm_token = gcm_token
                user.put()
            else:
                user = User(google_id=google_id, gcm_token=gcm_token, status=-1)
                user.put()

            self.response.status = 200
        else:
            self.response.status = 400
            self.response.write(json.dumps(dict(error='invalid token')))

class Tilted(webapp2.RequestHandler):
    def post(self):
        access_token = cgi.escape(self.request.get('access_token'))
      
        google_id = validate_access_token(access_token)
        
        if google_id:
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
                self.response.status = 400
                self.response.write(json.dumps(dict(error='no user')))
        else:
            self.response.status = 400
            self.response.write(json.dumps(dict(error='invalid token')))

app = webapp2.WSGIApplication([
    ('/tokens', Tokens),
    ('/tilted', Tilted)
], debug=True)