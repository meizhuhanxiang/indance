# coding: utf-8


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Integer, String, text, create_engine

Base = declarative_base()
metadata = Base.metadata


class Addres(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    name = Column(Integer)
    country = Column(Integer)
    province = Column(Integer)
    reginon = Column(Integer)
    address = Column(String(50))
    phone = Column(Integer)
    default = Column(Integer, server_default=text("'0'"))
    update_time = Column(DateTime)


class Cart(Base):
    __tablename__ = 'cart'

    id = Column(Integer, primary_key=True)
    seed_id = Column(Integer, nullable=False)
    properties = Column(String(100), nullable=False, server_default=text("''"))
    count = Column(Integer, nullable=False)
    make_order = Column(Integer, nullable=False, server_default=text("'0'"))
    update_time = Column(DateTime, nullable=False)


class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    seed_id = Column(Integer, nullable=False)
    address_id = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)
    update_time = Column(DateTime, nullable=False)


class Publisher(Base):
    __tablename__ = 'publisher'

    id = Column(Integer, primary_key=True)
    logo = Column(String(30))
    navigation_img = Column(String(30), nullable=False, server_default=text("''"))
    brief_introduction = Column(String(60), nullable=False, server_default=text("''"))
    activity_photos = Column(String(30), nullable=False, server_default=text("''"))
    admin_name = Column(String(16), nullable=False, server_default=text("''"))
    admin_phone = Column(Integer, nullable=False)
    admin_id_card_number = Column(String(20), nullable=False, server_default=text("''"))
    admin_id_card_img = Column(String(30), nullable=False, server_default=text("''"))
    other_title = Column(String(20), nullable=False, server_default=text("''"))
    other_content = Column(String(60), nullable=False, server_default=text("''"))
    update_time = Column(DateTime, nullable=False)


class Purchase(Base):
    __tablename__ = 'purchase'

    id = Column(Integer, primary_key=True)
    title = Column(String(40), nullable=False, server_default=text("''"))
    brief = Column(String(100), nullable=False, server_default=text("''"))
    navigation = Column(String(11), nullable=False, server_default=text("''"))
    presell_count = Column(Integer, nullable=False)
    sold_count = Column(Integer, nullable=False, server_default=text("'0'"))
    satisfy_count = Column(Integer, nullable=False)
    logo = Column(String(40), nullable=False, server_default=text("''"))
    publisher_id = Column(Integer, nullable=False)
    properties = Column(String(100), nullable=False, server_default=text("''"))
    update_time = Column(DateTime, nullable=False)


class Recommend(Base):
    __tablename__ = 'recommend'

    id = Column(Integer, primary_key=True)
    seed_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    content = Column(Integer, nullable=False)
    update_time = Column(DateTime, nullable=False)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    nickname = Column(String(30), nullable=False, server_default=text("''"))
    open_id = Column(String(30), nullable=False, server_default=text("''"))
    sex = Column(String(6), nullable=False, server_default=text("''"))
    province = Column(String(20), nullable=False, server_default=text("''"))
    city = Column(String(20), nullable=False, server_default=text("''"))
    country = Column(String(20), nullable=False, server_default=text("''"))
    head_img_url = Column(String(150), nullable=False, server_default=text("''"))
    privilege = Column(String(40), nullable=False, server_default=text("''"))
    union_id = Column(String(30), nullable=False, server_default=text("''"))
    is_v = Column(Integer, nullable=False, server_default=text("'0'"))
    name = Column(String(16))
    job = Column(String(30))
    company = Column(String(30))
    phone = Column(Integer)
    email = Column(String(30))
    update_time = Column(DateTime)



