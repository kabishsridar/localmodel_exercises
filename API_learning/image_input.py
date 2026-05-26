import lmstudio as lms

image_path = "C:\\Users\\Omac Solution\\Pictures\\Screenshots\\lmstudio_settings.png" # Replace with the path to your image
image_handle = lms.prepare_image(image_path)
model = lms.llm("qwen/qwen3.5-35b-a3b")
chat = lms.Chat()
chat.add_user_message("Describe this image please", images=[image_handle])
prediction = model.respond(chat)