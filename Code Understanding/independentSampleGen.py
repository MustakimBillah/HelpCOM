import csv
from pymongo import MongoClient
from bson.objectid import ObjectId
import random

client = MongoClient('mongodb://localhost:27017/')
db = client.code_understanding             
javaDBFinal = db.javaDBCodeT5p
populationDB = db.populationSideGT.find()
sampleIndepDB = db.indepSample
count = 0
sampleCount = 0 
sampleList = []

popList=[]

for item in populationDB:
    popList.append(item)

random.shuffle(popList)

# Replace 'your_file.csv' with the path to your CSV file
for sample in popList:
    parentID = sample.get('parentID')
    #print(parentID)
    index = sample.get('index')
    sampleInOriginalDB = javaDBFinal.find_one({'_id':ObjectId(parentID)})
    originalSample = sampleInOriginalDB.get('methods')[index]
    #print(sampleInOriginalDB.get('repo'))
    bleu = originalSample.get('bleuCodeT5p')

    originalSample['parentID']= parentID
    originalSample['index'] = index
    originalSample['repo'] = sampleInOriginalDB.get('repo')
    originalSample['path'] = sampleInOriginalDB.get('file')
    #print(bleu)
    #print('---------------')
    #maxBleu = max(bleu, maxBleu) 

    if(originalSample.get('isDependent')):
        continue

    if (bleu >= 0.018):  
        sampleList.append(originalSample)
        sampleCount+=1

    if(sampleCount==380):
        print("Sample Creaetion Done for independed methods")
        break

            
for sample in sampleList:
    sampleIndepDB.insert_one(sample)

print("Sample DB Created ", sampleCount)