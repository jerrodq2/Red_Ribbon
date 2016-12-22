from system.core.router import routes

# User-login GET routes
routes['default_controller'] = 'Users'
routes['/login_reg'] = 'Users#login_reg'
routes['/logout'] = 'Users#logout'

# User-login POST routes
routes['POST']['/login'] = 'Users#login'
routes['POST']['/register'] = 'Users#register'

# User routes
routes['/user'] = 'Services#dash'
routes['/edit_user'] = 'Users#edit'
routes['/support'] = 'Users#support'
routes['POST']['/create/support'] = 'Users#create_support'
routes['POST']['/update_user/pref'] = 'Users#update_pref'
routes['POST']['/update_user'] = 'Users#update_user'

# Searching & results routes
routes['/search'] = 'Services#index'
routes['/result'] = 'Services#result'
routes['/result/<name>'] = 'Services#result_specific'
routes['/add/fav/<id>'] = 'Services#add_fav'
routes['/destroy/fav/<id>'] = 'Services#destroy_fav'
routes['/flag/rating/<id>/<sid>'] = 'Services#flag_rating'
routes['POST']['/results'] = 'Services#multiple_result_specific'
routes['POST']['/add_rating/service/<id>'] = 'Services#add_rating'



# Single service view
routes['/service/<id>'] = 'Services#profile'

# Admin routes
routes['/admin'] = 'Users#admin'
routes['/destroy/service/<id>'] = 'Services#destroy'
routes["/destroy/rating/<id>/<sid>"] = 'Services#destroy_rating'
routes["/destroy/rating/<id>"] = 'Services#destroy_rating_admin'
routes["/remove/flag/<id>"] = 'Services#remove_flag'
routes["/deactivate/support/<id>"] = 'Users#deactivate_support'
routes['/all_support'] = 'Users#all_support'
routes["/activate/support/<id>"] = 'Users#activate_support'
routes["/archive/deactivate/support/<id>"] = 'Users#archive_deactivate_support'
routes['POST']['/update/service/<id>'] = 'Services#update_service'
routes['POST']['/add_service'] = 'Services#add_service'

# Feedback routes
routes['/all_feedback'] = 'Users#admin_feedback'
routes['/deactivate_feedback/<id>'] = 'Services#deactivate_feedback'
routes['/all_feedback/deactivate_feedback/<id>'] = 'Services#all_feedback_deactivate_feedback'
routes['/activate_feedback/<id>'] = 'Services#activate_feedback'
routes['POST']['/add_feedback/service/<id>'] = 'Services#add_feedback'
