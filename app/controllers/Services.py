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

# routes['POST']['/search/process'] = 'Services#search_process'   **********
	# def search_process(self):


# routes['/results/<name>'] = 'Services#result_specific'
	def result_specific(self, name):
		result = self.models['Service'].result_specific(name)
		session['show'] = result
		return redirect('/result')

# routes['/result'] = 'Services#result' **********
	def result(self):
		select = self.models['Service'].select_all()
		session['show'] = select
		return self.load_view('search_results.html', result = session['show'])

# routes['/reset'] = 'Service#reset'
	def reset(self):
		select = self.models['Service'].select_all()
		session['show'] = select
		return redirect('/result')

# routes['/update_feedback/<id>'] = 'Services#update_feedback'
	def update_feedback(self, id):
		self.models['Dashboard'].update_feedback(id)
		return redirect('/admin')

# route['/active_feedback/<id>'] = 'Services#activate_feedback'
	def activate_feedback(self, id):
		self.models['Dashboard'].activate_feedback(id)
		return redirect('/admin_feedback')


# routes['POST']['/add_feedback/service/<id>'] = 'Services#add_feedback'
	def add_feedback(self, id):
		if not 'user' in session:
			user['user_id'] = 0
			user['email'] = 'anonymous'
		else:
			user['user_id'] = session['user']['id']
			user['email'] =session['user']['email']
		self.models['Dashboard'].add_feedback(request.form.copy(), id, user)
		return redirect('service/'+id)

# routes['/service/<id>'] = 'Services#profile'
	def profile(self, id):
		profile = self.models['Service'].profile(id)
		return self.load_view('service_profile.html', profile = profile)

# routes['POST']['/add_rating/service/<id>'] = 'Services#add_rating'
	def add_rating(self, id):
		self.models['Dashboard'].add_rating(request.form.copy(), id, session['user']['id'])
		return redirect('/service/'+id)

# routes['/update/service'] = 'Services#update_service'
	def update_service(self):
		self.models['Service'].update_service(request.form.copy(), id)
		return redirect('/service/'+id)

# route['POST']['/add_service'] = 'Services#add_service'
	def add_service(self):
		add = self.models['Service'].add_service(request.form.copy())
		if add['errors']:
			for message in add['errors']:
				flash(message)
		return redirect('/admin')


# helping anthony
	def dash(self):
		pref = self.models['Service'].get_pref_for_dash(session['user']['id'])
		result = self.models['Service'].select_services(pref)
		print '***********HERE**********'
		print result
		fav = self.models['Dashboard'].select_fav(session['user']['id'])
		return self.load_view('user.html', result = result, fav = fav)
