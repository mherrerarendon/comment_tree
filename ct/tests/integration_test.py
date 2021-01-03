from ct.models.user import User
from ct import db
from ct.core.app import create_app 
from flask import current_app
import json
import pytest

@pytest.fixture()
def user1(request):
    print("setup")
    db.create_all()
    user1 = User(username='user1')
    db.session.add(user1)
    db.session.commit()

    def teardown():
        print("teardown")
        db.drop_all()
    request.addfinalizer(teardown)
    
    return user1

class TestIntegration:
    def setup_class(self):
        if not current_app:
            self.app = create_app()
            self.app.app_context().push()
        else:
            self.app = current_app
        
    def teardown_class(self):
        pass

    def create_thread(self, client, user1, content):
        payload = {
            "username": user1.username,
            "content": content
        }
        response = client.post(
                '/threads/thread',
                data=json.dumps(payload),
                content_type='application/json',
        )
        return response

    # def add_comment_to_thread(self, client, user1, )

    def test_simple_add_comment_works(self, user1):
        with self.app.test_client() as client:
            test_content = 'my new comment'
            response = self.create_thread(client, user1, 'my new comment')
            data = json.loads(response.data.decode())
            assert response.status_code == 201
            assert data['content'] == test_content

