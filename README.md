
# Marauders-Website


[![Open Issues](https://img.shields.io/github/issues/Marauders-9998/Marauders-Website?style=for-the-badge&logo=github)](https://github.com/Marauders-9998/Marauders-Website/issues)  [![Forks](https://img.shields.io/github/forks/Marauders-9998/Marauders-Website?style=for-the-badge&logo=github)](https://github.com/Marauders-9998/Marauders-Website/network/members)  [![Stars](https://img.shields.io/github/stars/Marauders-9998/Marauders-Website?style=for-the-badge&logo=reverbnation)](https://github.com/Marauders-9998/Marauders-Website/stargazers)   ![Made with Flask](https://img.shields.io/badge/Made%20with-Flask-blueviolet?style=for-the-badge&logo=flask)   [![Slack](https://img.shields.io/badge/Slack-Chat-informational?style=for-the-badge&logo=slack)](https://join.slack.com/t/marauders9998/shared_invite/enQtODkwNTgxMTAxNTIwLTJhOWFhNzQwYjU3MTUwN2Y5NmZmN2VjMTc4NDA1MGRjZmIzNWEzZDU0ODZjNjE3NjkzNzk4ZmI1ZGFiOGE2NzQ)

Official website of Marauders. [Visit](http://marauders9998.herokuapp.com/)

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
pip3 install -r requirements.txt
pip3 uninstall pkg-resources==0.0.0
python3 main_app.py [--setup]
```
### To Terminate the server

Press Ctrl+C
