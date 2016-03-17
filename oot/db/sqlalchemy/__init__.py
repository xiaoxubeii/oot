__author__ = 'tardis'
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from contextlib2 import contextmanager
from oslo_config import cfg
import uuid

opts = [
    cfg.StrOpt('db_url', default='mysql+mysqlconnector://oot:oot@localhost:3306/oot')
]

CONF = cfg.CONF
CONF.register_opts(opts)

engine = create_engine(CONF.db_url)
DBSession = sessionmaker(bind=engine)


def create(model):
    with _get_dbsession() as session:
        if hasattr(model, 'id'):
            setattr(model, 'id', str(uuid.uuid4()))
        session.add(model)
        session.commit()


def get(model_cls, model_id):
    with _get_dbsession() as session:
        model = session.query(model_cls).filter_by(id=model_id).one()
        return model


def list(model_cls, **kwargs):
    with _get_dbsession() as session:
        l = session.query(model_cls).filter_by(**kwargs).all()
        return l


def delete(model_cls, id):
    with _get_dbsession() as session:
        model = session.query(model_cls).filter_by(id=id).first()
        session.delete(model)
        session.commit()


def update(model_cls, m):
    with _get_dbsession() as session:
        session.query(model_cls).filter_by(id=m.pop('id')).update(m)
        session.commit()


@contextmanager
def _get_dbsession():
    session = DBSession()
    yield session
    session.close()

