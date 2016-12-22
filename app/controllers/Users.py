from system.core.controller import *
from flask import flash

class Users(Controller):
	def __init__(self, action):
		super(Users, self).__init__(action)
		self.load_model('User')
		self.load_model('Service')
		self.load_model('Dashboard')

	def index(self):
		return self.load_view('index.html')

	def login_reg(self):
		if 'user' in session:
			return redirect('/edit_user')
		return self.load_view('login_reg.html')

	def login(self):
		user = self.models['User'].get_user_by_email(request.form.copy())
		if user['status'] == True:
			session['user'] = user['user']
			if session['user']['admin_status']:
				return redirect('/admin')
			else:
				return redirect('/user')
		else:
			for message in user['errors']:
				flash(message, 'login_errors')
			return redirect('/login_reg')

	def register(self):
		result = self.models['User'].add_users(request.form.copy())
		if result['status'] == True:
			session['user'] = result['user']
			return redirect('/edit_user')
		else:
			for message in result['errors']:
				flash(message, 'regis_errors')
			return redirect('/login_reg')

	def edit(self):
		if not 'user' in session:
			return redirect('/login_reg')
		preferences = self.models['User'].get_preferences_by_id(session['user']['id'])
		if preferences['status']:
			return self.load_view('edit_user.html', preferences = preferences['pref'])
		else:
			return self.load_view('edit_user.html', preferences = {}) #so the html doesn't error out looking for the preferences dictionary

	def update_user(self):
		if not 'user' in session:
			return redirect('/login_reg')
		result = self.models['User'].update_user_by_id(session['user']['id'], request.form.copy())
		if result['status']:
			session['user']['email'] = result['result']['email']
			flash("Your information has been updated successfully", 'user_errors')
		else:
			for message in result['errors']:
				flash(message, 'user_errors')
		return redirect('/edit_user')

	def update_pref(self):
		if not 'user' in session:
			return redirect('/login_reg')
		result = self.models['User'].update_prefrences_by_id(session['user']['id'], request.form.copy())
		if result['status'] == True:
			return redirect('/user')
		else:
			flash('Preferences have been successfully update', 'pref')
			return redirect('/edit_user')

	def admin(self):
		if session['user']['admin_status'] == 0:
			return redirect('/user')
		feedback = self.models['Dashboard'].get_feedback_by_active_status()
		types = self.models['Service'].types()
		length = len(feedback)
		flags = self.models['Dashboard'].get_flagged_ratings()
		flag_length = len(flags)
		return self.load_view('admin_dash.html', feedback = feedback, types = types, length = length, flags = flags, flag_length = flag_length)

	def admin_feedback(self):
		if not 'admin_status' in session['user']:
			return redirect('/result')
		inactive = self.models['Dashboard'].get_feedback_by_inactive_status()
		active = self.models['Dashboard'].get_feedback_by_active_status()
		length = len(active)
		return self.load_view('admin_feedback.html', inactive = inactive, active = active)

	def logout(self):
		session.clear();
		return redirect('/')
