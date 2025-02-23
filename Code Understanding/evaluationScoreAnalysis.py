from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.code_understanding             
docStringMethods = db.docStringMethods.find()

cnt=0

for item in docStringMethods:
    cnt+=1

print(cnt)



