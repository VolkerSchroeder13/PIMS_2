from sqlalchemy import Column, String, Float, Text, Numeric, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *


Base = declarative_base()


class Product(Base):
    __tablename__ = "product"
    
    address = Column(String(255))
    brand = Column(String(255))
    id = Column(String(255), primary_key=True)
    title = Column(String(255))
    price = Column(Float)
    size = Column(Numeric(10, 2))
    unit = Column(String(255))
    time = Column(String(255))

    short_description = Column(Text)
    description = Column(Text)
    recommendation = Column(Text)
    composition = Column(Text)
    usage = Column(Text)
    safety = Column(Text)
   
    recommendation_title = Column(String(255))
    composition_title = Column(String(255))
    usage_title = Column(String(255))
    safety_title = Column(String(255))
   
    short_description_html = Column(Text)
    description_html = Column(Text)
    recommendation_html = Column(Text)
    composition_html = Column(Text)
    usage_html = Column(Text)
    safety_html = Column(Text)


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
    category = Column(Integer, ForeignKey(Category.id))

class Image(Base):
    __tablename__ = "image"
    id = Column(Integer, primary_key=True, autoincrement=True)
    product = Column(String(255), ForeignKey(Product.id))
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