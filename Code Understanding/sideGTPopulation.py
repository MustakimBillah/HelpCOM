from pymongo import MongoClient
import random

#client = MongoClient('mongodb://10.136.219.243:27017/')
client = MongoClient('mongodb://localhost:27017/')

db = client.code_understanding             
javaDBFinal = db.javaDBCodeT5p.find()
populationDB = db.populationSideGT
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
                if (method.get('sideGT')>=0.80):
                    data = {
                        "parentID": item.get('_id'),
                        "repo": item.get('repo'),
                        "file": item.get('file'),
                        "method": method,
                        "index": index,
                        "imports": item.get('imports'),
                        "language": item.get('language'),
                    }
                    population.append(data)

        except Exception as e:
            print("Not Found: ", e)

print ("Total population: ", len(population))



for element in population:
    populationDB.insert_one(element)

print("done processing")