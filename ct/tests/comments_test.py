from ct.models.comment import Comment
from ct import db
from ct.core.app import create_app 

import pytest

@pytest.fixture
def test_db():
    app = create_app()
    app.app_context().push()
    db.create_all()
    return db

def test_GetAllWorks(test_db):
    c1 = Comment(username='testusername', content='testscontent')
    test_db.session.add(c1)
    test_db.session.commit()
    assert len(Comment.query.all()) == 1

def test_GetAllWorks2(test_db):
    c1 = Comment(username='testusername2', content='testscontent')
    test_db.session.add(c1)
    test_db.session.commit()
    assert len(Comment.query.all()) == 2

def test_threadsAreReturnedInOrder(test_db):
    parentComment = Comment(username='marco', content='first in thread')
    test_db.session.add(parentComment)
    secondComment = Comment(username='marco', content='second in thread')
    thirdComment = Comment(username='marco', content='third in thread')
    parentComment.thread.append(secondComment)
    parentComment.thread.append(thirdComment)
    test_db.session.commit()
    thread = parentComment.get_thread()
    assert len(thread) == 2
    assert thread[0]['content'] == 'second in thread'
    assert thread[1]['content'] == 'third in thread'
    