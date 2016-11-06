# Example Flask + Flask-Restless API

## Installation

1. Clone this repository and [activate the virtual environment][venv].

    ```
    git clone git@github.uc.edu:Bioreactor/bioreactor-demo-api.git
    virtualenv venv && source venv/bin/activate
    ```

2. Install necessary Python packages (may not be necessary if you're using
   this repo as a template for a child service within the main [Bioreactor
   project][bioreactor])

    ```
    pip install -r requirements.txt
    ```

3. Tell Flask where to find the app, initialize the `organism` database, and
   launch the Flask web application:

    ```
    export FLASK_APP=demoapi.py
    flask initdb
    flask run
    ```

    If you install [autoenv], you don't have to set `FLASK_APP`, it's done for
    you automatically when you enter the directory.

    If you're running the Flask application on the [Bioreactor VM][vm], then
    you'll want to be sure that the app runs on 0.0.0.0:5001, so that the
    VirtualBox port forwarding works correctly. You can lauch the app in either
    of these two ways to achieve that:

    ```
    # either
    flask run --host=0.0.0.0 --port=5001
    # or
    python demoapi.py
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

[bioreactor]: https://github.uc.edu/Bioreactor/bioreactor
[vm]: https://github.uc.edu/Bioreactor/bioreactor-vm
[venv]: ../README.md#establishing-a-python-virtual-environment
[autoenv]: https://github.com/kennethreitz/autoenv
