import sys, os, requests
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, make_response

import httplib2
import simplejson as json

app = Flask(__name__)

@app.route('/')
def showFrontPage():
	print("Hello World, from Maruaders")
	return render_template('front_page.html')


if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 5000)