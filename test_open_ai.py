import openai

# Set your OpenAI API key
openai.api_key = "SECRET KEY REMOVED FOR COMMIT AND PUSH TO GITHUB"
# Make a request to the OpenAI API
response = openai.ChatCompletion.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, world!"}
    ]
)

# Print the response
print(response["choices"][0]["message"]["content"])