from ct.models.comment import Comment
from ct import db
from ct.core.app import create_app 

import pytest

# @pytest.fixture
# def db_helper():
#     app = create_app()
#     with app.app_context():
#         db.create_all()
#     return db

# def setup_function():
#     print("  setup_function")
    

# def teardown_function():
#     print("  teardown_function")

def test_GetAllWorks():
    app = create_app()
    app.app_context().push()
    db.create_all()
    c1 = Comment(username='testusername', content='testscontent')
    db.session.add(c1)
    db.session.commit()
    assert len(Comment.query.all()) == 1