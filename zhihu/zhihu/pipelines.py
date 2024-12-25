from zhihu.items import PeopleItem, RelationItem
from zhihu.persistence.sqlite import save_person, save_relation

class ZhihuPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, PeopleItem):
            save_person(item)
        elif isinstance(item, RelationItem):
            save_relation(item)
        return item