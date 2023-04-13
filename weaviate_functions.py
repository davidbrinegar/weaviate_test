import os
import json
import weaviate

def split_content(content, max_tokens):
    tokens = content.split()
    splits = []
    for i in range(0, len(tokens), max_tokens):
        splits.append(" ".join(tokens[i:i+max_tokens]))
    return splits

def create_schema(client):
    # Delete existing schema (if necessary - THIS WILL ALSO DELETE ALL OF YOUR DATA)
    client.schema.delete_all()

    # Fetch & inspect schema (should be empty)
    schema = client.schema.get()
    print(json.dumps(schema, indent=4))

    # Add schema
    class_obj = {
        "class": "Documentation",
        "vectorizer": "text2vec-openai"  # Or "text2vec-cohere" or "text2vec-huggingface"
    }
    client.schema.create_class(class_obj)

def import_data(client, file_path):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # Configure a batch process
    with client.batch as batch:
        batch.batch_size = 100
        # Batch import all data
        for i, d in enumerate(data):
            print(f"importing item: {i + 1}")

            content_splits = split_content(d["content"], 8190)  # Split content into parts

            for split_index, split in enumerate(content_splits):
                properties = {
                    "title": d["title"],
                    "content": split,
                    "split_part": split_index,
                }

                # Add the data object with the generated vector
                client.batch.add_data_object(properties, "Documentation")

    client.data_object.get()
