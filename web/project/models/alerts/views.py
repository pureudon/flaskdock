from flask import Blueprint
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask import redirect
from project.models.alerts.alert import Alert
from project.models.items.item import Item
import project.models.users.decorator as user_decorators

alert_blueprint = Blueprint("alerts", __name__)


@alert_blueprint.route('/')
def index():
    return "This is the alerts index"


@alert_blueprint.route('/new', methods=['GET', 'POST'])
@user_decorators.requires_login
def create_alert():
    if request.method == "POST":
        name = request.form['name']
        url = request.form['url']
        price_limit = float(request.form['price_limit'])

        item = Item(name, url)
        item.save_to_mongo()

        alert = Alert(session['email'], price_limit, item._id)
        alert.load_item_price() # This already saves to MongoDB
    return render_template("alerts/create_alert.html")


@alert_blueprint.route('/edit/<string:alert_id>', methods=['GET', 'POST'])
@user_decorators.requires_login
def edit_alert(alert_id):
    alert = Alert.find_by_id(alert_id)
    if request.method == "POST":
        price_limit = float(request.form['price_limit'])

        alert.price_limit = price_limit
        alert.save_to_mongo()

        return redirect(url_for('users.user_alerts'))
    return render_template('alerts/edit_alert.html', alert=alert)


@alert_blueprint.route('/deactivate/<string:alert_id>')
@user_decorators.requires_login
def deactivate_alert(alert_id):
    Alert.find_by_id(alert_id).deactivate()
    return redirect(url_for('users.user_alerts'))


@alert_blueprint.route('/delete/<string:alert_id>')
@user_decorators.requires_login
def delete_alert(alert_id):
    Alert.find_by_id(alert_id).delete()
    return redirect(url_for('users.user_alerts'))


@alert_blueprint.route('/activate/<string:alert_id>')
@user_decorators.requires_login
def activate_alert(alert_id):
    Alert.find_by_id(alert_id).activate()
    return redirect(url_for('users.user_alerts'))


@alert_blueprint.route('/<string:alert_id>')
@user_decorators.requires_login
def get_alert_page(alert_id):
    alert = Alert.find_by_id(alert_id)
    return render_template("alerts/alert.html", alert=alert)

#
# @alert_blueprint.route('/for_user:<string:user_id>')
# @user_decorators.require_login
# def get_alerts_for_user(user_id):
#     pass


@alert_blueprint.route('/check_price/<string:alert_id>')
def check_alert_price(alert_id):
    Alert.find_by_id(alert_id).load_item_price()
    return redirect(url_for('.get_alert_page', alert_id=alert_id))
