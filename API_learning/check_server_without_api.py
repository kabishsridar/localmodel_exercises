import lmstudio as lms

# this gives the sdk value
api_host = lms.Client.find_default_local_api_host()

if api_host is not None:
    print(f"An LM Studio API server instance is available at SDK: {api_host}")
else:
    print("No LM Studio API server instance found on any of the default local ports")