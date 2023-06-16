import pytz
import uuid
from config.Common import Common
from mongodb.MongoDB import MongoDB
from datetime import datetime

class AppModel:
    
    def __init__(self):
        conf = Common()
        self.db_config = conf.get_Database() 
        self.Timezone = conf.get_TimeZone()
        self._db = MongoDB()
          
    def insert_wallet(self, wallet: dict):
        '''
        This method verifies if the wallet exists and decides the
        record will be inserted or updated'''

        collection = self.db_config['DB_TABLE_WALLET']
            
        filter = {'user_email': wallet['user_email']}
        data = self._db.mongo_find(filter, collection, Limit=1)
        
        if len(data) == 0:
            wallet['_id'] = str(uuid.uuid4())
            wallet['inserted_date'] = datetime.utcnow()
            wallet['updated_date'] = datetime.utcnow()
            result = self._db.mongo_insert_items(wallet, collection)
        else:
            if data != wallet:
               wallet['updated_date'] = datetime.utcnow()
               result = self._db.mongo_update_items(Filter={'_id': wallet['_id']},
                                                    Update={'$set': wallet},
                                                    Collection=collection,
                                                    Upsert=True)
            
               return result


    def get_wallet(self, user_email) -> dict:
        
        result = self._db.mongo_find(Filter={'user_email': user_email}, 
                                     Collection=self.db_config['DB_TABLE_WALLET'], 
                                     Limit=1)
        return result

