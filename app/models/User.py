from system.core.model import Model
import re
EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')

class User(Model):
    def __init__(self):
        super(User, self).__init__()

    def get_user_by_email(self, users):
        errors = []
        if not users['email1']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(users['email1']):
            errors.append('Email format must be valid!')
        if not users['password1']:
            errors.append('Password cannot be blank')
        if errors:
            return {'status' : False, 'errors' :errors}

        user_query = "SELECT * FROM user WHERE email = :email LIMIT 1"
        data = { 'email' : users['email1'] }
        user = self.db.query_db(user_query, data)
        if len(user) == 0: #then that email wasn't found in the db
            errors.append('Email not found')
            return {'status' : False, 'errors' :errors}
 # same as query_db() but returns one result
        if self.bcrypt.check_password_hash(user[0]['password'], users['password1']):
             # check_password_hash() compares encrypted password in DB to one provided by user logging in
            return_user = self.db.query_db("SELECT id, alias, email, admin_status, gender, dependent, faith, income FROM user WHERE email = :email", data) # so we select what gets put into session, such not putting the password into the session.
            return {'status' : True, 'user' : return_user[0]}
        else:
            errors.append('Invalid password')
            return { 'status' : False, 'errors' : errors }

    def add_users(self, users):
        errors = []

        if not users['alias']:
            errors.append('Alias cannot be blank')
        elif len(users['alias']) < 2:
            errors.append('Alias must be at least 2 characters long')
        if not users['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(users['email']):
            errors.append('Email format must be valid!')
        if not users['password']:
            errors.append('Password cannot be blank')
        elif len(users['password']) < 8:
            errors.append('Password must be at least 8 characters long')
        elif users['password'] != users['con_password']:
            errors.append('Password and confirmation must match!')
        if errors:
            return {'status' : False, 'errors': errors}
        else:
            data = {
                'alias': users['alias'],
                'email' : users['email'],
                'password' : self.bcrypt.generate_password_hash(users['password'])
                }
            check = self.db.query_db("SELECT * FROM user")
            if len(check) == 0:
                data['admin_status'] = 1
            else:
                data['admin_status'] = 0
            query = "INSERT INTO user (alias, email, password, admin_status) VALUES (:alias, :email, :password, :admin_status)"

            try:
                result = self.db.query_db(query, data)
            except Exception as e:
                errors.append('Email or Alias already in use')
                return { 'status' : False, 'errors' : errors }
            user = self.db.query_db("SELECT id, alias, email, admin_status FROM user WHERE id = :id", {'id': result})
            return {'status' : True, 'user' : user[0]}

    def get_preferences_by_id(self, id):
        user_pref = self.db.query_db("SELECT * FROM preference WHERE user_id = :id", {'id' : id})
        if len(user_pref) > 0:
            return {'status': True, 'pref': user_pref[0]}
        else:
            return {'status': False}

    def update_user_by_id(self, id, users):
        errors = []
        if not users['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(users['email']):
            errors.append('Email format must be valid!')
        if not users['old_password']:
            errors.append('You must enter your old password')
        if users['password'] != users['con_password']:
            errors.append('New Password and Confirm New Password must match')
        if errors:
            return {'status': False, 'errors' : errors}

        check = self.db.query_db('SELECT * FROM user WHERE id = :id', {'id': id})
        if not self.bcrypt.check_password_hash(check[0]['password'], users['old_password']):
            errors.append('Old Password is incorrect')
            return {'status': False, 'errors' : errors}
        else:
            if users['password']: # so they don't have to change the password
                update = "UPDATE user SET email = :email, password = :password WHERE id = :id"
                data = {
                'id': id,
                'email' : users['email'],
                'password': self.bcrypt.generate_password_hash(users['password']),
                }
            else:
                update = "UPDATE user SET email = :email WHERE id = :id"
                data = {
                'id': id,
                'email' : users['email'],
                }
            try:
                result = self.db.query_db(update, data)
            except Exception as e:
                errors.append('Email is already in use')
                return {'status': False, 'errors' : errors}
            user = self.db.query_db("SELECT email FROM user WHERE id = :id", {'id': id})# so we can update the email in the session
            return {'status' : True, 'result' : user[0]}

    def update_prefrences_by_id(self, id, form_data):
        check = self.db.query_db('SELECT * FROM preference WHERE user_id = :id', {'id': id})
        data = {
        'gender' : form_data['gender'],
        'dependent' : form_data['dependent'],
        'faith' : form_data['faith'],
        'income' : form_data['income'],
        'id' : id
        }
        if len(check) == 0: #user currently has no preferences then
            self.db.query_db('INSERT INTO preference (user_id, gender_based, dependent_based, faith_based, income_restriction) VALUES (:id, :gender, :dependent, :faith, :income)', data)
            return {'status': True}
        else:
            update = "UPDATE preference SET gender_based = :gender, dependent_based = :dependent, faith_based = :faith, income_restriction = :income WHERE user_id = :id"
            self.db.query_db(update, data)
            return {'status' : False}

    def support(self, info):
        errors = []

        if not info['message']:
            errors.append('Message cannot be empty')
        elif len(info['message']) < 10:
            errors.append('Message must be at least 10 characters long')
        if info['email']: # email is optional, so the check for format is as well
            if not EMAIL_REGEX.match(info['email']):
                errors.append('Email format must be valid')
        if errors:
            return {'errors': errors, 'type': 'error'}

        self.db.query_db('INSERT INTO support (message, email) VALUES (:message, :email)', info)
        errors.append('Your message has been sent, Administrators will review it shortly, thank you for your feedback')
        return {'errors': errors, 'type': 'success'}

    def active_support(self):
        support = self.db.query_db("SELECT * FROM support WHERE active = 1")
        return support

    def archived_support(self):
        support = self.db.query_db("SELECT * FROM support WHERE active = 0")
        return support

    def deactivate_support(self, id):
        support = self.db.query_db('UPDATE support SET active = 0 WHERE id = :id', {'id': id})
        return support

    def activate_support(self, id):
        support = self.db.query_db('UPDATE support SET active = 1 WHERE id = :id', {'id': id})
        return support

    def destroy_support(self, id):
        destroy = self.db.query_db('DELETE FROM support WHERE id = :id', {'id': id})
        return destroy
