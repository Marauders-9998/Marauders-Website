
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



## Contribution

 Your contributions are always welcome and appreciated. Following are the things you can do to contribute to this project.

 1. **Report a bug** <br>
 If you think you have encountered an issue, and we should know about it, feel free to report it [here](https://github.com/Marauders-9998/Marauders-Website/issues/new) and we will take care of it.

 2. **Create a pull request** <br>
It can't get better then this, your pull request will be appreciated by the community. You can get started by picking up any open issues from [here](https://github.com/Marauders-9998/Marauders-Website/issues) and make a pull request.
 
|Label| Description |
|--|--|
| [good first issue](https://github.com/Marauders-9998/Marauders-Website/labels/good%20first%20issue) | Issues, good for newcomers |
|[easy](https://github.com/Marauders-9998/Marauders-Website/labels/easy)|Issues with relatively **easy** difficulty|
|[medium](https://github.com/Marauders-9998/Marauders-Website/labels/medium)|Issues with relatively **medium** difficulty|
|[hard](https://github.com/Marauders-9998/Marauders-Website/labels/hard)|Issues with relatively **hard** difficulty|


 > If you are new to open-source, make sure to check read more about it [here](https://www.digitalocean.com/community/tutorial_series/an-introduction-to-open-source) and learn more about creating a pull request [here](https://www.digitalocean.com/community/tutorials/how-to-create-a-pull-request-on-github).
