
import tree_sitter_python as tspython
from tree_sitter import Language, Parser
from pymongo import MongoClient
import sys
 
sys.setrecursionlimit(10**6)

PY_LANGUAGE = Language(tspython.language(),'python')

parser = Parser()
parser.set_language(PY_LANGUAGE)


def traverse(node, results):
    if node is None:
        return results
    # Print node information.
    if(node.type=="call"):
        node_text = node.text.decode('utf-8')    
        #print('Called_Method: ',node_text)
        functionName = ''
        cnt = 0
        arg_string=''
        arg_list=[]
        for child in node.children:
            #print(child.type)
            if(child.type=="argument_list"):
                for args in child.children:
                    arg_string+=args.type
                    #print(arg_string)
                arg_string = arg_string.strip('()')
                arg_list = [item.strip() for item in arg_string.split(',')]
                cnt = len(arg_list)
                if(cnt==1 and len(arg_string)==0):
                    cnt=0
  
            if(child.type=="attribute"):
                functionName = (child.text.decode('utf-8'))
        
        fName = functionName.split('.').pop()
        #print('function name: ',fName)
        #print('argument count: ',cnt)
        helperInf = {
            "Syntax":node_text,
            "FunctionName":fName,
            "ArgsCount":cnt
        }
        results.append(helperInf)
    # Recursively traverse child nodes
    for child in node.children:
        traverse(child,results)
    return results



def extractHelpers(code):
    tree = parser.parse((code))
    root = tree.root_node
    helperInfo=[]
    return traverse(root,helperInfo)


# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.code_understanding

# Access the collection
methodsPython = db.methodsPython

#methodList=[]

# currentRepo = 'celery/celery'

# cnt=0

# for item in methods:
#     if(item.get("repo")==currentRepo):
#         methodList.append(item)
#         cnt+=1
#         #print(item)
#         if cnt == 3:
#             break

# client.close()


client = MongoClient('mongodb://localhost:27017/')
db = client.code_understanding             
#helperMethods = db.helperMethods


for file in methodsPython.find():
    methods = file.get("methods")
    try:
        for index, method in enumerate(methods):
            code = method.get("Syntax")          
            helpers = {
                "helpers":extractHelpers(code.encode('utf-8'))
            }
            #method["helpers"] = helpers
            #print(method)
            
            methodsPython.update_one(
                    {'_id': file.get('_id')},
                    {
                        "$set": {
                            f"methods.{index}.helpers": helpers
                        }
                    }
                )

        #helperMethods.insert_one(data)

    except Exception as e:
        print(f"Error inserting data: {e}")
    
    print("data added:",file.get("_id"))
    #break
