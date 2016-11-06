DEBUG       = True
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5001
# SERVER_NAME <-- setting this messes everything up, but Flask won't say why
URL_PREFIX  = '/api/v1'

#SQLALCHEMY_ECHO                = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI        = 'sqlite:///organism.db'

#
# Example configuration for local MySQL server
#
#DB_HOST     = 'localhost'
#DB_PORT     = 3306
#DB_DATABASE = 'bioreactor'
#DB_USER     = 'bioreactor'
#DB_PASSWORD = 'BioreactorIsPartOfABalancedBreakfast'
#SQLALCHEMY_DATABASE_URI        = \
#    "mysql://{user}:{passwd}@{host}:{port}/{db}".format(
#        user=DB_USER, passwd=DB_PASSWORD, host=DB_HOST, port=DB_PORT,
#        db=DB_DATABASE
#     )
