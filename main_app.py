## ----------------------------------------------------------------------------------------------- ##
## ----------------------------------------------------------------------------------------------- ##
import httplib2
import sys, os, requests
import simplejson as json
## ----------------------------------------------------------------------------------------------- ##


## ----------------------------------------------------------------------------------------------- ##
## ---------------------------------- Necessary Flask Modules ------------------------------------ ##
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, make_response
## ----------------------------------------------------------------------------------------------- ##


## ----------------------------------------------------------------------------------------------- ##
## -------------------- Importing modules for database and Github OAuth -------------------------- ##
from flask_dance.contrib.github import make_github_blueprint, github
from flask_sqlalchemy import SQLAlchemy 
from flask_login import UserMixin, current_user, LoginManager, login_required, login_user, logout_user
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin, SQLAlchemyBackend
from flask_dance.consumer import oauth_authorized
from sqlalchemy.orm.exc import NoResultFound
## ----------------------------------------------------------------------------------------------- ##


## ----------------------------------------------------------------------------------------------- ##
## ----- Organisation to get github project from and github ids allowed for creating a blog ------ ##
organisation = 'Marauders-9998'
allowed_users_ids = []
## ----------------------------------------------------------------------------------------------- ##


## ----------------------------------------------------------------------------------------------- ##
## --------------- Initialising the flask object and registering github blueprint ---------------- ##
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login_data.db'

github_blueprint = make_github_blueprint(client_id = '6fbf106b39b23aeeba15',
										client_secret = 'c9b6b6fd35c11df5b240af0cac4e15619a5b3b83')
app.register_blueprint(github_blueprint, url_prefix = '/github_login')
## ----------------------------------------------------------------------------------------------- ##


## ----------------------------------------------------------------------------------------------- ##
## -------------------------------------- Database setup ----------------------------------------- ##
db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True)

class OAuth(OAuthConsumerMixin, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)

github_blueprint.backend = SQLAlchemyBackend(OAuth, db.session, user=current_user)
## ----------------------------------------------------------------------------------------------- ##


## ----------------------------------------------------------------------------------------------- ##
## --------------------------------- Setting up login manager ------------------------------------ ##
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
## ----------------------------------------------------------------------------------------------- ##


def render_page(html_page, **kwargs):
	return render_template(html_page, org = organisation, **kwargs)

@app.route('/')
@app.route('/home/')
def showFrontPage():
	print("Hello World, from Maruaders")
	return render_page('front_page.html')

@app.route('/projects/')
def showProjectsPage():
	marauders_api = 'https://api.github.com/orgs/{org}/repos'.format(org = organisation)
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
	marauders_api_response = requests.get(marauders_api, headers = headers)
	#print('---> marauders_api_response:', marauders_api_response)
	repos = []
	if marauders_api_response.status_code == 200:
		repositories = marauders_api_response.json()
		#print('---> repositories:', repositories)
		for repository in repositories:
			repo = {}
			repo['id'] = repository['id']
			repo['name'] = repository['name']
			repo['url'] = repository['html_url']
			repo['issues'] = repository['open_issues_count']
			repo['forks'] = repository['forks_count']
			repo['desc'] = repository['description']
			repo['lang'] = repository['language']
			repo['issues_api_url'] = repository['issues_url'].split('{')[0]
			repo['commits_api_url'] = repository['commits_url'].split('{')[0] 
			repos.append(repo)
	else:
		response = make_response(json.dumps('Could not request Github'), marauders_api_response.status_code)
		response.headers['Content-Type'] = 'application/json'
		return response

	print(repos)

	return render_page('projects_page.html', repositories = repos[::-1])

@app.route('/blogs/')
def showBlogPage():
	return render_page('blog_page.html')

@app.route('/forum/')
def showForumPage():
	return render_page('forum_page.html')

@app.route('/new_blog/')
def showNewBlogPage():
	return redirect(url_for('github_login'))


## ----------------------------------------------------------------------------------------------- ##
## ----------------------------------------------------------------------------------------------- ##
@oauth_authorized.connect_via(github_blueprint) ##Signal sent on log in
def github_logged_in(blueprint, token):

    account_info = blueprint.session.get('/user')

    if account_info.ok:
        account_info_json = account_info.json()
        username = account_info_json['login']

        query = User.query.filter_by(username = username)

        try:
            user = query.one()
        except NoResultFound:
            user = User(username = username)
            db.session.add(user)
            db.session.commit()

        login_user(user)

@app.route('/github/')
def github_login():
	if not github.authorized:
		return redirect(url_for("github.login"))
	else:
		account_info = github.get('/user')
		if account_info.ok:
			account_data = account_info.json()
			return '<h1>Your Github name is {}'.format(account_info_json['login'])
		else:
			return "Request Failed"


@app.route('/github_logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
## ----------------------------------------------------------------------------------------------- ##


if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' ##Remove this line <--------------------------------------
	app.run(host = '0.0.0.0', port = 5000)