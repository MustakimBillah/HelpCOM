from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.code_understanding      

methodHistoryDB = db.methodHistory
javaDB = db.javaDBCodeT5p.find()

#methodHistoryList = []
javaDBList = []


# for item in methodHistoryDB:
#     methodHistoryList.append(item)

for element in javaDB:
    javaDBList.append(element)


print("Before Searching")

for item in javaDBList:
    id = item.get('_id')
    matchedID = methodHistoryDB.find_one({"_id":id})
    if(matchedID!=None):
            javaDBMethods = item.get('methods')
            mHDBmethods = matchedID.get('methods')
            idx = 0
            for tuple in javaDBMethods:
                row = mHDBmethods[idx]
                tuple['commits'] = row.get('commits')
                tuple['authors'] = row.get('authors')
                tuple['diffs'] = row.get('diffs')
                tuple['commits'] = row.get('commits')
                tuple['firstCommit'] = row.get('firstCommit')
                tuple['lastCommit'] = row.get('lastCommit')
                tuple['timeFrame'] = row.get('timeFrame')
                idx += 1
    else:
         print("No match found for id : ",id)


javaDBFinal = db.javaDBFinal

for item in javaDBList:
    javaDBFinal.insert_one(item)
    print("Added item : ",item.get('_id'))