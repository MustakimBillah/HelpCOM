from pymongo import MongoClient
import csv
#client = MongoClient('mongodb://10.136.219.243:27017/')
client = MongoClient('mongodb://localhost:27017/')

db = client.code_understanding             
populationDB = db.populationDB.find()

with open('population.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["method","docstring","_id"])
    for sample in populationDB:
        id = sample.get('_id')
        method = sample.get('method')
        methodBody = method.get('Syntax')
        docstring = method.get('Docstring')
        helpers = method.get('helpers').get('helpers')

        writer.writerow([methodBody,docstring,id])

print("Data exported to CSV successfully!")