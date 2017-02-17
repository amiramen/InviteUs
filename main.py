from flask import Flask, url_for
from flask import render_template
from flask import request
import flask
import datetime
import json
from collections import namedtuple
app = Flask("invite_us")
app.debug = True;

# DB #
from database import db_session
from models import *

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
	
# Flask Login #
import flask_login 
	
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
app.secret_key = 'AV61556vdSFFgva54684f53d4f65sd84'

# Tell Flask-Login where the login page is
login_manager.login_view = "show_login_page"
# The message to flash to un-authenticated users
login_manager.login_message = u"You need to log in to view this page"

@login_manager.user_loader
def load_user(userid):
    user = User.query.get(int(userid))
    if user:
        return user
		

from flask_oauth import OAuth
 
oauth = OAuth()
 
facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key='1574120022875620',
    consumer_secret='a42faf0f45cae57a63430f73681376cb',
    request_token_params={'scope': 'email'}
)

@facebook.tokengetter
def get_facebook_oauth_token():
    return flask_login.session.get('oauth_token')



# Root Page #
@app.route("/")
def root():
	#import ipdb; ipdb.set_trace();
	return render_template('calendar_template.html', user=flask_login.current_user, is_user_logged_in=flask_login.current_user.is_authenticated)

# Test Index #
@app.route("/index")
def index():

	return render_template('index.html', user=flask_login.current_user, is_user_logged_in=flask_login.current_user.is_authenticated)

	
# Login Functions #
@app.route('/login/page')
def show_login_page():
	return flask.redirect(url_for('root'))
	"""
	#import ipdb; ipdb.set_trace();
	if flask_login.current_user.is_authenticated():
		return flask.redirect(url_for('root'))
		#return render_template('login_template.html', status="You Logged On :-)")
	else:
		return render_template('login_template.html', status="<a href='/login?next=/login/page'>Login..!</a>")
	"""
	
@app.route('/login')
def facebook_login():
	next_url = request.args.get('next') or url_for('root')
	return facebook.authorize(callback=url_for('facebook_authorized',
		next=next_url,
		_external=True))

@app.route("/logout")
@flask_login.login_required
def logout():
	flask_login.logout_user()
	return flask.redirect(url_for('show_login_page'))
	
@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
	next_url = flask_login.request.args.get('next') or url_for('root')
	if resp is None:
		# The user likely denied the request
		flask_login.flash(u'There was a problem logging in.')
		return flask_login.redirect(next_url)
	flask_login.session['oauth_token'] = (resp['access_token'], '')
	user_data = facebook.get('/me').data
	user = User.query.filter(User.email == user_data['email']).first()
	if user is None:
		new_user = User(email=user_data['email'], first_name=user_data['first_name'], last_name=user_data['last_name'])
		db_session.add(new_user)
		db_session.commit()
		flask_login.login_user(new_user)
	else:
		flask_login.login_user(user)
	return flask_login.redirect(next_url)


# Schedule functions #
@app.route("/commit_schedule_records_changes",  methods=['POST'])	
def commit_schedule_records_changes():	
	#get json string and convert it to ScheduleRecord
	uncommitted_schedule_records = json.loads(request.get_data(), object_hook=lambda record:\
										ScheduleRecord(date=datetime.datetime.strptime(record["date"], '%Y-%m-%d').date(), status=record["status"])\
										)
	#Try to update record
	for schedule_record in uncommitted_schedule_records :
		
		num_affected_rows_from_update = ScheduleRecord.query.filter(\
				ScheduleRecord.user_id==flask_login.current_user.id,\
				ScheduleRecord.date==schedule_record.date)\
					.update(dict(\
						status=schedule_record.status\
						))
		
		if	num_affected_rows_from_update == 0:
			# Add Record
			new_schedule_record = ScheduleRecord(\
													user_id 		= flask_login.current_user.id, \
													date    	    = schedule_record.date, \
													status  	    = schedule_record.status)		
			db_session.add(new_schedule_record)
		
	db_session.commit()

	return "OK!"
		
@app.route("/get_schedule_records",  methods=['POST'])	
def get_schedule_records():		
	#import ipdb; ipdb.set_trace()
	schedule_records_serialized_list = {}
	for schedule_record in ScheduleRecord.query.filter(ScheduleRecord.user_id==flask_login.current_user.id).all():
		schedule_records_serialized_list[schedule_record.date.strftime("%Y-%m-%d").replace('-0', '-')] = schedule_record.status
		
	return json.dumps(schedule_records_serialized_list)
	
if __name__ == "__main__":
    app.run(debug=True, port=80) # Dont forget to remove DEBUG~!!