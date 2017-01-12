#!/usr/bin/env python
###########################################################################
##
##  REST API for querying the 'organisms' MySQL table, intended for
##  use with the Select2 JavaScript typeahead forms library
##
##  Author:  Kevin Ernst <ernstki@mail.uc.edu>
##  Date:    27 Juli 2016
##  
##  References:
##    - http://docs.sqlalchemy.org/en/latest/orm/query.html
##        #sqlalchemy.orm.query.Query.filter
##    - http://docs.sqlalchemy.org/en/latest/orm/internals.html
##        #sqlalchemy.orm.attributes.QueryableAttribute.like
##    - http://www.unixwiz.net/techtips/sql-injection.html
##
##  Thanks:
##    - to Andrey Lando for help sorting out some problems with
##      using .query.filter() with a SQL LIKE condition.
##
###########################################################################
import os
import sys
import re

import click
from flask import Flask, render_template, jsonify, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from sqlalchemy import text
import flask_restless

basedir = os.path.dirname(__file__)
parentdir = os.path.dirname(__file__) + os.sep  + '..'

app = Flask(__name__)
app.config.from_pyfile('config.py')

Bootstrap(app)

db = SQLAlchemy(app)


class Organism(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    # Courtesy: https://stackoverflow.com/a/11884806
    def as_dict(self):
        """
        Return the entire table serialized as JSON

        (Note that you can also access the internal dictionary of SQLAlchemy
        objects with '.__dict__'.)
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# Create the Flask-Restless API manager and make 'organism' available
# (from http://flask-restless.readthedocs.io/en/0.17.0/quickstart.html)
manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(Organism, methods=['GET'], #, 'POST', 'DELETE'],
                   url_prefix=app.config['URL_PREFIX'])

# ----------------------------------------------------------------------------
#               s i m p l e    t e s t    i n p u t    f o r m 
# ----------------------------------------------------------------------------
@app.route('/')
def home():
    """Return a simple search form with autocomplete"""
    return render_template('home.html')

@app.route('/about')
def about():
    """Return the about page"""
    return render_template('about.html')

@app.route('/api')
@app.route(app.config['URL_PREFIX'])  # prob. smarter to use Flask blueprint
def api_root():
    """Redirect casual users to the API help page"""
    return redirect(url_for('help'))

# ----------------------------------------------------------------------------
#                    R E S T     A P I     e n d p o i n t s
# ----------------------------------------------------------------------------

@app.route(app.config['URL_PREFIX'] + '/help', methods = ['GET'])
def help():
    """Print available functions."""
    func_list = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__
    return jsonify(func_list)

@app.route(app.config['URL_PREFIX'] + '/organism/search')
def search_organisms():
    """Substring match on organisms using the 'q=' query string parameter"""
    # Return anything with a substring match on the 'name' field
    cond = Organism.name.like("%{}%".format(request.args.get('q', '')))
    return jsonify([match.as_dict() for match in Organism.query.filter(cond)])

@app.route(app.config['URL_PREFIX'] + '/organism/autocomplete')
def autocomplete_organisms():
    """Search returning correct fields for autocomplete with select2.js"""
    cond = Organism.name.like("%{}%".format(request.args.get('q', '')))
    matches = [match.as_dict() for match in Organism.query.filter(cond)]

    # Rename the 'name' field to 'text' to make select2.js happy; the
    # list() is required because map() returns an iterator in Python 3.x.
    # See: https://stackoverflow.com/a/1303354
    return jsonify(list(map(lambda x: {'id': x['id'], 'text': x['name']},
                            matches)))

# ----------------------------------------------------------------------------
#                c o m m a n d - l i n e    o p e r a t i o n s
# ----------------------------------------------------------------------------
@app.cli.command()
def initdb():
    """Create 'organism' table if it doesn't exist"""
    click.secho("Creating database tables for '{}'... "
                .format(app.config['SQLALCHEMY_DATABASE_URI']), fg='yellow',
                nl=False)

    # This create the table and the schema
    db.drop_all()
    db.create_all()

    with open(parentdir + os.sep + 'organism_table.csv', 'r') as organisms:
        for orgname in organisms.readlines():
            db.engine.execute("INSERT INTO organism (name) VALUES('{}')"
                              .format(orgname.replace('\n', '')))

    click.secho('done\n', fg='green')


if __name__ == '__main__':
    # You could specify host= and port= params here, but they won't be used if
    # you invoke the app in the usualy way with 'flask run'
    # Ref: http://flask.pocoo.org/docs/0.11/api/#flask.Flask.run
    #app.run()

    click.secho('\nPlease launch the demo API with\n', err=True)
    click.secho('    export FLASK_APP=demoapi/demoapi.py', bold=True,
                err=True)
    click.secho('    flask run [--host=X.X.X.X] [--port=YYYY]\n', bold=True,
                err=True)

