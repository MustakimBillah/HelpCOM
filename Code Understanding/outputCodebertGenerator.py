import json

# Define file paths
jsonl_file_path = '/u2/users/mjr175/codeBert/CodeXGLUE/Code-Text/code-to-text/dataset/java/cBertInput.jsonl'
output_file_path = '/u2/users/mjr175/codeBert/CodeXGLUE/Code-Text/code-to-text/code/model/java/test_0.output'
new_jsonl_file_path = '/u2/users/mjr175/codeBert/CodeXGLUE/Code-Text/code-to-text/dataset/java/cBertOutput.jsonl'

# Read the .output file (extracting text after the tab)
with open(output_file_path, 'r') as output_file:
    output_values = [line.split('\t', 1)[1].strip() for line in output_file.readlines()]

# Open the .jsonl file and read the content
with open(jsonl_file_path, 'r') as jsonl_file:
    json_lines = [json.loads(line) for line in jsonl_file.readlines()]

# Update the JSON objects with the corresponding values from the .output file
# Assuming both files have corresponding entries line by line
for i, json_object in enumerate(json_lines):
    if i < len(output_values):
        # Update the JSON object with the value from the output file
        json_object['summary'] = output_values[i]

# Write the updated JSON objects back to the .jsonl file
with open(new_jsonl_file_path, 'w') as jsonl_file:
    for json_object in json_lines:
        jsonl_file.write(json.dumps(json_object) + '\n')

print(f"Updated {jsonl_file_path} with values from {new_jsonl_file_path}")
