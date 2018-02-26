from models import connect_engine
from sqlalchemy.sql import and_, or_, not_

connection = connect_engine.connect()