import ast

from pymongo import MongoClient

def extract_goal_from_docstring(method_code):
    """
    Extract only the goal part (first line) of the docstring from a given method's code.

    Args:
        method_code (str): The code of the method as a string.

    Returns:
        str: The extracted goal part or a message indicating no docstring.
    """
    try:
        # Parse the code into an abstract syntax tree (AST)
        tree = ast.parse(method_code)
        
        # The first node in the body should be a function definition
        if isinstance(tree.body[0], ast.FunctionDef):
            docstring = ast.get_docstring(tree.body[0])
            if docstring:
                # Return only the first line (goal part)
                return docstring.strip().split("\n")[0]
            else:
                return ""
    except Exception as e:
        print(f"Error parsing code: {e}")
        return ""
    
    return ""



client = MongoClient('mongodb://localhost:27017/')
db = client.code_understanding             
pythonMethods = db.methodsPython



for item in pythonMethods.find():
    methods = item.get('methods')

    for index, method in enumerate(methods):
        methodBody = method.get('Syntax')
        docstring = extract_goal_from_docstring(methodBody)
        
        pythonMethods.update_one(
                    {'_id': item.get('_id')},
                    {
                        "$set": {
                            f"methods.{index}.Docstring": docstring
                        }
                    }
                )

print("done processing")

# total=0
# cnt=0

# for item in pythonMethods.find():
#     methods = item.get('methods')

#     for index, method in enumerate(methods):
#         methodBody = method.get('Syntax')
#         docstring = extract_goal_from_docstring(methodBody)
#         total+=1
#         if len(docstring)>0:
#             cnt+=1

# print("toal: ",total)
# print("cnt: ",cnt)