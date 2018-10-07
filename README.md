# [Marauders-Website](https://github.com/Marauders-9998/Marauders-Website)
![Python](https://img.shields.io/badge/python-v3.6-blue.svg)
[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html)
[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.png?v=103)](https://github.com/ellerbrock/open-source-badges/)

## Running the Website locally

### Fork and Clone
Fork this repository.<br>
Clone your forked repository.
```
git clone https://github.com/<user_name>/Marauders-Website.git
```

### Make a Github OAuth App
Register you new [Github OAuth App](https://github.com/settings/applications/new)
- **Homepage Url**: http://marauders.com:5000/
- **Authorization Callback URL**: http://marauders.com:5000/github_login/github/authorized

### Add names for localhost
```
cd /etc
nano hosts
```
Now add these names to 127.0.0.1 IP address:<br>
> marauders.com<br>
> api.marauders.com

### Add some Environment Variables
Add the environment variables and their corresponding values as specified in **Config_Variables** file.

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
