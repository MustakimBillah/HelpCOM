from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.code_understanding      

helperMethodsDB = db.helperMethods.find()

methodsDB = db.methods.find()


helperMethodsList = []
methodsList = []


for item in helperMethodsDB:
    helperMethodsList.append(item)

for element in methodsDB:
    methodsList.append(element)

client.close()


def getMethodBody(repo,functionName,argsCount):
    methodBody=""
    fileName=""
    for item in methodsList:
        if (item.get('repo')==repo):
            fileName = item.get('file')
            methods = item.get('methods')
            for method in methods:
                if(functionName == method.get('FunctionName') and argsCount == method.get('ArgsCount')):
                    methodBody = method.get('Syntax')
                    return methodBody,fileName
    return methodBody,fileName 

counter = 0
for element in helperMethodsList:
    repo = element.get('repo')
    file = element.get('file')
    methods = element.get('methods')

    for item in methods:
        helpersArray = item.get('helpers').get('helpers')
        
        for helper in helpersArray:
            functionName = helper.get('FunctionName')
            argsCount = helper.get('ArgsCount')
            methodBody, fileName = getMethodBody(repo,functionName,argsCount)
            helper["MethodBody"] = methodBody
            helper["FileName"] = fileName
            #print(item)
            counter += 1
            print("Processed helpers: ",counter)

client = MongoClient('mongodb://localhost:27017/')

db = client.code_understanding

matchedDB = db.matchedDB

for item in helperMethodsList:
    matchedDB.insert_one(item)
    






