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
import sys
import re
from flask import Flask, jsonify, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import flask_restless
import click

app = Flask(__name__)
app.config.from_pyfile('config.py')

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

@app.route('/')
@app.route('/api')
@app.route(app.config['URL_PREFIX'])
def index():
    """Redirect casual users to the API help page"""
    return redirect(url_for('help'))

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

    # Rename the 'name' field to 'text' to make select2.js happy
    return jsonify(map(lambda x: {'id': x['id'], 'text': x['name']}, matches))

@app.cli.command()
def initdb():
    """Create 'organism' table if it doesn't exist"""
    click.secho("Creating database tables for '{}'... "
                .format(app.config['SQLALCHEMY_DATABASE_URI']), fg='yellow',
                nl=False)

    # This create the table and the schema
    db.drop_all()
    db.create_all()

    with open('organism_table.csv', 'r') as organisms:
        for orgname in organisms.readlines():
            db.engine.execute("INSERT INTO organism (name) VALUES('{}')"
                              .format(orgname.replace('\n', '')))

    click.secho('done\n', fg='green')

if __name__ == '__main__':
    # I find it kind of moronic that this doesn't actually use the *host* part
    # of SERVER_NAME for, well, the 'host' parameter. As mentioned in the
    # docs[1], it *does* pay attention to the *port* part, sort of, but having
    # SERVER_NAME also set at the same time seems to mess things up.
    #
    # [1] http://flask.pocoo.org/docs/0.11/api/#flask.Flask.run
    app.run(host=app.config['SERVER_HOST'], port=app.config['SERVER_PORT'])

