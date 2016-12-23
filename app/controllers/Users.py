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

# routes['/users'] = 'Users#all_users'
	def all_users(self):
		if session['user']['admin_status'] == 0:
			return redirect('/')
		users = self.models['User'].all_users()
		admins = self.models['User'].admins()
		return self.load_view('users.html', users = users, admins = admins)

# routes["/destroy/user/<id>"]
	def destroy_user(self, id):
		if session['user']['admin_status'] == 0:
			return redirect('/')
		self.models['User'].destroy_user(id)
		return redirect('/all_users')

# routes["/create/admin/<id>"] = 'Users#upgrade_status'
	def upgrade_status(self, id):
		if session['user']['admin_status'] == 0:
			return redirect('/')
		self.models['User'].upgrade_status(id)
		return redirect('/all_users')

# routes["/destroy/admin/<id>"] = 'Users#revoke_status'
	def revoke_status(self, id):
		if session['user']['admin_status'] == 0:
			return redirect('/')
		if session['user']['id'] == int(id):
			flash('Cannot revoke your own status')
			return redirect("/all_users")
		revoke = self.models['User'].revoke_status(id)
		if revoke['error']:
			flash(revoke['error'])
		return redirect('/all_users')

	def admin(self):
		if session['user']['admin_status'] == 0:
			return redirect('/user')
		feedback = self.models['Dashboard'].get_feedback_by_active_status()
		types = self.models['Service'].types()
		length = len(feedback)
		flags = self.models['Dashboard'].get_flagged_ratings()
		flag_length = len(flags)
		support = self.models['User'].active_support()
		support_length = len(support)
		return self.load_view('admin_dash.html', feedback = feedback, types = types, length = length, flags = flags, flag_length = flag_length, support = support, support_length = support_length)

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

# routes['/support'] = 'Users#support'
	def support(self):
		return self.load_view('support.html')
# routes['POST']['/create/support'] = 'Users#create_support'
	def create_support(self):
		create = self.models['User'].support(request.form.copy())
		for message in create['errors']:
			flash(message, create['type'])
		return redirect('/support')

# routes['/all_support'] = 'Users#all_support'
	def all_support(self):
		active = self.models['User'].active_support()
		archived = self.models['User'].archived_support()
		return self.load_view('/archive_support.html', active = active, archived = archived)

# routes["/archive/support/{{i['id']}}"] = 'Users#deactivate_support'
	def deactivate_support(self, id):
		self.models['User'].deactivate_support(id)
		return redirect('/admin')

# routes["/activate/support/<id>"] = 'Users#activate_support'
	def activate_support(self, id):
		self.models['User'].activate_support(id)
		return redirect('/all_support')

# routes["/archive/deactivate/support/<id>"] = 'Users#archive_deactivate_support'
	def archive_deactivate_support(self, id):
		self.models['User'].deactivate_support(id)
		return redirect('/all_support')

# routes["/destroy/support/<id>"] = 'Users#destroy_support'
	def destroy_support(self, id):
		self.models['User'].destroy_support(id)
		return redirect('/all_support')
