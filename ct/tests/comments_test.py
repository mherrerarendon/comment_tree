from ct.models.comment import Comment
from ct.models.thread import Thread
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
    thread = Thread()
    c1 = Comment(username='testusername', content='testscontent', thread=thread)
    test_db.session.add(c1)
    test_db.session.commit()
    assert len(Comment.query.all()) == 1

def test_GetAllWorks2(test_db):
    thread = Thread()
    c1 = Comment(username='testusername2', content='testscontent', thread=thread)
    test_db.session.add(c1)
    test_db.session.commit()
    assert len(Comment.query.all()) == 2

def test_threadsWork(test_db):
    thread = Thread()
    Comment(username='testusername', content='first in thread', thread=thread)
    c2 = Comment(username='testusername', content='second in thread')
    thread.comments.append(c2)
    test_db.session.add(thread)
    assert len(thread.comments) == 2