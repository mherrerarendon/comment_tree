from ct.models.user import User
from ct import db
from ct.core.app import create_app 
from flask import current_app
import json
import pytest

@pytest.fixture()
def user1(request):
    db.create_all()
    user1 = User(username='user1')
    db.session.add(user1)
    db.session.commit()

    def teardown():
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

    def create_thread(self, user1, content):
        payload = {
            "username": user1.username,
            "content": content
        }
        with self.app.test_client() as client:
            response = client.post(
                    '/threads/thread',
                    data=json.dumps(payload),
                    content_type='application/json',
            )
        return response

    def add_comment_to_thread(self, user1, thread_id, content):
        payload = {
            "username": user1.username,
            "content": content
        }
        with self.app.test_client() as client:
            response = client.post(
                    f'/threads/thread/{thread_id}/comment',
                    data=json.dumps(payload),
                    content_type='application/json',
            )
        return response

    def test_create_thread(self, user1):
        test_content = 'my new comment'
        response = self.create_thread(user1, test_content)
        data = json.loads(response.data.decode())
        assert response.status_code == 201
        assert data['content'] == test_content

    def test_get_thread(self, user1):
        test_content = 'thread comment'
        data = json.loads(self.create_thread(user1, test_content).data.decode())
        thread_id = data['id']
        with self.app.test_client() as client:
            response = client.get(
                    f'/threads/thread/{thread_id}'
            )
        data = json.loads(response.data.decode())
        assert response.status_code == 200
        assert data['comment']['content'] == test_content

    def test_append_comment_to_thread(self, user1):
        data = json.loads(self.create_thread(user1, 'thread comment').data.decode())
        test_content = 'comment in thread'
        thread_id = data['id']
        response = self.add_comment_to_thread(user1, thread_id, test_content)
        assert response.status_code == 201