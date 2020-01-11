# ----------------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------------- #
import sys
import os
import requests
import simplejson as json
# ----------------------------------------------------------------------------------------------- #


# ----------------------------------------------------------------------------------------------- #
# ---------------------------------- Necessary Flask Modules ------------------------------------ #
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, make_response
# ----------------------------------------------------------------------------------------------- #


# ----------------------------------------------------------------------------------------------- #
# -------------------- Importing modules for database and Github OAuth -------------------------- #
from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin, SQLAlchemyBackend
from flask_dance.consumer import oauth_authorized
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, current_user, LoginManager, login_required, login_user, logout_user
from sqlalchemy.orm.exc import NoResultFound

# ----------------------------------------------------------------------------------------------- #


# ----------------------------------------------------------------------------------------------- #
# ----- Organisation to get github project from and github ids allowed for creating a blog ------ #
ORGANISATION = 'Marauders-9998'
ALLOWED_USERS_IDs = [27439964, 31085591]
# ----------------------------------------------------------------------------------------------- #


# ----------------------------------------------------------------------------------------------- #
# --------------- Initialising the flask object and registering github blueprint ---------------- #
app = Flask(__name__)
WEBSITE_URL = "marauders.com:5000"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('MARAUDERS_LOGIN_DATA')

CLIENT_ID = os.environ.get('GITHUB_APP_CLIENT_ID')
CLIENT_SECRET = os.environ.get('MARAUDERS_GITHUB_SECRET')
GITHUB_BLUEPRINT = make_github_blueprint(client_id=CLIENT_ID,
                                         client_secret=CLIENT_SECRET)
app.register_blueprint(GITHUB_BLUEPRINT, url_prefix='/github_login')
# ----------------------------------------------------------------------------------------------- #


# ----------------------------------------------------------------------------------------------- #
# -------------------------------------- Database setup ----------------------------------------- #
db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True)


class OAuth(OAuthConsumerMixin, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)


GITHUB_BLUEPRINT.backend = SQLAlchemyBackend(OAuth, db.session, user=current_user, user_required=False)  ##in_production
# GITHUB_BLUEPRINT.backend = SQLAlchemyBackend(OAuth, db.session, user=current_user)
# ----------------------------------------------------------------------------------------------- #


# ----------------------------------------------------------------------------------------------- #
# --------------------------------- Setting up login manager ------------------------------------ #
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ----------------------------------------------------------------------------------------------- #

def website_urlmaker(url_got):
    return url_got.format(protocol="http", website_url=WEBSITE_URL, access_token="{/access_token}")


def render_page(html_page, **kwargs):
    if loggedIn():
        account_info = accountInfo(github)
        if account_info is not None:
            orgs_info = orgsAccountInfo(github, github_user=account_info['login'])
            user_name = account_info['login']
            user_image = account_info['avatar_url']
            user_url = account_info['html_url']
            kwargs['usr_name'] = user_name
            kwargs['usr_img'] = user_image
            kwargs['usr_url'] = user_url
            kwargs['userLogged'] = True
            kwargs['orgs_info'] = orgs_info
            kwargs['maraudersLogged'] = maraudersLoggedIn()
        else:
            return "Request Failed"
    else:
        kwargs['userLogged'] = False

    return render_template(html_page, org=ORGANISATION, **kwargs)


def updateLimiting(auth_token):
    # Code to update the necessary information for limiting the api hits per user
    pass


@app.route('/')
def showFrontPage():
    print("Hello World, from Maruaders")
    return render_page('front_page.html')


@app.route('/<auth_token>', subdomain="api")
@app.route('/', subdomain="api")
def apiFrontPage(auth_token=None):
    if loggedIn() or validAccessToken(auth_token):
        # Find auth_token if directly logged in
        updateLimiting(auth_token)
        homePageJSON = {
            "api":
                {
                    "api_url": website_urlmaker("{protocol}://api.{WEBSITE_URL}"),
                    "blogs_url": website_urlmaker("{protocol}://api.{WEBSITE_URL}/blogs"),
                    "forum_url": website_urlmaker("{protocol}://api.{WEBSITE_URL}/forum"),
                    "projects_url": website_urlmaker("{protocol}://api.{WEBSITE_URL}/projects"),
                },
            "html":
                {
                    "html_url": website_urlmaker("{protocol}://{WEBSITE_URL}"),
                    "blogs_html_url": website_urlmaker("https://marauders9998.blogspot.com"),
                    "forum_html_url": website_urlmaker("{protocol}://{WEBSITE_URL}/forum"),
                    "projects_html_url": website_urlmaker("{protocol}://{WEBSITE_URL}/projects")
                }}
        response = make_response(jsonify(homePageJSON), 200)
    else:
        UnauthAPI = {
            "message": "Unauthorized",
            "access":
                {
                    "marauders_login_url": website_urlmaker("{protocol}://{WEBSITE_URL}/github"),
                    "api_url": website_urlmaker("{protocol}://api.{WEBSITE_URL}{access_token}")
                }}
        response = make_response(jsonify(UnauthAPI), 401)

    response.headers['Server'] = app.config['SERVER_NAME']
    response.headers['Content-Type'] = 'application/json'
    # Number of api hits allowed per user per specified time
    response.headers['X-RateLimit-Limit'] = '60'
    # Show the allowed number of api hits for the user for the current time interval
    response.headers['X-RateLimit-Remaining'] = '60'  ##in_production
    return response


