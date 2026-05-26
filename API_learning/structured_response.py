import lmstudio as lms

api_host = lms.Client.find_default_local_api_host()

client = lms.Client(api_host)

model = client.llm.model("qwen/qwen3.5-35b-a3b")

schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "author": {"type": "string"},
        "year": {"type": "integer"}
    },
    "required": ["title", "author", "year"]
}

prediction_stream = model.respond_stream("Tell me about The Hobbit", response_format=schema)

# Optionally stream the response
# for fragment in prediction:
#   print(fragment.content, end="", flush=True)
# print()
# Note that even for structured responses, the *fragment* contents are still only text

# Get the final structured result
result = prediction_stream.result()
book = result.parsed

print(book)
#           ^
# Note that `book` is correctly typed as { title: string, author: string, year: number }

print(book)