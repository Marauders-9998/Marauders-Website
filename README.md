# [Marauders-Website](https://github.com/Marauders-9998/Marauders-Website)
![Python](https://img.shields.io/badge/python-v3.6-blue.svg)
[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html)
[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.png?v=103)](https://github.com/ellerbrock/open-source-badges/)

## Make a Github OAuth App
Register you new [Github OAuth App](https://github.com/settings/applications/new)
- Homepage Url: **http://marauders.com:5000/**
- Authorization Callback URL: **http://marauders.com:5000/github_login/github/authorized**

## Fork and Clone
Fork this repository.<br>
Clone your forked repository.
```
git clone https://github.com/<user_name>/Marauders-Website.git
```

## Running the Website locally
### Add names for localhost
```
cd /etc
nano hosts
```
Now add these names to 127.0.0.1 IP address:<br>
> marauders.com<br>
> api.marauders.com

### Add some Environment Variables
Add the environment variables and their corresponding values as specified in **Config_Variables** file.<br><br>
Run the app locally once before deploying on heroku.

### Running the app locally

Include the **--setup** arg when running only for the first time.
```
cd Marauders-Website
python3 -m venv venv
source venv/bin/activate
pip3 install flask jinja2 certifi chardet gunicorn requests httplib2 simplejson sqlalchemy
pip3 install flask_dance flask_login sqlalchemy_utils blinker flask_sqlalchemy flask-restful
pip3 uninstall pkg-resources==0.0.0
python3 main_app.py [--setup]
```
Press Ctrl+C to terminate.

## Deploying the Website on Heroku

#### main_app.py
Update **website_url** with **<your_heroku_app_name>.herokuapp.com**

### Add environment variables to your server
- Go to your [Heroku Dashboard](https://dashboard.heroku.com/apps)
- Select your Heroku App.
- Under Settings tab, click on **Reveal Config Vars**
- Now add the environment variables as specified in **Config_Variables** file.


### Create a Heroku App
Sign up on [Heroku](https://www.heroku.com/) if you haven't got an account.
```
heroku login
cd Marauders-Website
heroku create <heroku_app_name>
```
## Update Github OAuth App
Go to your github app settings.<br>
Update Homepage and Callback URLs.

### Create requirements file for the server
```
pip3 freeze > requirements.txt
```
### Push to Heroku
```
git add -A
git commit -m "Initial Deploy"
git push heroku master
```
### Scale your Heroku App
```
heroku ps:scale web=1
```
### Open up the Website
```
heroku open
```