import os

from flask import Flask
from . import db

def create_app(test_config=None):
    #create and configure app
    app = Flask(__name__,instance_relative_config=True) #instance_relative_config shows that the 
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path,'flaskr.sqlite'),
    )

    if test_config is None:
        #load instance config, if not testing
        app.config.from_pyfile('config.py',silent=True)
    else:
        #load test config if passed in
        app.config.from_mapping(test_config)

    #insure that instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #a simple Hello World page for flask
    @app.route('/hello')
    def hello():
        return "Hello World!"
    
    #this is just to test
    @app.route('/hamza')
    def hamza():
        return "Hello Hamza Work Harder"
    
    
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/',endpoint='index')

    return app

            