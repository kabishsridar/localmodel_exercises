import lmstudio as lms
model = lms.llm()

prediction_stream = model.respond_stream("What is the meaning of life?")
cancelled = False
for fragment in prediction_stream:
    if ...: # Cancellation condition will be app specific
        cancelled = True
        prediction_stream.cancel()
        # Note: it is recommended to let the iteration complete,
        # as doing so allows the partial result to be recorded.
        # Breaking the loop *is* permitted, but means the partial result
        # and final prediction stats won't be available to the client
# The stream allows the prediction result to be retrieved after iteration
if not cancelled:
    print(prediction_stream.result())