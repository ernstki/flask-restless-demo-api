# Example Flask + Flask-Restless API

## Requirements

* Python 2.7.x or 3.5.x (later is probably OK)
* virtualenv

## Installation

1. Clone this repository and generate a fresh virtual environment:

    ```
    git clone git@github.uc.edu:ernstki/flask-restless-demo-api.git
    virtualenv venv && source venv/bin/activate
    ```

2. Install necessary Python packages using `pip`:

    ```
    pip install -r requirements.txt
    ```

3. Tell Flask where to find the app, initialize the `organism` database, and
   launch the Flask web application:

    ```
    export FLASK_APP=demoapi/demoapi.py
    flask initdb
    flask run  # defaults to http://127.0.0.1:5000
    ```

    If you install [autoenv], you don't have to set `FLASK_APP`, it's done for
    you automatically when you enter the directory.

    If you're running the Flask application within a VirtualBox VM, you'll want
    to be sure that the app runs on 0.0.0.0, so that the VirtualBox port
    forwarding works correctly. You can launch the app with command line flags
    to achieve that:

    ```
    flask run --host=0.0.0.0  # optionally: --port=5000
    ```

## Other tips

Out of the box, this Flask app is set up to use a SQLite3 database in the
named `organism.db` in the current working directory, but with slight
modifications, you can use a MySQL database instead. (Check out the comments
in `config.py`.)

The two `.sql` files are provided so that you can feed them into either
`mysql` or `sqlite3` at the command line to create the table schema and insert
the default values. Here's a sample invocation for SQLite:

```
sqlite3 organism.db < organism_table_sqlite3.sql
```

[autoenv]: https://github.com/kennethreitz/autoenv
