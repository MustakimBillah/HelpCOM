from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.code_understanding             
matchedDB = db.matchedDB.find()

fileList = []


for item in matchedDB:
    fileList.append(item)

client.close()


for element in fileList:
    methods = element.get('methods')
    for item in methods:
        isDependent = False
        helpersArray = item.get('helpers').get('helpers')
        for helper in helpersArray:
            methodBody = helper.get('MethodBody')
            methodBody = methodBody.strip()
            if (methodBody != ""):
                isDependent = True
                break
        item["isDependent"] = isDependent


client = MongoClient('mongodb://localhost:27017/')
db = client.code_understanding             
javaDB = db.javaDB


for item in fileList:
    javaDB.insert_one(item)
    print("inserted: ",item.get("_id"))
            





            



