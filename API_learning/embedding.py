import lmstudio as lms

model = lms.embedding_model("nomic-embed-text-v1.5")
tokens = model.tokenize("Hello World!")
embedding = model.embed("hi")
print(tokens)
print(embedding)
