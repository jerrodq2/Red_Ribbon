from system.core.model import Model

class Dashboard(Model):
	def __init__(self):
		super(Dashboard, self).__init__()

	def update_feedback(self, id):
		update = self.db.query_db('UPDATE feedback SET active = 0, updated_at = Now() WHERE id = :id', {'id': id})
		return update

	def active_feedback(self, id):
		update = self.db.query_db('UPDATE feedback SET active = 1, updated_at = Now() WHERE id = :id', {'id': id})
		return update

	def add_feedback(self, info, id, user):
		info['user_id'] = user['user_id']
		info['email'] = user['email']
		info['id'] = id
		update = self.db.query_db('INSERT INTO feedback (comment, active, user_id, service_id, email) VALUES (:comment, 1, :user_id, :id, :email)', info)
		return update

	def add_rating(self, info, id, uid):
		query = ('INSERT INTO rating (rating, comment, user_id, service_id, active, flag) VALUES (:rating, :comment, :uid, :id, 1, 0)')
		info['uid'] = uid
		info['id'] = id
		update = self.db.query_db(query, info)
		return update

	def select_fav(self, id):
		fav = self.db.query_db('SELECT s.id sid, s.name s_name, description, hours, phone, email, website, faith_based, gender_based, dependent_based, income_restriction, DATE_FORMAT(s.updated_at, "%b %d %Y %h: %i %p") s_date, req_doc, t.name FROM fav f JOIN service s ON f.service_id = s.id JOIN service_type st ON st.service_id = s.id JOIN type t ON t.id = st.type_id WHERE f.user_id = :id', {'id': id})
		return fav

	def get_feedback_by_active_status(self):
		select = "SELECT * FROM feedback WHERE active = 1 ORDER BY updated_at DESC"
		feedback = self.db.query_db(select)
		return feedback

	def get_feedback_by_inactive_status(self):
		select = "SELECT * FROM feedback WHERE active = 0 ORDER BY updated_at DESC"
		feedback = self.db.query_db(select)
		return feedback
