from system.core.model import Model

class Dashboard(Model):
	def __init__(self):
		super(Dashboard, self).__init__()

	def add_fav(self, id, uid):
		data = {'uid': uid, 'id': id}
		check = self.db.query_db('SELECT * FROM fav WHERE service_id = :id and user_id = :uid', data)
		if len(check) > 0:
			return check
		add = self.db.query_db("INSERT INTO fav (user_id, service_id) VALUES (:uid, :id)", data)
		return add

	def destroy_fav(self, id, uid):
		data = {'uid': uid, 'id': id}
		delete = self.db.query_db('DELETE FROM fav WHERE service_id = :id and user_id = :uid', data)
		return delete

	def update_feedback(self, id):
		update = self.db.query_db('UPDATE feedback SET active = 0, updated_at = Now() WHERE id = :id', {'id': id})
		return update

	def active_feedback(self, id):
		update = self.db.query_db('UPDATE feedback SET active = 1, updated_at = Now() WHERE id = :id', {'id': id})
		return update

	def add_feedback(self, info, id, uid):
		errors = []
		if not info['comment']:
			errors.append('Form cannot be blank')
		elif len(info['comment']) < 10:
			errors.append('Form must be at least 10 characters long')
		if errors:
			return {'errors': errors}
		info['id'] = id
		info['uid'] = uid
		update = self.db.query_db('INSERT INTO feedback (comment, active, user_id, service_id) VALUES (:comment, 1, :uid, :id)', info)
		errors.append('Feedback sent')
		return {'errors': errors}

	def add_rating(self, info, id, uid):
		errors = []
		if not info['rating']:
			errors.append('Rating cannot be blank')
		if not info['comment']:
			errors.append('Comment cannot be blank')
		elif len(info['comment']) < 10:
			errors.append('Comment must be at least 10 characters long')
		if errors:
			return {'errors': errors}
		query = ('INSERT INTO rating (rating, comment, user_id, service_id, active, flag) VALUES (:rating, :comment, :uid, :id, 1, 0)')
		info['uid'] = uid
		info['id'] = id
		update = self.db.query_db(query, info)
		return {'errors': errors}

	def flag_rating(self, id):
		sid = self.db.query_db('UPDATE rating SET flag = 1 WHERE id = :id', {'id': id})
		return sid

	def select_fav(self, id):
		fav = self.db.query_db('SELECT s.id sid, s.name s_name, description, hours, phone, email, website, faith_based, gender_based, dependent_based, income_restriction, DATE_FORMAT(s.updated_at, "%b %d %Y %h: %i %p") s_date, req_doc, documents, t.name, a.zip, a.street, a.suite, a.state, a.city FROM fav f JOIN service s ON f.service_id = s.id JOIN service_type st ON st.service_id = s.id JOIN type t ON t.id = st.type_id JOIN address a ON a.service_id = s.id WHERE f.user_id = :id', {'id': id})
		return fav

	def get_feedback_by_active_status(self):
		select = "SELECT * FROM feedback WHERE active = 1 ORDER BY updated_at DESC"
		feedback = self.db.query_db(select)
		return feedback

	def get_feedback_by_inactive_status(self):
		select = "SELECT * FROM feedback WHERE active = 0 ORDER BY updated_at DESC"
		feedback = self.db.query_db(select)
		return feedback
