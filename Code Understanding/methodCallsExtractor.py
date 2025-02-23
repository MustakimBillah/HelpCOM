
from tree_sitter import Language, Parser
from pymongo import MongoClient
import sys
 
sys.setrecursionlimit(10**6)


def instantiate_language(name):
    Language.build_library(f"{name}.so", ["/student/mjr175/method-level-comment-generation/"+name])
    return Language(f"/student/mjr175/method-level-comment-generation/java/{name}.so", name)


# instantiate language
JAVA = instantiate_language("java") 

# instantiate parser
parser = Parser()
parser.set_language(JAVA)

def traverse(node, results):
    if node is None:
        return results
    # Print node information.
    if(node.type=="method_invocation"):
        node_text = node.text.decode('utf-8')    
        #print('Called_Method: ',node_text)
        functionName = []
        cnt = 0
        arg_string=''
        arg_list=[]
        for child in node.children:
            if(child.type=="argument_list"):
                for args in child.children:
                    arg_string+=args.type
                arg_string = arg_string.strip('()')
                arg_list = [item.strip() for item in arg_string.split(',')]
                cnt = len(arg_list)
                if(cnt==1 and len(arg_string)==0):
                    cnt=0
  
            if(child.type=="identifier"):
                functionName.append(child.text.decode('utf-8'))
        #print('function name: ',functionName.pop())
        #print('argument count: ',cnt)
        helperInf = {
            "Syntax":node_text,
            "FunctionName":functionName.pop(),
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
methods = db.methods.find()

methodList=[]

currentRepo = 'elastic/elasticsearch'

for item in methods:
    if(item.get("repo")==currentRepo):
        print("skip")
    else:
        methodList.append(item)

client.close()


client = MongoClient('mongodb://localhost:27017/')
db = client.code_understanding             
helperMethods = db.helperMethods


for data in methodList:
    methods = data.get("methods")
    try:
        for method in methods:
            code = method.get("Syntax")          
            helpers = {
                "helpers":extractHelpers(code.encode('utf-8'))
            }
            method["helpers"] = helpers

        helperMethods.insert_one(data)

    except Exception as e:
        print(f"Error inserting data: {e}")
    
    print("data added:",data.get("_id"))
    #break
