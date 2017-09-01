# -*- coding: utf-8 -*-
from .dbengine import SqlalchemyEngine
from .hwrmodel import ImageInfo
from .hwrmodel import FeedBackInfo
from sqlalchemy import extract, and_
import datetime
import time
import random
import os
import sys
sys.path.append(os.path.dirname(__file__)+'/'+'..')
from config import Config


class HwrService:
    CODE_LIST = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    # 保存上传的手写图片信息
    def saveImage(self, path):
        image_no = self.createno(3)
        path += (image_no + Config.image_format)
        image = ImageInfo(image_no, path, '')
        session = SqlalchemyEngine().getSession()
        session.add(image)
        session.commit()
        return image_no

    # 查询当天已上传的图片数量
    def queryCntByCurDate(self):
        session = SqlalchemyEngine().getSession()
        now = datetime.datetime.now()
        year = now.strftime('%Y')
        mouth = now.strftime('%m')
        day = now.strftime('%d')
        return session.query(ImageInfo).filter(and_(extract('year', ImageInfo.create_time) == year,
                                                    extract('month', ImageInfo.create_time) == mouth,
                                                    extract('day', ImageInfo.create_time) == day,
                                                    ImageInfo.deal_result != '')).count()

    # 更新手写体图片识别结果
    def updateResult(self, image_no, result):
        session = SqlalchemyEngine().getSession()
        session.query(ImageInfo).filter(ImageInfo.image_no == image_no).update({ImageInfo.deal_result: result})
        session.commit()

    # 保存用户反馈信息
    def saveFeedBackInfo(self, image_no, feed_back_result):
        feedBackInfo = FeedBackInfo(image_no,feed_back_result)
        session = SqlalchemyEngine().getSession()
        session.add(feedBackInfo)
        session.commit()

    # 生产序列号
    def createno(self, num):
        time_str = time.strftime("%Y%m%d%H%M%S", time.localtime())
        if num == 0:
            return time_str
        random_str = ''.join(random.sample(self.CODE_LIST, num))
        code = time_str + random_str
        return code
