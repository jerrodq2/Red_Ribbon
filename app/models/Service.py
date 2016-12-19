from system.core.model import Model

class Service(Model):
	def __init__(self):
		super(Service, self).__init__()

	def profile(self, id):
		profile = self.db.query_db('SELECT s.id sid, s.name s_name, description, hours, phone, email, website, faith_based, gender_based, dependent_based, income_restriction, DATE_FORMAT(s.updated_at, "%b %d %Y %h: %i %p") s_date, req_doc, t.name FROM service s JOIN service_type st ON st.service_id = s.id JOIN type t ON t.id = st.type_id WHERE s.id = :id', {'id': id})
		return profile[0]

	def add_service(self, info):
		# Validations
		errors = []
		if not info['service_name']:
			errors.append('Service name cannot be blank')
		if not info['description']:
			errors.append('Description name cannot be blank')
		elif len(info['description']) < 10:
			errors.append('Description must be at least 10 characters long')
		if not info['hours']:
			errors.append('Hours cannot be blank')
		if not info['faith_based']:
			errors.append('Faith Based cannot be blank')
		if not info['gender_based']:
			errors.append('Gender Based cannot be blank')
		if not info['dependent_based']:
			errors.append('Dependent Based cannot be blank')
		if not info['req_doc']:
			errors.append('Required Documents cannot be blank')
		if errors:
			return {'errors': errors}

		# First we add service
		info['name'] = info['service_name'] #So we don't have to make a new dictionary, every other input name matches
		if not info['dependent_based']:
			info['dependent_based'] = '0'
		if not info['income_restriction']:
			info['income_restriction'] = '0'
		if not info['suite']:
			info['suite'] = '0'
		print('info -> {}'.format(info))
		query = 'INSERT INTO service (name, description, hours, phone, email, website, faith_based, gender_based, dependent_based, income_restriction, req_doc) VALUES (:name, :description, :hours, :phone, :email, :website, :faith_based, :gender_based, :dependent_based, :income_restriction, :req_doc)'
		try:
			id = self.db.query_db(query, info)
		except:
			errors.append('Service name is already in database')
			return {'errors': errors}

		# If and else is to add the service type, add a new one if they entered that input or linking to an existing one
		if (info['type_name_new']):
			# incase they try to manually add a type that already exists in the DB
			check = self.db.query_db('SELECT * from type WHERE name = :type_name_new', info)
			if len(check) == 0: # then they're manually entering a new type and we don't have a problem
				tid = self.db.query_db('INSERT INTO type (name) VALUES (:type_name_new)', info)
			else:
				tid = check[0]['id']
		else:
			check = self.db.query_db('SELECT * from type WHERE name = :type_name', info)
			tid = check[0]['id']
		query = 'INSERT INTO service_type (service_id, type_id) VALUES (:id, :tid)'
		print tid
		add = self.db.query_db(query, {'id': id, 'tid': tid})
		# Now we need to add the address
		info['service_id'] = id
		self.db.query_db('INSERT INTO address (zip, suite, state, city, street, service_id) VALUES (:zip, :suite, :state, :city, :street, :service_id)', info)
		return {'errors': errors}

	def update_service(self, info):
		self.db.query_db('UPDATE service SET name = :name, description = :description, hours = :hours, phone = :phone, email = :email, website = :website, faith_based = :faith_based, gender_based = :gender_based, dependent_based = :dependent_based, income_restriction = :income_restriction, req_doc = :req_doc, updated_at = Now() WHERE id = :id',info)
		if (info['type_name_new']):
			tid = self.db.query_db('INSERT INTO type (name) VALUES (:name)', info)
		else:
			tid = self.db.query_db('SELECT id FROM type WHERE name = :name', info)
		update = self.db.query_db('UPDATE service_type SET type_id = :tid, updated_at = Now()', {'tid': tid})
		return update

	def result_specific(self, name):
		result = self.db.query_db('SELECT s.id sid, s.name s_name, description, hours, phone, email, website, faith_based, gender_based, dependent_based, income_restriction, DATE_FORMAT(s.updated_at, "%b %d %Y %h: %i %p") s_date, req_doc, t.name FROM service s JOIN service_type st ON st.service_id = s.id JOIN type t ON t.id = st.type_id WHERE :name = 1', {'name': name})
		return result
		# This route is for when they search for services with one elegibility requirement, like in the right box on page 4

	def get_pref_for_dash(self, id):
		info = self.db.query_db("SELECT * FROM preference WHERE user_id = :id", {'id': id})
		return info

	def select_services(self, info):
		if len(info) < 1:
			return []
		result = self.db.query_db('SELECT s.id sid, s.name s_name, description, hours, phone, email, website, faith_based, gender_based, dependent_based, income_restriction, DATE_FORMAT(s.updated_at, "%b %d %Y %h: %i %p") s_date, req_doc, t.name, a.zip, a.street, a.suite, a.state, a.city FROM address a JOIN service s ON a.service_id = s.id JOIN service_type st ON st.service_id = s.id JOIN type t ON t.id = st.type_id WHERE gender_based = :gender_based and faith_based = :faith_based and dependent_based = :dependent_based and income_restriction = :income_restriction', info)
		return result

	def select_all(self):
		result = self.db.query_db('SELECT a.zip, a.street, a.suite, a.state, a.city, s.id sid, s.name s_name, description, hours, phone, email, website, faith_based, gender_based, dependent_based, income_restriction, DATE_FORMAT(s.updated_at, "%b %d %Y %h: %i %p") s_date, req_doc, t.name FROM address a JOIN service s ON a.service_id = s.id JOIN service_type st ON st.service_id = s.id JOIN type t ON t.id = st.type_id')
		return result
	def types(self):
		result = self.db.query_db('SELECT * FROM type')
		return result
