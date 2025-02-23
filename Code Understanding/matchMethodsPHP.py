from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.code_understanding      


methodsDB = db.methodsPHP.find()


helperMethodsList = []
methodsList = []


for item in methodsDB:
    helperMethodsList.append(item)
    methodsList.append(item)


print(len(methodsList))

client.close()


def getMethodBody(repo,functionName,argsCount):
    methodBody=""
    fileName=""
    probableList=[]
    for item in methodsList:
        
        if (item.get('repo')==repo):
            
            fileName = item.get('file')
            methods = item.get('methods')
            if len(methods)==0:
                continue
            for method in methods:
                if functionName == method.get('FunctionName'):
                    methodBody = method.get('Syntax')
                    paramCount = method.get('ArgsCount')
                    probableList.append({
                        'MethodBody': methodBody,
                        'ArgsCount':paramCount,
                        'FileName':fileName
                    })
    

    for item in probableList:
        methodBody = item.get('MethodBody')
        ArgsCount = item.get('ArgsCount')
        fileName = item.get('FileName')

        if(ArgsCount==argsCount):
            return methodBody, fileName


    return methodBody,fileName 

counter = 0
for element in helperMethodsList:
    repo = element.get('repo')
    file = element.get('file')
    methods = element.get('methods')

    for item in methods:
        try:
            helpersArray = item.get('helpers').get('helpers')
        except:
            continue
        
        for helper in helpersArray:
            functionName = helper.get('FunctionName')
            argsCount = helper.get('ArgsCount')
            methodBody, fileName = getMethodBody(repo,functionName,argsCount)
            helper["MethodBody"] = methodBody
            helper["FileName"] = fileName
            #print(item)
            if len(methodBody)>0:
                counter += 1
            #print("Processed helpers: ",counter)

client = MongoClient('mongodb://localhost:27017/')

db = client.code_understanding

methodsDB = db.methodsPHP

for item in helperMethodsList:
    
    methods = item.get('methods')

    for index, method in enumerate(methods):

        helpers = method.get('helpers')

        methodsDB.update_one(
                {'_id': item.get('_id')},
                {
                    "$set": {
                        f"methods.{index}.helpers": helpers
                    }
                }
            )
    






