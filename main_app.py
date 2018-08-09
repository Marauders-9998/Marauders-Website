import sys, os, requests
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, make_response

import httplib2
import simplejson as json

app = Flask(__name__)

@app.route('/')
def showFrontPage():
	print("Hello World, from Maruaders")
	return render_template('front_page.html')

@app.route('/projects')
def showProjectsPage():
	marauders_api = 'https://api.github.com/orgs/Marauders-9998/repos'
	marauders_api_response = requests.get(marauders_api)
	repos = []
	#For testing purposes
	if True:#marauders_api_response.status_code == 200:
		repositories = marauders_api_response.json()
		for repository in repositories:
			repo = {}
			repo['id'] = 'abc'# repository['id']
			repo['name'] = 'def'# repository['name']
			repo['url'] = 'ghi'# repository['html_url']
			repo['issues'] = 'jkl'# repository['open_issues_count']
			repo['forks'] = 'mno'# repository['forks_count']
			repo['desc'] = 'pqr'# repository['description']
			repo['lang'] = 'stu'# repository['language']
			repo['issues_api_url'] = 'vwx'# repository['issues_url'].split('{')[0]
			repo['commits_api_url'] = 'yza'# repository['commits_url'].split('{')[0] 
			repos.append(repo)
	else:
		response = make_response(json.dumps('Could not request Github'), marauders_api_response.status_code)
		response.headers['Content-Type'] = 'application/json'
		return response

	print(repos)

	return render_template('projects_page.html', repositories = repos[::-1])

@app.route('/blog')
def showBlogPage():
	return render_template('blog_page.html')

@app.route('/forum')
def showForumPafe():
	return render_template('forum_page.html')

if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 5000)