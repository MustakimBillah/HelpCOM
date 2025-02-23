from pymongo import MongoClient
import random

#client = MongoClient('mongodb://10.136.219.243:27017/')
client = MongoClient('mongodb://localhost:27017/')

db = client.code_understanding             
javaDBFinal = db.javaDBCodeT5p.find()
populationDB = db.populationDB
population =[]

count = 0
total = 0
dependentCount = 0
independentCount = 0
dependentSideGT = 0

for item in javaDBFinal:
    methods = item.get('methods')
    for index, method in enumerate(methods):
        try:
            Docstring = method.get('Docstring') 
            if (len(Docstring)>0):
                count+=1
                if (method.get('isDependent')):
                    dependentCount+=1
                    if (method.get('sideGT')>=0.80):
                        dependentSideGT+=1
                        data = {
                            "parentID": item.get('_id'),
                            "repo": item.get('repo'),
                            "file": item.get('file'),
                            "method": method,
                            "index": index,
                            "imports": item.get('imports'),
                            "language": item.get('language')
                        }
                        population.append(data)
                else:
                    independentCount+=1
        except Exception as e:
            print("Not Found: ", e)

print ("Total Methods with docstring: ", count)
print("among Them Dependent : ",dependentCount)
print("dependent with better quality GT: ",dependentSideGT)
print("among Them InDependent :",independentCount)


