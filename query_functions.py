import weaviate
import json

def create_weaviate_client(api_key, weaviate_url, openai_api_key):
    auth_config = weaviate.auth.AuthApiKey(api_key=api_key)
    client = weaviate.Client(
        url=weaviate_url,
        auth_client_secret=auth_config,
        additional_headers={
            "X-OpenAI-Api-Key": openai_api_key
        }
    )
    return client

def get_documentation_with_concepts(client, concepts, limit=1, certainty=0.7):
    result = (
        client.query
        .get("Documentation", ["title","split_part"])
        .with_near_text({
            "concepts": concepts,
            "operator": "like",
            "certainty": certainty
        })
        .with_limit(limit)
        .do()
    )
    return result
