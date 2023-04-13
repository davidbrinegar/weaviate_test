import os, weaviate, json


api_tkn = "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"
auth_config = weaviate.auth.AuthApiKey(api_key="Sj3CzKRdC7wg0oDwrGSiaKOzobC2qKOjmbqk")  # Replace w/ your API Key for the Weaviate instance

# Instantiate Weaviate client
client = weaviate.Client(
    url="https://gablivia--eagleai-dev-k6qpkg84.weaviate.network",
    auth_client_secret=auth_config,
    additional_headers={
        "X-OpenAI-Api-Key": api_tkn  # Or "X-Cohere-Api-Key" or "X-HuggingFace-Api-Key"
    }
)

# Delete existing schema (if necessary - THIS WILL ALSO DELETE ALL OF YOUR DATA)
client.schema.delete_all()

# Fetch & inspect schema (should be empty)
schema = client.schema.get()
print(json.dumps(schema, indent=4))

# ===== add schema ===== 
class_obj = {
    "class": "Question",
    "vectorizer": "text2vec-openai"  # Or "text2vec-cohere" or "text2vec-huggingface"
}

client.schema.create_class(class_obj)

# ===== import data ===== 
# Load data from GitHub
import requests
url = 'https://raw.githubusercontent.com/weaviate/weaviate-examples/main/jeopardy_small_dataset/jeopardy_tiny.json'
resp = requests.get(url)
data = json.loads(resp.text)

# Configure a batch process
with client.batch as batch:
    batch.batch_size=100
    # Batch import all Questions
    for i, d in enumerate(data):
        print(f"importing question: {i+1}")

        properties = {
            "answer": d["Answer"],
            "question": d["Question"],
            "category": d["Category"],
        }

        client.batch.add_data_object(properties, "Question")

client.data_object.get()

nearText = {"concepts": ["airplane"]}

result = (
    client.query
    .get("Question", ["question", "answer", "category"])
    .with_near_text(nearText)
    .with_limit(2)
    .do()
)

print(json.dumps(result, indent=4))
