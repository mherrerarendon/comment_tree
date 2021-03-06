from ct import db
from ct.models.notification import Notification
from ct.models.user import User
from ct.models.comment import Comment
from ct.core.app import create_app 
from flask import current_app
import pytest

@pytest.fixture()
def users(request):
    db.create_all()
    users = []
    users.append(User(username='user1'))
    users.append(User(username='user2'))
    users.append(User(username='user3'))

    def teardown():
        db.drop_all()
    request.addfinalizer(teardown)
    
    return users

class TestNotifications:
    def setup_class(self):
        if not current_app:
            app = create_app()
            app.app_context().push()
        else:
            app = current_app
        
    def teardown_class(self):
        pass

    def test_simple_notification_works(self, users):
        user1, user2, user3 = users
        c1 = Comment(content='first', user=user1)
        db.session.add(c1)
        c2 = Comment(content='second', user=user2)
        c1.add_comment_to_thread(c2)
        Notification.create_comment_notifications(c2)
        user1Notifications = Notification.get_comment_notifications(user1.id)
        user2Notifications = Notification.get_comment_notifications(user2.id)

        # Make sure that user 1 gets notification
        assert len(user1Notifications) == 1
        assert c1.id in user1Notifications
        assert user1Notifications[c1.id][0]['id'] == c2.id

        # Make sure user 2 doesn't get notification of his own comment
        assert len(user2Notifications) == 0

    def test_subthread_comment_should_not_notify_parent_thread(self, users):
        user1, user2, user3 = users
        c1 = Comment(content='first', user=user1)
        db.session.add(c1)
        c2 = Comment(content='second', user=user2)
        c1.add_comment_to_thread(c2)
        c3 = Comment(content='third', user=user3)
        c2.add_comment_to_thread(c3)
        Notification.create_comment_notifications(c3)
        user1Notifications = Notification.get_comment_notifications(user1.id)
        user2Notifications = Notification.get_comment_notifications(user2.id)
        user3Notifications = Notification.get_comment_notifications(user3.id)

        assert len(user1Notifications) == 0
        assert len(user2Notifications) == 1
        assert len(user3Notifications) == 0