def validAccessToken(auth_token):
    if auth_token:
        # Code to check for the validation token
        return True
    else:
        return False


@app.route('/projects/')
def showProjectsPage():
    with open('colors.json') as f:
        lang_info = json.load(f)
    repos = []
    repositories = orgReposInfo(github)
    if repositories:
        for repository in repositories:
            repo = {'id': repository['id'], 'name': repository['name'], 'url': repository['html_url'],
                    'issues': repository['open_issues_count'], 'forks': repository['forks_count'],
                    'desc': repository['description'], 'lang': repository['language']}
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
        response.headers['Server'] = app.config['SERVER_NAME']
        return response

    return render_page('projects_page.html', repositories=repos[::-1])


@app.route('/projects/<auth_token>', subdomain="api")
@app.route('/projects/', subdomain="api")
def apiProjectsPage(auth_token=None):
    if loggedIn() or validAccessToken(auth_token):
        projectsJSON = {

            "projects": orgReposInfo(github, auth_token)
        }
        response = make_response(jsonify(projectsJSON), 200)
    else:
        UnauthAPI = {
            "message": "Unauthorized",
            "access":
                {
                    "marauders_login_url": website_urlmaker("{protocol}://{WEBSITE_URL}/github"),
                    "api_url": website_urlmaker("{protocol}://api.{WEBSITE_URL}{access_token}")
                }}
        response = make_response(jsonify(UnauthAPI), 401)

    response.headers['Server'] = app.config['SERVER_NAME']
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/blogs/')
def showBlogPage():
    return render_page('blog_page.html')


@app.route('/blogs/<auth_token>', subdomain="api")
@app.route('/blogs/', subdomain="api")
def apiBlogsPage(auth_token=None):
    if loggedIn() or validAccessToken(auth_token):
        blogsJSON = {
        }
        response = make_response(jsonify(blogsJSON), 200)
    else:
        UnauthAPI = {
            "message": "Unauthorized",
            "access":
                {
                    "marauders_login_url": website_urlmaker("{protocol}://{WEBSITE_URL}/github"),
                    "api_url": website_urlmaker("{protocol}://api.{WEBSITE_URL}{access_token}")
                }}
        response = make_response(jsonify(UnauthAPI), 401)

    response.headers['Server'] = app.config['SERVER_NAME']
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/forum/')
@login_required
def showForumPage():
    return render_page('forum_page.html')


@app.route('/new_blog/', methods=['GET', 'POST'])
@login_required
def showNewBlogPage():
    if maraudersLoggedIn():
        return render_page('new_blog_page.html')
    else:
        response = make_response(render_page("Unauthorized.html"), 401)
        response.headers['Content-Type'] = 'text/html'
        return response


# ----------------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------------- #
def loggedIn():
    if not github.authorized:
        return False
    else:
        return True


def maraudersLoggedIn():
    if loggedIn():
        account_info = accountInfo(github)
        if account_info is not None:
            if account_info['id'] in ALLOWED_USERS_IDs:
                return True
    return False


def accountInfo(blueprint_session):
    account_info = blueprint_session.get('/user')
    if account_info.ok:
        account_info_json = account_info.json()
    else:
        account_info_json = None
    return account_info_json


def orgsAccountInfo(blueprint_session, github_user):
    orgs_info = blueprint_session.get('/users/{user}/orgs'.format(user=github_user))
    if orgs_info.ok:
        orgs_info_json = orgs_info.json()
    else:
        orgs_info_json = None
    return orgs_info_json


def orgReposInfo(blueprint_session, auth_token=None):
    repos_info = None
    if auth_token:
        request_url = 'https://api.github.com/orgs/{org}/repos?access_token={token}'.format(org=ORGANISATION,
                                                                                            token=auth_token)
        repos_info = requests.get(request_url)
    else:
        repos_info = blueprint_session.get('/orgs/{org}/repos'.format(org=ORGANISATION))
    # print('repos_info.ok', repos_info.ok)
    if repos_info.ok:
        repos_info_json = repos_info.json()
    else:
        repos_info_json = None
    return repos_info_json


@oauth_authorized.connect_via(GITHUB_BLUEPRINT)  ##Signal sent on log in
def github_logged_in(blueprint, token):
    account_info = accountInfo(blueprint.session)

    if account_info is not None:
        username = account_info['login']

        query = User.query.filter_by(username=username)

        try:
            user = query.one()
        except NoResultFound:
            user = User(username=username)
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


# ----------------------------------------------------------------------------------------------- #


if __name__ == '__main__':
    if "--setup" in sys.argv:
        with app.app_context():
            db.create_all()
            db.session.commit()
            print("Database tables created")
    app.secret_key = os.environ.get('MARAUDERS_SECRET_KEY')
    app.config['SERVER_NAME'] = WEBSITE_URL
    app.config['JSON_SORT_KEYS'] = False
    app.debug = False
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  ##in_production
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
