from peewee import *
db = SqliteDatabase('zhihu/persistence/sqlite.db')

class Person(Model):
      name = CharField(null=True)
      url_token = CharField(unique=True)
      location = CharField(null=True)
      business = CharField(null=True)
      gender = CharField(null=True)
      employment = CharField(null=True)
      education = CharField(null=True)
      avatar_url = CharField(null=True)
      description = CharField(null=True)
      headline = CharField(null=True)
      class Meta:
          database = db  # 指定数据库 

class Relation(Model):
      left_url_token = CharField()
      right_url_token = CharField()
      relation_type = IntegerField()
      class Meta:
          database = db  # 指定数据库 
          primary_key = CompositeKey('left_url_token', 'right_url_token','relation_type')

db.connect()
db.create_tables([Person,Relation])

def save_person(person):
  try:
    Person.create(**person)
  except IntegrityError as err:
    print('已存在', err)
    
    
def query_person_by_token(url_token):
  if user:=Person.get_or_none(Person.url_token == url_token):
    return user.__data__
  return None



def save_relation(relation):
  try:
    Relation.create(**relation)
  except IntegrityError as err:
    print('已存在', err)
    
# save_person({"name":2,"url_token":6})