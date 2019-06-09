# BucketList-API

The innovative knights-manager app is an application that allows users  to users to register, search, upload and download student project reports.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.
- Just clone this repository by typing: `https://github.com/coe3-knights/proj.git`
- Switch to project directory: `cd proj`
- Install project requirements using python pip. But wait, you have to have some stuff before you get to this point. So these are:

### Prerequisites

- Python3.5 and above
- Python virtual environment
Just type:
```
python -V
```
in your terminal and if its not greater than or equal to 3.5, you're not in big trouble, there are tons of tutorials to get up up and running with these. Just grub one then come back when done.

### Installing

Now, you have python3 and a way of running a virtual environment. Lets set up the project environment.(remember we're still in the app directory)

1. Create your virtual environment. Usually, without any wrappers:
```
python -m venv venv
```
2. Start your virtual environment:
```
source venv/bin/activate
```
3. Install the project requirements specified in the requirements.txt file. Usually,
```
pip install -r requirements.txt
```
4. *Do Migrations*. This application uses postgresql. If you don't have psql you may install it here.
Create a `flask_api` database to be used by the application while running on your localhost.
Then, you can do migrations as:
```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

This is enough to get you started.
You can now run the application using:

`python run.py`

## API Endpoints
You can use postman or even curl to reach out to the following api endpoints:

URL Endpoint	|               HTTP Request   | Resource Accessed | Access Type|
----------------|-----------------|-------------|------------------
/v1/signup  |      POST	| Register a new user|publc
/v1/login	  |     POST	| Login and retrieve token|public
/v1/logout	  |     POST	| Logout and thus deactivate token|public
/v1/projects	  |  GET	| Get projects colletion|public
/v1/projects/search?q=<query>| GET	|Search a project|public

## Deployment

This app is ready for Heroku. You can deploy your copy of this app by:
`heroku create <your_url_name>` (where <your_url_name> is what you want to call your app)
`git push heroku master` 
..and boom, you're done!
If you have never worked with Heroku, you can learn how to [Deploy Python Applications on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python#introduction)
## Built With

* [Python Flask](https://www.fullstackpython.com/flask.html) - The web framework used for this API

## Contributing

You can create your pull request. :D

## Versioning

This is the first version of this app 

## Authors

* **Blessed Boakye Britwum** - *Kickstarting the project* - [@cbenisson](https://github.com/coe3-knights/proj)
* **Godwin Krieger** 
* **Quansah Jacklingo**

## Acknowledgments

* Jephtah Yankey - Inspiring the idea.
