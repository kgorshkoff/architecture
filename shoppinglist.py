from app import app, db
from app.models import ItemList, User


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'ItemList': ItemList}
