from ollama import Client
llama_host = 'http://10.18.208.5:11433'

def ask(query_temp='', input_query='who are you?',model='codellama:7b-instruct'):
    
    client = Client(host=llama_host)
    query = query_temp + input_query
    response = client.chat(
        model=model,
        messages=[{ 'role': 'system', 'content': 'You are an expert Java developer.'}, 
                  {'role':'user', 'content': query}]
                  )

    return response['message']['content']

print(ask())