import json

from google.appengine.api import urlfetch

server_client_id = '616915116273-7vd2buav2tuc5koh72uvpmtoeuhn0l7a.apps.googleusercontent.com'
ext_client_id = '957149093304-n01v9lk1s8tti1q5tgjres277142hn1e.apps.googleusercontent.com'
api_key = 'AIzaSyCVS7M926mJ74sRRBAxwhrph42r9a9LL2E'

def validate_id_token(token):
    url = 'https://www.googleapis.com/oauth2/v3/tokeninfo'
    url += '?id_token=' + token
    
    resp = urlfetch.fetch(url)

    if (resp.status_code == 200):
        j = json.loads(resp.content)

        if j['aud'] == server_client_id:
            google_id = j['sub']
            return google_id
        else:
            return None
    else:
        return None

def validate_access_token(token):
    url = 'https://www.googleapis.com/oauth2/v3/tokeninfo'
    url += '?access_token=' + token
        
    resp = urlfetch.fetch(url)

    if (resp.status_code == 200):
        j = json.loads(resp.content)

        if j['aud'] == ext_client_id:
            google_id = j['sub']
            return google_id
    else:
        return None    