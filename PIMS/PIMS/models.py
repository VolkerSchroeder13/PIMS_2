from sqlalchemy import Column, String, Float, Text, Numeric, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *


Base = declarative_base()


class Product(Base):
    __tablename__ = "product"
    
    address = Column(String(255))
    brand = Column(String(255))
    id = Column(String(255), primary_key=True)
    parent = Column(String(255))
    ean = Column(String(255))
    title = Column(String(255))
    price = Column(Float)
    size = Column(Numeric(10, 2))
    unit = Column(String(255))
    time = Column(String(255))
    date = Column(String(255))

    title_1 = Column(Text)
    title_2 = Column(Text)
    title_3 = Column(Text)
    title_4 = Column(Text)
    title_5 = Column(Text)
    title_6 = Column(Text)

    content_1 = Column(Text)
    content_2 = Column(Text)
    content_3 = Column(Text)
    content_4 = Column(Text)
    content_5 = Column(Text)
    content_6 = Column(Text)

    content_1_html = Column(Text)
    content_2_html = Column(Text)
    content_3_html = Column(Text)
    content_4_html = Column(Text)
    content_5_html = Column(Text)
    content_6_html = Column(Text)


class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    parent = Column(Integer)
    title = Column(String(255))


class Selector(Base):
    __tablename__ = "selector"
    id = Column(Integer, primary_key=True, autoincrement=True)
    brand = Column(String(255))
    selector = Column(Text)
    category = Column(Integer, ForeignKey(Category.id))


class ProductCategory(Base):
    __tablename__ = "product_category"
    id = Column(Integer, primary_key=True, autoincrement=True)
    product = Column(String(255), ForeignKey(Product.id))
    brand = Column(String(255))
    category = Column(Integer, ForeignKey(Category.id))

class Image(Base):
    __tablename__ = "image"
    id = Column(Integer, primary_key=True, autoincrement=True)
    product = Column(String(255), ForeignKey(Product.id))
    brand = Column(String(255))
    image_1 = Column(String(255))
    image_2 = Column(String(255)) 
    image_3 = Column(String(255)) 
    image_4 = Column(String(255)) 
    image_5 = Column(String(255)) 
    image_6 = Column(String(255)) 
    image_7 = Column(String(255)) 
    image_8 = Column(String(255)) 
    image_9 = Column(String(255)) 
    image_10 = Column(String(255)) 
    image_11 = Column(String(255)) 
    image_12 = Column(String(255))