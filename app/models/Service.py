from system.core.model import Model
import re

class Service(Model):
	def __init__(self):
		super(Service, self).__init__()

	def profile(self, id):
		profile = self.db.query_db('SELECT s.id sid, s.name s_name, description, hours, phone, email, website, faith_based, gender_based, dependent_based, income_restriction, DATE_FORMAT(s.updated_at, "%b %d %Y %h: %i %p") s_date, req_doc, documents, img_url, num_of_dependents, t.name, a.zip, a.street, a.suite, a.state, a.city FROM address a JOIN service s ON a.service_id = s.id JOIN service_type st ON st.service_id = s.id JOIN type t ON t.id = st.type_id WHERE s.id = :id', {'id': id})
		return profile[0]

	def comments(self, id):
		comments = self.db.query_db('SELECT rating, comment, r.user_id uid, flag, r.id id, alias FROM rating r JOIN user u ON r.user_id = u.id WHERE service_id = :id', {'id': id})
		return comments

	def add_service(self, info):
		# Validations
		errors = []
		EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
		phone_regex = re.compile(r'\((\d{3})\)\d{3}-\d{4}')

		if not info['name']:
			errors.append('Service name cannot be blank')
		if not info['type_name'] and not info['type_name_new']:
			errors.append('Must select a type of service or enter new one')
		if not info['description']:
			errors.append('Description cannot be blank')
		elif len(info['description']) < 10:
			errors.append('Description must be at least 10 characters long')
		if not info['hours']:
			errors.append('Hours cannot be blank')
		if not info['phone']:
			errors.append('Phone number cannot be blank')
		elif len(info['phone']) != 13:
			errors.append('Phone number must be in (123)456-7890 format')
		elif not phone_regex.match(info['phone']):
			errors.append('Phone number must be in (123)456-7890 format')
		if not info['email']:
			errors.append('Email cannot be blank')
		elif not EMAIL_REGEX.match(info['email']):
			errors.append('Email format must be valid')
		elif info['email'] != info['conf_email']:
			errors.append('Email must match Confirm Email')
		if not info['faith_based']:
			errors.append('Faith Based cannot be blank')
		if not info['gender_based']:
			errors.append('Gender Based cannot be blank')
		if not info['dependent_based']:
			errors.append('Dependent Based cannot be blank')
		if not info['req_doc']:
			errors.append('Required Documents cannot be blank')
		if not info['street']:
			errors.append('Street Address cannot be blank')
		if not info['state']:
			errors.append('State cannot be blank')
		elif len(info['state']) != 2:
			errors.append('State must be 2 characters long')
		if not info['city']:
			errors.append('City cannot be blank')
		if not info['zip']:
			errors.append('Zipcode cannot be blank')
		elif len(info['zip']) < 5:
			errors.append('Zipcode must be at least 5 characters long')
		try:
			val = int(info['zip'])
		except:
			errors.append('Zipcode must be a number')
		if errors:
			return {'errors': errors}

		if not info['income_restriction']:
			info['income_restriction'] = 0
		if not info['suite']:
			info['suite'] = 0
		if not info['num_of_dependents']:
			info['num_of_dependents'] = 0
		info['state'] = info['state'].upper()
		# First we add service
		query = 'INSERT INTO service (name, description, hours, phone, email, website, faith_based, gender_based, dependent_based, income_restriction, req_doc, documents, img_url, num_of_dependents) VALUES (:name, :description, :hours, :phone, :email, :website, :faith_based, :gender_based, :dependent_based, :income_restriction, :req_doc, :documents, :img_url, :num_of_dependents)'
		try:
			id = self.db.query_db(query, info)
		except:
			errors.append('There was an error, Service name, Phone number, or Email may already in use')
			return {'errors': errors}

		# If and else is to add the service type, add a new one if they entered that input or linking to an existing one
		if info['type_name_new']:
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
		add = self.db.query_db(query, {'id': id, 'tid': tid})

		# Now we need to add the address
		info['service_id'] = id
		self.db.query_db('INSERT INTO address (zip, suite, state, city, street, service_id) VALUES (:zip, :suite, :state, :city, :street, :service_id)', info)
		return {'errors': errors}

	def update_service(self, info, id):
		# START VALIDATIONS
		errors = []
		EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
		phone_regex = re.compile(r'\((\d{3})\)\d{3}-\d{4}')

		if not info['name']:
			errors.append('Service name cannot be blank')
		if not info['type_name'] and not info['type_name_new']:
			errors.append('Must select a type of service or enter new one')
		if not info['description']:
			errors.append('Description cannot be blank')
		elif len(info['description']) < 10:
			errors.append('Description must be at least 10 characters long')
		if not info['hours']:
			errors.append('Hours cannot be blank')
		if not info['phone']:
			errors.append('Phone number cannot be blank')
		elif len(info['phone']) != 13:
			errors.append('Phone number must be in (123)456-7890 format')
		elif not phone_regex.match(info['phone']):
			errors.append('Phone number must be in (123)456-7890 format')
		if not info['email']:
			errors.append('Email cannot be blank')
		elif not EMAIL_REGEX.match(info['email']):
			errors.append('Email format must be valid')
		if not info['faith_based']:
			errors.append('Faith Based cannot be blank')
		if not info['gender_based']:
			errors.append('Gender Based cannot be blank')
		if not info['dependent_based']:
			errors.append('Dependent Based cannot be blank')
		if not info['req_doc']:
			errors.append('Required Documents cannot be blank')
		if not info['street']:
			errors.append('Street Address cannot be blank')
		if not info['state']:
			errors.append('State cannot be blank')
		elif len(info['state']) != 2:
			errors.append('State must be 2 characters long')
		if not info['city']:
			errors.append('City cannot be blank')
		if not info['zip']:
			errors.append('Zipcode cannot be blank')
		elif len(info['zip']) < 5:
			errors.append('Zipcode must be at least 5 characters long')
		try:
			val = int(info['zip'])
		except:
			errors.append('Zipcode must be a number')
		if errors:
			return {'errors': errors}
		# END VALIDATIONS

		if not info['income_restriction']:
			info['income_restriction'] = 0
		if not info['suite']:
			info['suite'] = 0
		if not info['num_of_dependents']:
			info['num_of_dependents'] = 0
		info['state'] = info['state'].upper()
		info['service_id'] = id
		try:
			self.db.query_db('UPDATE service SET name = :name, description = :description, hours = :hours, phone = :phone, email = :email, website = :website, faith_based = :faith_based, gender_based = :gender_based, dependent_based = :dependent_based, income_restriction = :income_restriction, req_doc = :req_doc, documents = :documents, img_url = :img_url, num_of_dependents= :num_of_dependents, updated_at = Now() WHERE id = :service_id',info)
		except:
			errors.append('There was an error, Service name, Phone number, or Email is already in use')
			return {'errors': errors}
		# END SERVICE UPDATE
		# START TYPE UPDATE
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
		update = self.db.query_db('UPDATE service_type SET type_id = :tid, updated_at = Now() WHERE service_id = :id', {'tid': tid, 'id': id})
		# END TYPE UPDATE
		# START ADDRESS UPDATE
		self.db.query_db('UPDATE address SET zip = :zip, street = :street, suite = :suite, state = :state, city = :city, updated_at = NOW() WHERE service_id = :service_id', info)
		# END ADDRESS UPDATE
		errors.append('Information successfully updated')
		return {'errors': errors}


	def recommend(self, info):
		errors = []
		EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
		phone_regex = re.compile(r'\((\d{3})\)\d{3}-\d{4}')

		if not info['name']:
			errors.append('Service name cannot be blank')
		if info['user_email']:
			if not EMAIL_REGEX.match(info['user_email']):
				errors.append('Your personal email format must be valid')
		if info['email']:
			if not EMAIL_REGEX.match(info['email']):
				errors.append('Service email format must be valid')
		if info['phone']:
			if not phone_regex.match(info['phone']):
				errors.append('Phone number must be in (123)456-7890 format')
		if not info['description']:
			errors.append('Description cannot be blank')
		elif len(info) < 10:
			errors.append('Description must be at least 10 characters long')

		if errors:
			return {'errors': errors, 'type': 'errors'}

		query = 'INSERT INTO recommended_service (user_name, user_email, name, email, website, phone, hours, address, description, additional) VALUES (:user_name, :user_email, :name, :email, :website, :phone, :hours, :address, :description, :additional)'
		try:
			self.db.query_db(query, info)
		except:
			errors.append('There was an error, Service name, Phone number, or Email may already in use')
			return {'errors': errors, 'type': 'errors'}
		errors.append('Recommendation successfully sent, we will look into this service soon, thank you for you help.')
		return {'errors': errors, 'type': 'success'}


	def result_specific(self, name):
		if name == 'income_based':
			str = 'income_restriction != 0'
		else:
			str = name + ' = 1'
		result = self.db.query_db("SELECT s.id sid, s.name s_name, description, hours, phone, email, website, faith_based, gender_based, dependent_based, income_restriction, DATE_FORMAT(s.updated_at, '%b %d %Y %h: %i %p') s_date, req_doc, documents, img_url, num_of_dependents, t.name, a.zip, a.street, a.suite, a.state, a.city FROM address a JOIN service s ON a.service_id = s.id JOIN service_type st ON st.service_id = s.id JOIN type t ON t.id = st.type_id WHERE " + str)
		return result
		# This route is for when they search for services with one elegibility requirement, like in the right box on page 4

	def multiple_result_specific(self, info):
		if info['income_restriction'] == '1':
			str = ' income_restriction > 0'
		else:
			str = ' income_restriction = 0'
		result = self.db.query_db('SELECT s.id sid, s.name s_name, description, hours, phone, email, website, faith_based, gender_based, dependent_based, income_restriction, DATE_FORMAT(s.updated_at, "%b %d %Y %h: %i %p") s_date, req_doc, documents, img_url, num_of_dependents, t.name, a.zip, a.street, a.suite, a.state, a.city FROM address a JOIN service s ON a.service_id = s.id JOIN service_type st ON st.service_id = s.id JOIN type t ON t.id = st.type_id WHERE gender_based = :gender_based and faith_based = :faith_based and req_doc = :req_doc and dependent_based = :dependent_based and' + str, info)
		return result

	def get_pref_for_dash(self, id):
		info = self.db.query_db("SELECT * FROM preference WHERE user_id = :id", {'id': id})
		return info

	def select_services(self, info):
		if len(info) < 1:
			return []
		result = self.db.query_db('SELECT s.id sid, s.name s_name, description, hours, phone, email, website, faith_based, gender_based, dependent_based, income_restriction, DATE_FORMAT(s.updated_at, "%b %d %Y %h: %i %p") s_date, req_doc, documents, img_url, num_of_dependents, t.name, a.zip, a.street, a.suite, a.state, a.city FROM address a JOIN service s ON a.service_id = s.id JOIN service_type st ON st.service_id = s.id JOIN type t ON t.id = st.type_id WHERE gender_based = :gender_based and faith_based = :faith_based and dependent_based = :dependent_based and income_restriction = :income_restriction', info)
		return result

	def select_all(self):
		result = self.db.query_db('SELECT a.zip, a.street, a.suite, a.state, a.city, s.id sid, s.name s_name, description, hours, phone, email, website, faith_based, gender_based, dependent_based, income_restriction, DATE_FORMAT(s.updated_at, "%b %d %Y %h: %i %p") s_date, req_doc, documents, img_url, num_of_dependents, t.name FROM address a JOIN service s ON a.service_id = s.id JOIN service_type st ON st.service_id = s.id JOIN type t ON t.id = st.type_id')
		return result

	def types(self):
		result = self.db.query_db('SELECT * FROM type')
		return result

	def get_recommendations(self):
		result = self.db.query_db('SELECT * FROM recommended_service')
		return result

	def destroy_recommendation(self, id):
		destroy = self.db.query_db('DELETE FROM recommended_service WHERE id = :id', {'id': id})
		return destroy

	def destroy_service(self, id):
		data = {'id': id}
		self.db.query_db('DELETE FROM address WHERE service_id = :id', data)
		self.db.query_db('DELETE FROM service_type WHERE service_id = :id', data)
		self.db.query_db('DELETE FROM rating WHERE service_id = :id', data)
		self.db.query_db('DELETE FROM feedback WHERE service_id = :id', data)
		self.db.query_db('DELETE FROM fav WHERE service_id = :id', data)
		final = self.db.query_db('DELETE FROM service WHERE id = :id', data)
		return final

	def destroy_rating(self, id):
		delete = self.db.query_db('DELETE FROM rating WHERE id = :id', {'id': id})
		return delete

	def check_rating(self, id, uid):
		check = self.db.query_db('SELECT user_id FROM rating WHERE id = :id', {'id': id})
		if check[0]['user_id'] == uid:
			return True
		return False

	def ratings(self):
		ratings = self.db.query_db("SELECT s.id sid, ROUND(AVG(rating)) rating FROM rating r JOIN service s ON r.service_id = s.id GROUP BY s.id")
		return ratings

	def single_rating(self, id):
		rating = self.db.query_db("SELECT ROUND(AVG(rating)) rating FROM rating r WHERE r.service_id = :id GROUP BY r.service_id ", {'id': id})
		return rating
