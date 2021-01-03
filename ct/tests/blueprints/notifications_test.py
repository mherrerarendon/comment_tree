from ct.models.user import User
from ct import db
from ct.core.app import create_app 
from flask import current_app
import json
import pytest

@pytest.fixture()
def users(request):
    db.create_all()
    users = [
        User(username='user1'), 
        User(username='user2'), 
        User(username='user3')
    ]
    for user in users:
        db.session.add(user)
    db.session.commit()

    def teardown():
        db.drop_all()
    request.addfinalizer(teardown)

    return users

class TestNotificationBlueprints:
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
        data = json.loads(response.data.decode())
        return data['id']

    def add_comment_to_thread_with_notification(self, user1, thread_id, content):
        payload = {
            "username": user1.username,
            "content": content
        }
        with self.app.test_client() as client:
            response = client.post(
                    f'/threads/thread/{thread_id}/comment?notify=True',
                    data=json.dumps(payload),
                    content_type='application/json',
            )
        data = json.loads(response.data.decode())
        return data['id']

    def create_notifications(self, user1, user2, user3):
        thread_id = self.create_thread(user1, 'thread content')
        comment_id = self.add_comment_to_thread_with_notification(user2, thread_id, 'comment content')
        self.add_comment_to_thread_with_notification(user3, comment_id, 'subthread content')

    def get_notifications_for_user(self, user_id):
        with self.app.test_client() as client:
            response = client.get(f'/notifications/user/{user_id}')
        data = json.loads(response.data.decode())
        assert response.status_code == 200
        data = json.loads(response.data.decode())
        return data

    def test_get_notifications_for_user(self, users):
        user1, user2, user3 = users
        self.create_notifications(user1, user2, user3)
        user1_notifications = self.get_notifications_for_user(user1.id)
        user2_notifications = self.get_notifications_for_user(user2.id)
        user3_notifications = self.get_notifications_for_user(user3.id)
        assert len(user1_notifications) == 1
        assert len(user2_notifications) == 1
        assert len(user3_notifications) == 0
