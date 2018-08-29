# [Marauders-Website](https://github.com/Marauders-9998/Marauders-Website)

## Deploying Flask App on Heroku
```
heroku login
git clone https://github.com/Marauders-9998/Marauders-Website.git
cd Marauders-Website
heroku create <heroku_app_name>
nano Procfile
```
Put this in Procfile and Save
> web: python3 main_app.py
```
python3 -m venv venv
source venv/bin/activate
pip3 install flask jinja2 certifi chardet gunicorn requests httplib2 simplejson sqlalchemy flask_dance flask_login sqlalchemy_utils blinker flask_sqlalchemy
pip3 uninstall pkg-resources==0.0.0
pip3 freeze > requirements.txt
git add -A
git commit -m "Changes"
git push heroku master
heroku ps:scale web=1
heroku open
```
