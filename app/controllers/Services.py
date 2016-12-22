from system.core.controller import *
# for message in create['errors']:
#     flash(message, 'regis_errors')

class Services(Controller):
	def __init__(self, action):
		super(Services, self).__init__(action)
		self.load_model('Service')
		self.load_model('Dashboard')

# routes['/search'] = 'Services#index'
	def index(self):
		return self.load_view('search.html')

# routes['/results/<name>'] = 'Services#result_specific'
	def result_specific(self, name):
		result = self.models['Service'].result_specific(name)
		return self.load_view('result_specific.html', result = result)

# routes['/result'] = 'Services#result' **********
	def result(self):
		select = self.models['Service'].select_all()
		return self.load_view('search_results.html', result = select)

# routes['/results'] = 'Services#multiple_result_specific'
	def multiple_result_specific(self):
		result = self.models['Service'].multiple_result_specific(request.form.copy())
		return self.load_view('search_results.html', result = result)

# routes['/deactivate_feedback/<id>'] = 'Services#update_feedback'
	def deactivate_feedback(self, id):
		if not 'admin_status' in session['user']:
			return redirect('/result')
		self.models['Dashboard'].deactivate_feedback(id)
		return redirect('/admin')

#routes['/all_feedback/deactivate_feedback/<id>'] = 'Services#all_feedback_deactivate_feedback'
	def all_feedback_deactivate_feedback(self, id):
		if not 'admin_status' in session['user']:
			return redirect('/result')
		self.models['Dashboard'].deactivate_feedback(id)
		return redirect('/all_feedback')

# route['/activate_feedback/<id>'] = 'Services#activate_feedback'
	def activate_feedback(self, id):
		if not 'admin_status' in session['user']:
			return redirect('/result')
		self.models['Dashboard'].activate_feedback(id)
		return redirect('/all_feedback')


# routes['POST']['/add_feedback/service/<id>'] = 'Services#add_feedback'
	def add_feedback(self, id):
		if not 'user' in session:
			flash('You must be logged in to submit this form', 'feedback')
			return redirect('service/'+id)
		add = self.models['Dashboard'].add_feedback(request.form.copy(), id, session['user']['id'])
		for message in add['errors']:
			flash(message, 'feedback')
		return redirect('service/'+id)

# routes['/service/<id>'] = 'Services#profile'
	def profile(self, id):
		profile = self.models['Service'].profile(id)
		comments = self.models['Service'].comments(id)
		types = self.models['Service'].types()
		return self.load_view('service_profile.html', profile = profile, comments = comments, types = types)

# routes['POST']['/add_rating/service/<id>'] = 'Services#add_rating'
	def add_rating(self, id):
		if not 'user' in session:
			flash('You must be logged in to comment', 'comment')
			return redirect('/service/'+id)
		add = self.models['Dashboard'].add_rating(request.form.copy(), id, session['user']['id'])
		for message in add['errors']:
			flash(message, 'comment')
		return redirect('/service/'+id)

# routes['/flag/rating/<id>/<sid>'] = 'Services#flag_rating'
	def flag_rating(self, id, sid):
		if not 'user' in session:
			flash('You must be logged in to flag', 'comment')
			return redirect('/service/'+id)
		self.models['Dashboard'].flag_rating(id)
		return redirect('/service/'+sid)

# routes['/update/service/<id>'] = 'Services#update_service'
	def update_service(self, id):
		if not 'admin_status' in session['user']:
			return redirect('/service/'+id)
		update = self.models['Service'].update_service(request.form.copy(), id)
		for message in update['errors']:
			flash(message, 'update')
		return redirect('/service/'+id)

# route['POST']['/add_service'] = 'Services#add_service'
	def add_service(self):
		if not 'admin_status' in session['user']:
			return redirect('/result')
		add = self.models['Service'].add_service(request.form.copy())
		if add['errors']:
			for message in add['errors']:
				flash(message)
		return redirect('/admin')


# helping anthony
	def dash(self):
		pref = self.models['Service'].get_pref_for_dash(session['user']['id'])
		result = self.models['Service'].select_services(pref)
		fav = self.models['Dashboard'].select_fav(session['user']['id'])
		return self.load_view('user.html', result = result, favs = fav)

# routes['/add/fav/<id>'] = 'Services#add_fav'
	def add_fav(self, id):
		if not 'user' in session:
			return redirect('/login_reg')
		self.models['Dashboard'].add_fav(id, session['user']['id'])
		return redirect('/user')

# routes['/destroy/fav/<id>'] = 'Services#destroy_fav'
	def destroy_fav(self, id):
		if not 'user' in session:
			return redirect('/login_reg')
		self.models['Dashboard'].destroy_fav(id, session['user']['id'])
		return redirect('/user')

# routes['/destroy/service/<id>'] = 'Services#destroy'
	def destroy(self, id):
		if not 'admin_status' in session['user']:
			return redirect('/result')
		self.models['Service'].destroy_service(id)
		return redirect('/admin')

# route["/destroy/rating/<id>/<sid>"] = 'Services#destroy_rating'
	def destroy_rating(self, id, sid):
		if not 'admin_status' in session['user']:
			return redirect('/result')
		self.models['Service'].destroy_rating(id)
		return redirect('/service/'+sid)

# routes["/remove/flag/<id>"] = 'Services#remove_flag'
	def remove_flag(self, id):
		if not 'admin_status' in session['user']:
			return redirect('/result')
		self.models['Dashboard'].remove_flag(id)
		return redirect('/admin')

# routes["/destroy/rating/<id>"] = 'Services#destroy_rating_admin'
	def destroy_rating_admin(self, id):
		if not 'admin_status' in session['user']:
			return redirect('/result')
		self.models['Dashboard'].admin_destroy_rating(id)
		return redirect('/admin')
