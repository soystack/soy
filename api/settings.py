SERVER_NAME = '127.0.0.1:5000'

SCHEMA = {
	'user': {
		'type': 'string',
		'minlength': 5,
		'maxlength': 55,
		'required': True
	},
	'host': {
		'type': 'string',
		'required': True,
		'unique': True
	}
}

nginx_create = {
	'item_title': 'create host',
	'cache_control': 'max-age=10,must-revalidate',
	'resource_methods': ['GET'],
	'schema': SCHEMA
}
		

DOMAIN = {
	'nginx_create': nginx_create,
}

MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_USERNAME = 'root'
MONGO_PASSWORD = 'rootpass'
MONGO_DBNAME = 'api'
