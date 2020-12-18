# you have to set DEBUG as an environment variable; refer to
# https://flask.palletsprojects.com/en/1.1.x/config/#environment-and-debug-features
#DEBUG                    = True
EXPLAIN_TEMPLATE_LOADING = True
API_PREFIX               = '/api/v1'

#SQLALCHEMY_ECHO                = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI        = 'sqlite:///organism.db'

#
# Example configuration for local MySQL server
#
#DB_HOST     = 'localhost'
#DB_PORT     = 3306
#DB_DATABASE = 'dbname'
#DB_USER     = 'dbuser'
#DB_PASSWORD = 'GoodPasswordsArePartOfABalancedBreakfast'
#SQLALCHEMY_DATABASE_URI        = \
#    "mysql://{user}:{passwd}@{host}:{port}/{db}".format(
#        user=DB_USER, passwd=DB_PASSWORD, host=DB_HOST, port=DB_PORT,
#        db=DB_DATABASE
#     )
