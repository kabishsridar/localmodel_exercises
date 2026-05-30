import lmstudio as lms

model = lms.llm()
""" for fragment in model.respond_stream("Hi"):
    print(fragment.content, end="", flush=True)
print() """

chat =  lms.Chat("You are my friend.")
chat.add_user_message("Hi")
#result = model.respond(chat)

result = model.respond("Hi", config={
    "temperature":0.6,
    "maxTokens": 50
})

print(result)
# After iterating through the prediction fragments,
# the overall prediction result may be obtained from the stream
print("Model used:", result.model_info.display_name)
print("Predicted tokens:", result.stats.predicted_tokens_count)
print("Time to first token (seconds):", result.stats.time_to_first_token_sec)
print("Stop reason:", result.stats.stop_reason)