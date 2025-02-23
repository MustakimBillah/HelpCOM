from pymongo import MongoClient
import json
import re
client = MongoClient('mongodb://localhost:27017/')
db = client.code_understanding             
dependentSample = db.depSample.find()
inDependentSample = db.indepSample.find()

count = 0

inputData = []

for item in inDependentSample:
    id = item.get('_id')
    syntax = item.get('Syntax')
    code_tokens = re.findall(r'@\w+|"[^"]*"|\w+|//[^\n]*|[{}();.,<>]', syntax)
    docstring= item.get('methodLevelComment')
    docstring_tokens = docstring.replace("\n"," ").split()

    data = {"_id": str(id), "original_string": syntax,"code": syntax, "code_tokens": code_tokens,
            "language":"java", "repo":item.get('repo'),"path":item.get('path'),"url":item.get('path'),"partition":"test",
            "func_name":item.get('FunctionName'),"docstring":docstring, "docstring_tokens": docstring_tokens, "sampleType":"independent"}
    inputData.append(data)
    count+=1
    print("added independent data: ",count)

count = 0

for item in dependentSample:
    id = item.get('_id')
    syntax = item.get('Syntax')
    code_tokens = re.findall(r'@\w+|"[^"]*"|\w+|//[^\n]*|[{}();.,<>]', syntax)
    docstring= item.get('methodLevelComment')
    docstring_tokens = docstring.replace("\n"," ").split()

    data = {"_id": str(id), "original_string": syntax,"code": syntax, "code_tokens": code_tokens,
            "language":"java", "repo":item.get('repo'),"path":item.get('path'),"url":item.get('path'),"partition":"test",
            "func_name":item.get('FunctionName'),"docstring":docstring, "docstring_tokens": docstring_tokens, "sampleType":"dependent"}
    inputData.append(data)
    count+=1
    print("added dependent data: ",count)


# Define the file name
filename = "path/ASAP_DATASET/Java_data/Java_data/testASAP.jsonl"

# Open the file in write mode
with open(filename, 'w') as file:
    # Iterate through the list of data
    for entry in inputData:
        # Convert each dictionary to a JSON string and write it as a line
        file.write(json.dumps(entry) + '\n')

print(f"Data successfully written to {filename}")



            
