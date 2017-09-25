from flask import Flask
from flask import render_template
from project.common.database import Database

app= Flask(__name__)
app.config.from_object('project.config')
app.secret_key = "123"

# @app.route('/')
# def hello_world():
#     return "Hello, world!"


@app.before_first_request
def init_db():
    Database.initialize()


@app.route('/')
def home():
    return render_template('home.html')

from project.models.users.views import user_blueprint
from project.models.alerts.views import alert_blueprint
from project.models.stores.views import store_blueprint
app.register_blueprint(user_blueprint, url_prefix="/users")
app.register_blueprint(alert_blueprint, url_prefix="/alerts")
app.register_blueprint(store_blueprint, url_prefix="/stores")


if __name__ == '__main__':
    app.run(debug=True, port=8000)