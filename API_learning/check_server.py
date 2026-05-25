import lmstudio as lms
SERVER_API_HOST = "localhost:1234"
#the method is_valid_api_host from he Client class will return whether the 
if lms.Client.is_valid_api_host(SERVER_API_HOST):
    print(f"An LM Studio API server instance is available at {SERVER_API_HOST}")
else:
    print("No LM Studio API server instance found at {SERVER_API_HOST}")