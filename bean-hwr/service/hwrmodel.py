# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String,DateTime
from sqlalchemy.ext.declarative import declarative_base
from .dbengine import SqlalchemyEngine
from datetime import datetime

Base = declarative_base()
engine = SqlalchemyEngine().engine

# 手写体图片实体类
class ImageInfo(Base):

    __tablename__ = 'image_info'
    id = Column('id', Integer, primary_key=True)
    image_no = Column('image_no', String(20), nullable=False,index=True)
    upload_path = Column('upload_path', String(255), nullable=False)
    deal_result = Column('deal_result', String(255), nullable=True)
    create_time = Column('create_time', DateTime, default=datetime.now)
    update_time = Column('update_time', DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self,image_no, upload_path, deal_result):
        self.image_no = image_no
        self.upload_path = upload_path
        self.deal_result = deal_result


# 图片识别结果实体类
class FeedBackInfo(Base):

    __tablename__ = 'feed_back_info'
    id = Column('id', Integer, primary_key=True)
    image_no = Column('image_no', String(20), nullable=False,)
    feed_back_result = Column('feed_back_result', String(100), nullable=True)
    create_time = Column('create_time', DateTime, default=datetime.now)

    def __init__(self,image_no,feed_back_result):
        self.image_no = image_no
        self.feed_back_result = feed_back_result


def init_db():
    Base.metadata.create_all(engine)
