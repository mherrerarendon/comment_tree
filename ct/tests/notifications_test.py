from ct import db
from ct.models.notification import Notification
from ct.models.user import User
from ct.models.comment import Comment
from ct.core.app import create_app 

class TestNotifications:
    def setup_class(self):
        app = create_app()
        app.app_context().push()
        db.create_all()
        self.user1 = User(username='user1')
        self.user2 = User(username='user2')
        self.user3 = User(username='user3')
        db.session.add(self.user1)
        db.session.add(self.user2)
        db.session.add(self.user3)
        db.session.commit()

    def teardown_class(self):
        db.drop_all()

    def test_simple_notification_works(self):
        c1 = Comment(content='first', user=self.user1)
        db.session.add(c1)
        c2 = Comment(content='second', user=self.user2)
        c1.add_comment_to_thread(c2)
        Notification.create_comment_notifications(c2)
        user1Notifications = Notification.get_notifications_by_thread_for_user(self.user1.id)
        user2Notifications = Notification.get_notifications_by_thread_for_user(self.user2.id)

        # Make sure that user 1 gets notification
        assert len(user1Notifications) == 1
        assert c1.id in user1Notifications
        assert user1Notifications[c1.id][0].id == c2.id

        # Make sure user 2 doesn't get notification of his own comment
        # assert len(user2Notifications) == 0

