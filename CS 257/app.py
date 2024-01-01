'''app.py'''

'''Author: A.J. Ristino'''

'''A Flask app containing routes that serve our HTML pages'''

import flask
import argparse
import api

app = flask.Flask(__name__, static_folder='static', template_folder='templates')
app.register_blueprint(api.api, url_prefix='/api')

@app.route('/')
def index():
    return flask.render_template('mockup_home.html')

@app.route('/mockup_advsearch.html')
def advsearch():
    return flask.render_template('mockup_advsearch.html')

@app.route('/mockup_about.html')
def about():
    return flask.render_template('mockup_about.html')

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Scaffolding for our albums app, including API & DB')
    parser.add_argument('host', help='the host to run on')
    parser.add_argument('port', type=int, help='the port to listen on')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
