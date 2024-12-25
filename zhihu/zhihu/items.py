
from scrapy import Item, Field


class PeopleItem(Item):
    """
    知乎用户属性
    
    属性:
        name 用户名
        url_token 用户id
        location 位置
        business 行业
        gender 性别
        employment 公司
        education 教育情况
        avatar_url 头像图片url
        description 个人简介
        headline 一句话介绍
    """
    name = Field()
    url_token = Field()
    location = Field()
    business = Field()
    gender = Field()
    employment = Field()
    education = Field()
    avatar_url = Field()
    description = Field()
    headline = Field()



class RelationItem(Item):
    """知乎用户关系
    Attributes:
        left_url_token 用户id
        right_url_token 用户id
        user_type 用户left_url_token和right_url_token的关系（1 前者关注后者 2前者被后者关注）
    """
    left_url_token = Field()
    right_url_token = Field()    
    relation_type = Field()


