from pymongo import MongoClient


class TestData:

    def __init__(self,):
        # Provide the mongodb atlas url to connect python to mongodb using pymongo
        CONNECTION_STRING = "mongodb://jawad:betts@cluster0-shard-00-00.e4wxf.mongodb.net:27017,cluster0-shard-00-01.e4wxf.mongodb.net:27017,cluster0-shard-00-02.e4wxf.mongodb.net:27017/?ssl=true&replicaSet=atlas-enqd3d-shard-0&authSource=admin&retryWrites=true&w=majority"

        # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
        client = MongoClient(CONNECTION_STRING)

        #db
        self.db = client.connectTest

    def update_job_values(self, updated_job_values):
        self.db["job_values"].update_many({}, {"$set":updated_job_values})
    
    def update_cand_values(self, updated_cand_values):
        self.db["cand_values"].update_many({}, {"$set":updated_cand_values})

