# Portfolio manager using yahoo finance web scraping


![example workflow](https://github.com/phillip2468/stocks_scraper_2/actions/workflows/tests.yml/badge.svg)


A web application designed for tracking and managing stocks from [yahoo finance](https://au.finance.yahoo.com/).

It is a stateless, single-page app using [Flask](https://flask.palletsprojects.com/en/2.0.x/) and [React JS](https://reactjs.org/) to manage and respond to requests made by the user. It can be deployed on [Heroku](https://www.heroku.com/) which allows users to access the website from any device they wish to choose.

When deployed to [Heroku](https://www.heroku.com/) the flask application runs inside a [Gunicorn](https://gunicorn.org/) WSGI app server. Any interactions that require storage and retrival are performed by the [Postgresql](https://www.postgresql.org/) database. A seperate [celery](https://docs.celeryproject.org/en/stable/getting-started/introduction.html) worker performs actions in the background asynchronously and tasks are stored in a separate [Redis](https://redis.io/) queue. 

An example of this website can be found [here](https://morning-temple-33157.herokuapp.com/).

