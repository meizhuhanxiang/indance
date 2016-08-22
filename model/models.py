# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Kind(Base):
    __tablename__ = 'kind'

    id = Column(Integer, primary_key=True)
    purchase_id = Column(Integer)
    kind = Column(String(11))


class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    status = Column(String(11))
    user_id = Column(String(11))
    kind_id = Column(String(11))
    pay_time = Column(Integer)
    verify_time = Column(Integer)
    verify_count = Column(Integer)


class Publisher(Base):
    __tablename__ = 'publisher'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    city = Column(String(30))


class Purchase(Base):
    __tablename__ = 'purchase'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    price = Column(String(30))
    publisher_id = Column(String(30))
    create_time = Column(String(30))
    update_time = Column(String(30))
    start_time = Column(String(30))
    end_time = Column(Integer)


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
