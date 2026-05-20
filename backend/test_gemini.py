import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

from google import genai

client = genai.Client()

result = client.models.embed_content(
    model="text-embedding-004",
    contents="hello world",
    config={"task_type": "RETRIEVAL_DOCUMENT"}
)

print(type(result))
print(type(result.embeddings))
if result.embeddings:
    print(type(result.embeddings[0]))
    print(type(result.embeddings[0].values))
    print(len(result.embeddings[0].values))
