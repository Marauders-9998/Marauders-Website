## ----------------------------------------------------------------------------------------------- ##
## ----------------------------------------------------------------------------------------------- ##
import httplib2
import sys, os, requests
import simplejson as json
from pprint import pprint
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
allowed_users_ids = [27439964, 31085591]
## ----------------------------------------------------------------------------------------------- ##


## ----------------------------------------------------------------------------------------------- ##
## --------------- Initialising the flask object and registering github blueprint ---------------- ##
app = Flask(__name__)
os.environ['MARAUDERS_LOGIN_DATA'] = 'sqlite:///login_data.db' ##in_production
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('MARAUDERS_LOGIN_DATA')

os.environ['MARAUDERS_GITHUB_SECRET'] = '3a16737a98ac1449ce2fb1db8816b4a61b1566a5' ##in_production
client_id = '6fbf106b39b23aeeba15' ##in_production
#client_id = 'GITHUB_APP_CLIENT_ID'
client_secret = os.environ.get('MARAUDERS_GITHUB_SECRET')
github_blueprint = make_github_blueprint(client_id = client_id,
										client_secret = client_secret)
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

github_blueprint.backend = SQLAlchemyBackend(OAuth, db.session, user=current_user, user_required = False) ##in_production
#github_blueprint.backend = SQLAlchemyBackend(OAuth, db.session, user=current_user)
## ----------------------------------------------------------------------------------------------- ##


## ----------------------------------------------------------------------------------------------- ##
## --------------------------------- Setting up login manager ------------------------------------ ##
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
## ----------------------------------------------------------------------------------------------- ##


def render_page(html_page, **kwargs):
	if loggedIn():
		account_info = accountInfo(github)
		if account_info is not None:
			orgs_info = orgsAccountInfo(github, github_user = account_info['login'])
			user_image = account_info['avatar_url']
			user_url = account_info['html_url']
			kwargs['usr_img'] = user_image
			kwargs['usr_url'] = user_url
			kwargs['userLogged'] = True
			kwargs['orgs_info'] = orgs_info
			kwargs['maraudersLogged'] = maraudersLoggedIn()
		else:
			return "Request Failed"
	else:
		kwargs['userLogged'] = False

	return render_template(html_page, org = organisation, **kwargs)


@app.route('/')
def showFrontPage():
	print("Hello World, from Maruaders")
	return render_page('front_page.html')
	

@app.route('/projects/')
def showProjectsPage():
	with open('colors.json') as f:
		lang_info = json.load(f)
	repos = []
	repositories = orgReposInfo(github)
	if repositories:
		for repository in repositories:
			repo = {}
			repo['id'] = repository['id']
			repo['name'] = repository['name']
			repo['url'] = repository['html_url']
			repo['issues'] = repository['open_issues_count']
			repo['forks'] = repository['forks_count']
			repo['desc'] = repository['description']
			repo['lang'] = repository['language']
			try:
				repo['lang_color'] = lang_info[repo['lang']]['color']
			except:
				repo['lang_color'] = None
			repo['issues_api_url'] = repository['issues_url'].split('{')[0]
			repo['commits_api_url'] = repository['commits_url'].split('{')[0] 
			repos.append(repo)
	else:
		response = make_response(json.dumps('Could not request Github'), 503)
		response.headers['Content-Type'] = 'application/json'
		return response

	#pprint(repos)

	return render_page('projects_page.html', repositories = repos[::-1])


@app.route('/blogs/')
def showBlogPage():
	return render_page('blog_page.html')


@app.route('/forum/')
@login_required
def showForumPage():
	return render_page('forum_page.html')


@app.route('/new_blog/', methods = ['GET', 'POST'])
@login_required
def showNewBlogPage():
	if maraudersLoggedIn():
		return render_page('new_blog_page.html')
	else:
		response = make_response(render_page("Unauthorized.html"), 401)
		response.headers['Content-Type'] = 'text/html'
		return response


## ----------------------------------------------------------------------------------------------- ##
## ----------------------------------------------------------------------------------------------- ##
def loggedIn():
	if not github.authorized:
		return False
	else:
		return True

def maraudersLoggedIn():
	if loggedIn():
		account_info = accountInfo(github)
		if account_info is not None:
			if account_info['id'] in allowed_users_ids:
				return True
			else:
				return False
		else:
			return False
	else:
		return False


def accountInfo(blueprint_session):
	account_info = blueprint_session.get('/user')
	if account_info.ok:
		account_info_json = account_info.json()
	else:
		account_info_json = None
	return account_info_json


def orgsAccountInfo(blueprint_session, github_user):
	orgs_info = blueprint_session.get('/users/{user}/orgs'.format(user = github_user))
	if orgs_info.ok:
		orgs_info_json = orgs_info.json()
	else:
		orgs_info_json = None
	return orgs_info_json


def orgReposInfo(blueprint_session):
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
	'''repos_info = blueprint_session.get('/orgs/{org}/repos?client_id={}&client_secret={client_secret}'.format(org = organisation,
		client_id = client_id,
		client_secret = client_secret),
	headers = headers)''' ##in_production
	repos_info = blueprint_session.get('/orgs/{org}/repos'.format(org = organisation))
	if repos_info.ok:
		repos_info_json = repos_info.json()
	else:
		repos_info_json = None
	return repos_info_json	


@oauth_authorized.connect_via(github_blueprint) ##Signal sent on log in
def github_logged_in(blueprint, token):
	account_info = accountInfo(blueprint.session)

	if account_info is not None:
		username = account_info['login']

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
	if not loggedIn():
		return redirect(url_for("github.login"))
	else:
		account_info = accountInfo(github)
		if account_info is not None:
			return url_for('showFrontPage')
		else:
			return "Request Failed"


@app.route('/github_logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('showFrontPage'))
## ----------------------------------------------------------------------------------------------- ##


if __name__ == '__main__':
	if "--setup" in sys.argv:
		with app.app_context():
			db.create_all()
			db.session.commit()
			print("Database tables created")
	os.environ['MARAUDERS_SECRET_KEY'] = 'super_secret_key' ##in_production
	os.environ['MARAUDERS_DATABASE_URL'] = 'www.google.com' ##in_production
	app.secret_key = os.environ.get('MARAUDERS_SECRET_KEY')
	app.debug = True
	os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' ##in_production
	app.run(host = '0.0.0.0', port = 5000)