from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from web_app.producer import MessageProducer
from web_app.config import DevelopmentConfig


migrate = Migrate()
db = SQLAlchemy()
message_producer = MessageProducer(DevelopmentConfig)
