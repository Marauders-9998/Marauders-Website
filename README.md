# [Marauders-Website](https://github.com/Marauders-9998/Marauders-Website)
![Python](https://img.shields.io/badge/python-v3.6-blue.svg)
[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html)
[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.png?v=103)](https://github.com/ellerbrock/open-source-badges/)

## Running the Website locally
### Add names for localhost
```
cd /etc
nano hosts
```
Now add these names to 127.0.0.1 IP address:<br>
marauders.com<br>
api.marauders.com<br>

### Running the app
```
git clone https://github.com/Marauders-9998/Marauders-Website.git
cd Marauders-Website
python3 -m venv venv
source venv/bin/activate
pip3 install flask jinja2 certifi chardet gunicorn requests httplib2 simplejson sqlalchemy
pip3 install flask_dance flask_login sqlalchemy_utils blinker flask_sqlalchemy flask-restful
python3 main_app.py
```
