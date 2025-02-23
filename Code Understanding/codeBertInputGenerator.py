from pymongo import MongoClient
import json

client = MongoClient('mongodb://10.136.219.243:27017/')
#client = MongoClient('mongodb://localhost:27017/')
db = client.code_understanding             
javaDBFinal = db.javaDBFinal.find()


javaDBFinalList = []

for element in javaDBFinal:
    javaDBFinalList.append(element)

client.close()

count = 0

inputData = []

for item in javaDBFinalList:
    id = item.get('_id')
    methods = item.get('methods')
    for index, method in enumerate(methods):
        Docstring = method.get('Docstring')
        wordCount = len(Docstring.split())
        if (wordCount > 0):
            count+=1
            code = method.get('Syntax')
            data = {"_id": str(id), "index": index, "code": code, "docstring": Docstring}
            inputData.append(data)
            print("added data: ",count)

# Define the file name
filename = "codeBertInput.jsonl"

# Open the file in write mode
with open(filename, 'w') as file:
    # Iterate through the list of data
    for entry in inputData:
        # Convert each dictionary to a JSON string and write it as a line
        file.write(json.dumps(entry) + '\n')

print(f"Data successfully written to {filename}")



            
