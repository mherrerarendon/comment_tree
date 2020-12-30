from ct.core.app import create_app 
from ct import db

app = create_app()
app.app_context().push()
db.create_all()
app.run(debug=True)
