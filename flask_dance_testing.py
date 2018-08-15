from flask import Flask, redirect, url_for
from flask_dance.contrib.github import make_github_blueprint, github

app = Flask(__name__)

github_blueprint = make_github_blueprint(client_id = '6fbf106b39b23aeeba15', client_secret = 'c9b6b6fd35c11df5b240af0cac4e15619a5b3b83')

app.register_blueprint(github_blueprint, url_prefix = '/github_login')

@app.route('/github'):
def github_login():
	if not github.authorized:
		return redirect(url_for(github.login))
	else:
		account_info = github.get('/user')
		if account_info.ok:
			account_data = account_info.json()
			return "Your github name is {}".format(account_data['login'])
		else:
			return "Request Failed"


if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 8080)