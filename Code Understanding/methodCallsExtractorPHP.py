
from tree_sitter import Language, Parser
from pymongo import MongoClient
import sys
import time
 
sys.setrecursionlimit(10**6)


def instantiate_language(name):
    Language.build_library(f"libtree-sitter-php.so", ["/student/mjr175/method-level-comment-generation/tree-sitter-php/php"])
    return Language(f"/student/mjr175/method-level-comment-generation/tree-sitter-php/php/libtree-sitter-php.so", name)


# instantiate language
PHP = instantiate_language("php") 

# instantiate parser
parser = Parser()
parser.set_language(PHP)


def traverse(node, results):
    #print("called")
    if node is None:
        print('none')
        return results
    # Print node information.
    #print(node.type)
    if(node.type=="function_call_expression"):
        node_text = node.text.decode('utf-8')    
        print('Called_Method: ',node_text)
        functionName = []
        cnt = 0
        arg_string=''
        arg_list=[]
        for child in node.children:
            #print(child.type)
            if(child.type=="arguments"):
                for args in child.children:
                    arg_string+=args.type
                    #print(arg_string)
                arg_string = arg_string.strip('()')
                arg_list = [item.strip() for item in arg_string.split(',')]
                cnt = len(arg_list)
                if(cnt==1 and len(arg_string)==0):
                    cnt=0
  
            if(child.type=="name"):
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
methodsPHP = db.methodsPHP



client = MongoClient('mongodb://localhost:27017/')
db = client.code_understanding             
#helperMethods = db.helperMethods


for data in methodsPHP.find():
    methods = data.get("methods")
    
    try:
        for index, method in enumerate(methods):
            code = '<?php declare(strict_types=1);\n'
            code += method.get("Syntax")          
            helpers = {
                "helpers":extractHelpers(code.encode('utf-8'))
            }

            methodsPHP.update_one(
                {'_id': data.get('_id')},
                {
                    "$set": {
                        f"methods.{index}.helpers": helpers
                    }
                }
            )


    except Exception as e:
        print(f"Error inserting data: {e}")
    
    print("data updated:",data.get("_id"))
