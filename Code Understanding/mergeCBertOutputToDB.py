import json
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient('mongodb://10.136.219.243:27017/')
#client = MongoClient('mongodb://localhost:27017/')
db = client.code_understanding             
javaDBCodeT5p = db.javaDBCodeT5p

jsonl_file_path = '/u2/users/mjr175/codeBert/CodeXGLUE/Code-Text/code-to-text/dataset/java/cBertOutput.jsonl'

with open(jsonl_file_path, 'r') as jsonl_file:
    json_lines = [json.loads(line) for line in jsonl_file.readlines()]

for item in json_lines:
    id = item.get('_id')
    index = item.get('index')
    object_id = ObjectId(id)
    element = javaDBCodeT5p.find_one({"_id":object_id})
    
    method = element.get('methods')[index]
    
    javaDBCodeT5p.update_one(
        {'_id': element['_id']},
        {"$set": {f"methods.{index}.cBert_Summary": item.get('summary')}}
    ) 
    print('updated id: ',object_id)

