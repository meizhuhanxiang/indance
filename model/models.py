# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String, text, Text, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker, scoped_session
import utils.config

Base = declarative_base()
metadata = Base.metadata
DB_USER = utils.config.get("preseller_mysql", "user")
DB_PWD = utils.config.get("preseller_mysql", "passwd")
DB_HOST = utils.config.get("preseller_mysql", "host")
DB_NAME = utils.config.get("preseller_mysql", "database")
DB_PORT = utils.config.get("preseller_mysql", "port")
engine = create_engine('mysql://%s:%s@%s/%s?charset=utf8' % (DB_USER, DB_PWD, DB_HOST, DB_NAME), encoding='utf-8',
                       echo=False, pool_size=100, pool_recycle=10)
db = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=True, expire_on_commit=False))()


class Kind(Base):
    __tablename__ = 'kind'

    id = Column(Integer, primary_key=True)
    purchase_id = Column(Integer, ForeignKey('purchase.id'))
    kind = Column(String(11))

    orders = relationship('Order', backref=backref('kind'))

    @property
    def items(self):
        return dict(kind=self.kind)


class Purchase(Base):
    __tablename__ = 'purchase'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    price = Column(String(30))
    publisher_id = Column(String(30), ForeignKey('publisher.id'))
    info = Column(Text)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
    start_time = Column(DateTime)
    end_time = Column(DateTime)

    kinds = relationship('Kind', backref=backref('purchase'))
    orders = relationship('Order', backref=backref('purchase'))


class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    status = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.id'))
    kind_id = Column(Integer, ForeignKey('kind.id'))
    purchase_id = Column(Integer, ForeignKey('purchase.id'))
    pay_time = Column(DateTime)
    create_time = Column(DateTime)
    verify_time = Column(DateTime)
    verify_count = Column(Integer)

    def save(self):
        db.add(self)
        db.commit()

    @property
    def items(self):
        purchase = db.query(Purchase).filter(id=self.purchase_id).first()
        info = purchase.info if purchase else ''
        return dict(user_id=self.id, status=self.status, kind_id=self.kind_id, pay_time=self.pay_time, purchase_info=info)


class Publisher(Base):
    __tablename__ = 'publisher'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    city = Column(String(30))

    purchases = relationship('Purchase', backref=backref('publisher'))


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    nickname = Column(String(30), nullable=False, server_default=text("''"))
    open_id = Column(String(30), nullable=False, server_default=text("''"))
    sex = Column(String(6), nullable=False, server_default=text("''"))
    province = Column(String(20), nullable=False, server_default=text("''"))
    city = Column(String(20), nullable=False, server_default=text("''"))
    country = Column(String(20), nullable=False, server_default=text("''"))
    profile = Column(String(150), nullable=False, server_default=text("''"))
    privilege = Column(String(40), nullable=False, server_default=text("''"))
    union_id = Column(String(30), nullable=False, server_default=text("''"))
    is_v = Column(Integer, nullable=False, server_default=text("'0'"))
    name = Column(String(16))
    job = Column(String(30))
    company = Column(String(30))
    phone = Column(Integer)
    email = Column(String(30))
    update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    create_time = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))

    orders = relationship('Order', backref=backref('user'))



pass