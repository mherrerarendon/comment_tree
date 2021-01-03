from ct.models.comment import Comment
from ct.models.user import User
from ct import db
from ct.core.app import create_app 
from flask import current_app
import pytest

@pytest.fixture()
def user1(request):
    db.create_all()

    def teardown():
        db.drop_all()
    request.addfinalizer(teardown)
    
    return User(username='user1')

class TestComments:
    def setup_class(self):
        if not current_app:
            app = create_app()
            app.app_context().push()
        else:
            app = current_app

    def teardown_class(self):
        pass

    def test_GetAllWorks(self, user1):
        c1 = Comment(content='testscontent', user=user1)
        db.session.add(c1)
        db.session.commit()
        assert len(Comment.query.all()) == 1

    def test_threadsAreReturnedInOrder(self, user1):
        parentComment = Comment(content='first in thread', user=user1)
        db.session.add(parentComment)
        secondComment = Comment(content='second in thread', user=user1)
        thirdComment = Comment(content='third in thread', user=user1)
        parentComment.thread.append(secondComment)
        parentComment.thread.append(thirdComment)
        db.session.commit()
        thread = parentComment.get_thread()
        assert len(thread) == 2
        assert thread[0]['content'] == 'second in thread'
        assert thread[1]['content'] == 'third in thread'

    def test_subthreadsWork(self, user1):
        parent_comment = Comment(content='parent comment', user=user1)
        db.session.add(parent_comment)
        child_comment = Comment(content='child comment', user=user1)
        parent_comment.thread.append(child_comment)
        grandchild_comment = Comment(content='grand child comment', user=user1)
        child_comment.thread.append(grandchild_comment)
        db.session.commit()
        thread = child_comment.get_thread()
        assert len(thread) == 1
        assert thread[0]['content'] == 'grand child comment'

    def test_recursiveSubthreadsWork(self, user1):
        parent_comment = Comment(content='parent comment', user=user1)
        db.session.add(parent_comment)
        child_comment = Comment(content='child comment', user=user1)
        parent_comment.thread.append(child_comment)
        grandchild_comment = Comment(content='grand child comment', user=user1)
        child_comment.thread.append(grandchild_comment)
        db.session.commit()
        thread = parent_comment.get_thread(recursive=True)
        assert thread[0]['content'] == 'child comment'
        assert thread[0]['thread'][0]['content'] == 'grand child comment'
    