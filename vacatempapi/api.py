from eve import Eve
from .sensor_manager import TempSensorManager


# API configuration
SETTINGS = {
    'DOMAIN': {
        'sensors': {
            'schema': {
                '_id': {'type': 'string', 'unique': True},
                'label': {'type': 'string', 'unique': True}
            }
        },
        'temperatures': {
            'schema': {
                'sensor': {
                    'type': 'string',
                    'data_relation': {
                        'resource': 'sensors',
                        'field': '_id',
                        'embeddable': True
                    }
                },
                'temperature': {'type': 'number'}
            }
        }
    },
    'MONGO_DBNAME': 'temperatures',
    'API_VERSION': 'v1',
    'URL_PREFIX': 'api',
    'X_DOMAINS': '*',
    'X_HEADERS': 'Origin, X-Requested-With, Content-Type, Accept, Authorization, If-Match',
    'X_ALLOW_CREDENTIALS': True,
    'HATEOAS': False,
    'TRANSPARENT_SCHEMA_RULES': True,
    'DATE_FORMAT': '%Y-%m-%d %H:%M:%S',
    'ITEM_METHODS': ['GET', 'PATCH', 'DELETE'],
    'RESOURCE_METHODS': ['GET']
}


def create_app():
    '''Cria uma aplicação Eve.'''
    app = Eve(settings=SETTINGS)
    # Create sensor manager object
    with app.app_context():
        manager = TempSensorManager(app.data.driver.db)
        manager.list_sensors()
        manager.start()
    return app
