3# . Implement OAuth2 authentication to allow users to log in using their Google or Facebook accounts.


from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# OAuth configuration
oauth = OAuth(app)

# Google configuration
google = oauth.register(
    name='google',
    client_id='YOUR_GOOGLE_CLIENT_ID',
    client_secret='YOUR_GOOGLE_CLIENT_SECRET',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://www.googleapis.com/oauth2/v1/userinfo',
    client_kwargs={'scope': 'openid profile email'}
)

# Facebook configuration
facebook = oauth.register(
    name='facebook',
    client_id='YOUR_FACEBOOK_APP_ID',
    client_secret='YOUR_FACEBOOK_APP_SECRET',
    access_token_url='https://graph.facebook.com/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    authorize_params=None,
    api_base_url='https://graph.facebook.com/',
    userinfo_endpoint='https://graph.facebook.com/me?fields=id,name,email,picture{url}',
    client_kwargs={'scope': 'email'}
)

@app.route('/')
def index():
    return 'Welcome to the OAuth2 Authentication Example'

@app.route('/login/<provider>')
def login(provider):
    provider = oauth.create_client(provider)
    redirect_uri = url_for('authorize', provider=provider.name, _external=True)
    return provider.authorize_redirect(redirect_uri)

@app.route('/authorize/<provider>')
def authorize(provider):
    provider = oauth.create_client(provider)
    token = provider.authorize_access_token()
    user_info = provider.userinfo()
    session['user'] = user_info
    return f'Logged in as {user_info["name"]}'

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5003)