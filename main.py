import os, weaviate, json
from weaviate_functions import create_schema, import_data
from query_functions import create_weaviate_client, get_documentation_with_concepts


# OpenAI Token
api_tkn = "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"

# Weaviate Auth
auth_config = weaviate.auth.AuthApiKey(api_key="Sj3CzKRdC7wg0oDwrGSiaKOzobC2qKOjmbqk")  # Replace w/ your API Key for the Weaviate instance

# Instantiate Weaviate client
client = weaviate.Client(
    url="https://gablivia--eagleai-dev-k6qpkg84.weaviate.network",
    auth_client_secret=auth_config,
    additional_headers={
        "X-OpenAI-Api-Key": api_tkn  # Or "X-Cohere-Api-Key" or "X-HuggingFace-Api-Key"
    }
)

# # Create schema
# create_schema(client)

# # Import data
# file_path = './data/preprocessed/documentation/documentation.json'
# import_data(client, file_path)

# Query
concepts = "Looker 22.3"
result = get_documentation_with_concepts(client, concepts, limit=1, certainty=0.8)
print(json.dumps(result, indent=4))
