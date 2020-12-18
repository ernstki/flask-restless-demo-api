#!/usr/bin/env python
###########################################################################
##
##  Simple Flask-Restless-based REST API and example search form
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
parentdir = os.path.join(os.path.dirname(__file__), '..')

# the default CSV file to load when you do 'flask initdb'
csvfile = os.path.join(parentdir, 'organism_table.csv')

app = Flask(__name__)
app.config.from_pyfile('config.py')  # same directory as __file__ inferred?

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
                   url_prefix=app.config['API_PREFIX'])

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
@app.route(app.config['API_PREFIX'])  # prob. smarter to use Flask blueprint
def api_root():
    """Redirect casual users to the API help page--you're lookin' at it!"""
    return redirect(url_for('help'))

# ----------------------------------------------------------------------------
#                    R E S T     A P I     e n d p o i n t s
# ----------------------------------------------------------------------------

# helper function to reformat docstrings for API help output
def docstring_to_help(endpoint):
    lines = []
    for l in [l.strip() for l in endpoint.__doc__.split("\n")]:
        if l:  # if the line had any content besides whitespace
            lines += [l.strip()]
    return ' '.join(lines)


@app.route(app.config['API_PREFIX'] + '/help', methods = ['GET'])
def help():
    """Return API endpoint documentation as a JSON structure."""
    func_list = {}
    for rule in app.url_map.iter_rules():
        if rule.rule.startswith(app.config['API_PREFIX']):
            func_list[rule.rule] = \
                    docstring_to_help(app.view_functions[rule.endpoint])
    return jsonify(func_list)


@app.route(app.config['API_PREFIX'] + '/organism/search')
def search_organisms():
    """Substring match on organisms using the 'q=' query string parameter."""
    # Return anything with a substring match on the 'name' field
    cond = Organism.name.like("%{}%".format(request.args.get('q', '')))
    return jsonify([match.as_dict() for match in Organism.query.filter(cond)])


@app.route(app.config['API_PREFIX'] + '/organism/autocomplete')
def autocomplete_organisms():
    """Search returning correct structure for autocomplete with select2.js."""
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
# Refer to http://click.pocoo.org/5/options/ for help on option parsing

@app.cli.command()
@click.option('csvfile', '--from-file', type=click.File(), default=csvfile,
              help='Load data from CSV file.')
def initdb(csvfile):
    """Create 'organism' table if it doesn't exist."""
    click.secho("Creating database tables for '{}'... "
                .format(app.config['SQLALCHEMY_DATABASE_URI']), fg='yellow',
                nl=False)

    # This create the table and the schema
    db.drop_all()
    db.create_all()

    for line in csvfile.readlines():
        db.engine.execute(
            "INSERT INTO organism (name) VALUES('%s')" % line.strip()
        )

    click.secho('done\n', fg='green')


@app.cli.command()
@click.option('--with-ids', is_flag=True, default=False,
              help='Include unique IDs with each record.')
@click.option('--as-csv', is_flag=True, default=False,
              help='Dump in comma-separated value format.')
def dumpdb(with_ids, as_csv):
    """Dump contents of database to the terminal."""
    sep = '\t'

    if as_csv:
        with_ids = True
        sep = ','
        cols = [col.name for col in Organism.__table__.columns]

        click.echo(','.join(cols))

    for rec in Organism.query.all():
        cols = [rec.name]

        if with_ids:
            cols.insert(0, str(rec.id))

        click.echo(sep.join(cols))


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
