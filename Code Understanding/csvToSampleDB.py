import csv
from pymongo import MongoClient
from bson.objectid import ObjectId
import random

client = MongoClient('mongodb://localhost:27017/')
db = client.code_understanding             
javaDBFinal = db.javaDBCodeT5p
populationDepDB = db.populationDB
sampleDepDB = db.depSample
count = 0
sampleCount = 0 
sampleList = []
# Replace 'your_file.csv' with the path to your CSV file
with open('/student/mjr175/method-level-comment-generation/Code Understanding/population(in).csv', mode='r') as file:
    csv_reader = csv.DictReader(file)
    
    # Display each row as a dictionary
    maxBleu = 0
    for row in csv_reader:
        selected = (row.get('selected_as_sample'))
        
        id = row.get('_id')
        sample = populationDepDB.find_one({'_id':ObjectId(id)})
        parentID = sample.get('parentID')
        #print(parentID)
        index = sample.get('index')
        sampleInOriginalDB = javaDBFinal.find_one({'_id':ObjectId(parentID)})
        originalSample = sampleInOriginalDB.get('methods')[index]
        #print(sampleInOriginalDB.get('repo'))
        bleu = originalSample.get('bleuCodeT5p')
        #print(bleu)
        #print('---------------')
        #maxBleu = max(bleu, maxBleu) 
        originalSample['parentID']= parentID
        originalSample['index'] = index
        originalSample['repo'] = sampleInOriginalDB.get('repo')
        originalSample['path'] = sampleInOriginalDB.get('file')

        if (selected == 'Yes'):  
            sampleList.append(originalSample)
            sampleCount+=1


print("inserted samples:", sampleCount)

with open('/student/mjr175/method-level-comment-generation/Code Understanding/population(in).csv', mode='r') as file:
    csv_reader = list(csv.DictReader(file))  # Convert to list for shuffling
    random.shuffle(csv_reader)
    
    # Display each row as a dictionary
    for row in csv_reader:
        selected = (row.get('selected_as_sample'))
        
        id = row.get('_id')
        sample = populationDepDB.find_one({'_id':ObjectId(id)})
        parentID = sample.get('parentID')
        #print(parentID)
        index = sample.get('index')
        sampleInOriginalDB = javaDBFinal.find_one({'_id':ObjectId(parentID)})
        originalSample = sampleInOriginalDB.get('methods')[index]
        #print(sampleInOriginalDB.get('repo'))
        bleu = originalSample.get('bleuCodeT5p')
        #print(bleu)
        #print('---------------')
        #maxBleu = max(bleu, maxBleu) 
        originalSample['parentID']= parentID
        originalSample['index'] = index
        originalSample['repo'] = sampleInOriginalDB.get('repo')
        originalSample['path'] = sampleInOriginalDB.get('file')

        if (selected == 'Yes'):  
            continue
        else:
            helpers = originalSample.get('helpers').get('helpers')
            if(len(helpers)<=4 and bleu<=0.1):
                sampleList.append(originalSample)
                sampleCount+=1
    
        if(sampleCount==380):
            print("Sample Creaetion Done for depended methods")
            break

            
for sample in sampleList:
    sampleDepDB.insert_one(sample)

print("Sample DB Created")