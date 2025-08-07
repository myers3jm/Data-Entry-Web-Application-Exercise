# Author:   Jared Myers
# Date:     08.07.2025
from api import app, db

with app.app_context():
    db.create_all()