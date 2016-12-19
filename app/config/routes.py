from system.core.router import routes

# User-login GET routes
routes['default_controller'] = 'Users'
routes['/login_reg'] = 'Users#login_reg'
routes['/logout'] = 'Users#logout'

# User-login POST routes
routes['POST']['/login'] = 'Users#login'
routes['POST']['/register'] = 'Users#register'

# User dashboard routes
routes['/user'] = 'Services#dash'
routes['/edit_user'] = 'Users#edit'
routes['POST']['/update_user/pref'] = 'Users#update_pref'
routes['POST']['/update_user'] = 'Users#update_user'

# Searching & results routes
routes['/search'] = 'Services#index'
routes['/result'] = 'Services#result'
routes['/results/<name>'] = 'Services#result_specific'
routes['/reset'] = 'Services#reset'
routes['POST']['/search/process'] = 'Services#search_process'
routes['POST']['/add_rating/service/<id>'] = 'Services#add_rating'

# Single service view
routes['/service/<id>'] = 'Services#profile'

# Admin routes
routes['/admin'] = 'Users#admin'
routes['/update/service/<id>'] = 'Services#update_service'
routes['POST']['/add_service'] = 'Services#add_service'

# Feedback routes - ignore untill implemented
routes['/all_feedback'] = 'Users#admin_feedback'
routes['/update_feedback/<id>'] = 'Services#update_feedback'
routes['/active_feedback/<id>'] = 'Services#activate_feedback'
routes['POST']['/add_feedback/service/<id>'] = 'Services#add_feedback'