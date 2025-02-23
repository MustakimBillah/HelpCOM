from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.code_understanding             
javaDBFinal = db.javaDBCodeT5p.find()
docStringMethods = db.docStringMethods

methodList=[]

for element in javaDBFinal:
    print("processing item: ",element.get('_id'))
    methods = element.get('methods')
    for method in methods:

        docstring = method.get('Docstring')

        if len(docstring)>0:
            methodList.append(method)


            
       
for item in methodList:
    docStringMethods.insert_one(item)


print("done processing")
