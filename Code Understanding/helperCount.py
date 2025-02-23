from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.code_understanding             
javaDBFinal = db.javaDBFinal.find()

helpetCount = 0

for element in javaDBFinal:
    methods = element.get('methods')
    for item in methods:
        if (item.get('isDependent')==True):
            helpers = item.get('helpers').get('helpers')
            helpetCount += len(helpers)

print("Total helper methods : ", helpetCount)





            



