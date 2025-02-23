from pymongo import MongoClient
import random

#client = MongoClient('mongodb://10.136.219.243:27017/')
client = MongoClient('mongodb://localhost:27017/')

db = client.code_understanding             
pythonDBFinal = db.methodsPython.find()
samplePython = db.samplePython
population =[]

count = 0
total = 0
dependentCount = 0
independentCount = 0
dependentSideGT = 0
independentSideGT = 0

for item in pythonDBFinal:
    methods = item.get('methods')
    for index, method in enumerate(methods):
        isDependent = False
        try:
            Docstring = method.get('Docstring') 
            if (len(Docstring)>0):
                count+=1

                try:
                    helpers=method.get('helpers').get('helpers')
                    
                    for helper in helpers:
                        if(len(helper.get('MethodBody'))>0):
                            dependentCount+=1
                            isDependent = True
                            break

                except:
                    print("no helpers")


        except Exception as e:
            print("Not Found: ", e)
        
        if isDependent == True:
            population.append(method)

print ("Total Methods with docstring: ", count)
print("among Them Dependent : ",dependentCount)


sampleList = random.sample(population, 50)

print("Population Size: ",len(population))

for item in sampleList:
     samplePython.insert_one(item)
