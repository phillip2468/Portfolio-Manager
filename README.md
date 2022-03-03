# Portfolio manager using yahoo finance web scraping
![example workflow](https://github.com/phillip2468/stocks_scraper_2/actions/workflows/tests.yml/badge.svg)


A web application designed for tracking and managing stocks from [yahoo finance](https://au.finance.yahoo.com/).

It is a stateless, single-page app using [Flask](https://flask.palletsprojects.com/en/2.0.x/) and [React JS](https://reactjs.org/) to manage and respond to requests made by the user. It can be deployed on [Heroku](https://www.heroku.com/) which allows users to access the website from any device they wish to choose.

When deployed to [Heroku](https://www.heroku.com/) the flask application runs inside a [Gunicorn](https://gunicorn.org/) WSGI app server. Any interactions that require storage and retrieval are performed by the [Postgresql](https://www.postgresql.org/) database. A seperate [celery](https://docs.celeryproject.org/en/stable/getting-started/introduction.html) worker performs actions in the background asynchronously and tasks are stored in a separate [Redis](https://redis.io/) queue. 

An example of this website can be found [here](https://morning-temple-33157.herokuapp.com/).

![Screenshot 2022-03-03 at 21-11-44 Money maker](https://user-images.githubusercontent.com/54766922/156543740-baad1a7e-7481-425e-8098-94417a198cc8.png)
![Screenshot 2022-03-03 at 21-11-54 Money maker](https://user-images.githubusercontent.com/54766922/156543744-bd79fd6f-3778-4713-933b-a9becab273b4.png)
![Screenshot 2022-03-03 at 21-12-09 Money maker](https://user-images.githubusercontent.com/54766922/156543749-b2ce83e4-99a2-4bce-9715-2a6760b9a603.png)


# Development requirements
  - Windows 10 or higher / Linux OS
  - Python3.10+ and pip
  - Node.js 16.4+
  - Yarn 1.2+
  - Terminal
  - An understaning of basic git and yarn commands + some IDE/ text editor of your choice
  - Any latest web browser (Chrome, Firefox, etc...)
 
# Getting started
Make sure the above requirements are met and that a terminal of your choosing is opened.

Git clone this repository, making sure to change into the directory after cloning.

Create a virtual enviroment with python (note that the fourth argument can be whatever name you want) ```python -m venv venv```

Activate the virtual environment (in Windows this command is) ```venv/Scripts/activate```.

Install required dependencies with ```pip -r requirements.txt```.

Then run the backend with ```python3 backend/run.py```.

In a new terminal change into the frontend directory.

Install required packages with ```yarn install```.

Then to start the frontend use ```yarn start```.


# Project structure
The project is divided into 2 major sections; the backend and frontend folders. 

The backend routes requests as defined by each blueprint in the app.py file. Each blueprint is registered to the application, so that requests can be properly routed. Each blueprint contains its own methods (and thus their own urls) prefixed by the base blueprint url (for example the url for '/login' is 'auth/login' since it is in the auth blueprint). All methods exist within the routes.py in each module.

```
└── backend
    └── db                      
        ├── versions            stores previous migrations made by alembic
        ├── env.py              commands for alembic migrations
        ├── script.py.mako      provides a git like messages for all migrations
        ├── seeds.py            provides example data for the website
    └── money_maker
        ├── auth                handles the authentication of user accounts
        ├── home                displays trending tickers and most actively traded stocks on the home page
        ├── models              SQL tables as defined by SQLAlchemy ORM syntax
        ├── news                scrapes news articles from AFR
        ├── portfolio           stores stocks as a list for viewing later with features such as units purchased and unit per price
        ├── quote               retrieves information for an individual stock
        ├── search              retrieves a matching stock given a keyword
        ├── tasks               background tasks powered by celery workers
        ├── tickers             retrieves infromation for several stocks
        ├── trending            provides simple trends on all stocks based on certain attributes
        ├── watchlist           stores stocks as a list for viewing later
        ├── app.py              entry point to flask application
        ├── celery.py           entry point for celery app
        ├── config.py           configuration details for flask and celery
        ├── extensions.py       callback of extra features that are attached to the flask application
        ├── helpers.py          provides useful functions used throught the flask application
        ├── config.py           configuration details for pytests
        ├── wsgi.py             alternative entry for wsgi servers
    ├── .flaskenv               environment variables for flask
    ├── alembic.ini             used for alembic migrations
    ├── conftest.py             fixtures and constants used by pytests
    ├── extensions.py           used for celery applications
    ├── pyproject.toml          github actions config file
    ├── pytest.ini              configuration file for pytests
    ├── requirements.txt        pip packages used for tox pytests
    ├── run.py                  main method for starting the backend
    ├── tox.ini                 configuration file used for tox testing
    
```

The frontend meanwhile has all the pages routed in App.js file. These pages allow for the movement inside the application but do not interact anyway with the backend. Seperate fetch functions are used in order to retrieve the JSON data and components are modified in order to reflect these interactions. 

```
└── frontend
    └── build                   importantly contains the index.html which provides a index for all webpages in the website
    └── public                  contains static files
    └── src
        └── components          individual javascript/html components, designed for resuability
        └── pages               individual webpages
        └── store               datastore for user authentication
        ├── App.css             provides default css styling
        ├── App.js              router for all pages
        ├── index.css           default css for index
        ├── index.js            default index file
        ├── logo.svg            used to display icon in tab
        ├── reportWebVitals.js  used for testing
        ├── setupTest.js        testing
    ├── .eslint.js              eslint config file
    ├── .gitignore              used to make sure that certain files aren't uploaded
    ├── README.me               readme generated from react-create-app
    ├── package.json            contains a list of packages required to use the application
```
