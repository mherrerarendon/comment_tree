from ct.models.comment import Comment
from ct.models.user import User
from ct import db
from ct.core.app import create_app 

import pytest

class TestComments:
    def setup_class(self):
        app = create_app()
        app.app_context().push()
        db.create_all()
        self.user = User(username='testusername')
        db.session.add(self.user)
        db.session.commit()

    def teardown_class(self):
        db.drop_all()

    def test_GetAllWorks(self):
        c1 = Comment(content='testscontent', user=self.user)
        db.session.add(c1)
        db.session.commit()
        assert len(Comment.query.all()) == 1

    def test_GetAllWorks2(self):
        c1 = Comment(content='testscontent', user=self.user)
        db.session.add(c1)
        db.session.commit()
        assert len(Comment.query.all()) == 2

    def test_threadsAreReturnedInOrder(self):
        parentComment = Comment(content='first in thread', user=self.user)
        db.session.add(parentComment)
        secondComment = Comment(content='second in thread', user=self.user)
        thirdComment = Comment(content='third in thread', user=self.user)
        parentComment.thread.append(secondComment)
        parentComment.thread.append(thirdComment)
        db.session.commit()
        thread = parentComment.get_thread()
        assert len(thread) == 2
        assert thread[0]['content'] == 'second in thread'
        assert thread[1]['content'] == 'third in thread'

    def test_subthreadsWork(self):
        parent_comment = Comment(content='parent comment', user=self.user)
        db.session.add(parent_comment)
        child_comment = Comment(content='child comment', user=self.user)
        parent_comment.thread.append(child_comment)
        grandchild_comment = Comment(content='grand child comment', user=self.user)
        child_comment.thread.append(grandchild_comment)
        db.session.commit()
        thread = child_comment.get_thread()
        assert len(thread) == 1
        assert thread[0]['content'] == 'grand child comment'

    def test_recursiveSubthreadsWork(self):
        parent_comment = Comment(content='parent comment', user=self.user)
        db.session.add(parent_comment)
        child_comment = Comment(content='child comment', user=self.user)
        parent_comment.thread.append(child_comment)
        grandchild_comment = Comment(content='grand child comment', user=self.user)
        child_comment.thread.append(grandchild_comment)
        db.session.commit()
        thread = parent_comment.get_thread(recursive=True)
        assert thread[0]['content'] == 'child comment'
        assert thread[0]['thread'][0]['content'] == 'grand child comment'
    