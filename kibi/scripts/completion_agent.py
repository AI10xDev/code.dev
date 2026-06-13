import os
import sys
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load credentials from ~/projects/email_graphs/.env
load_dotenv("/home/emmanuel/.env")

# Retrieve and clean up endpoint URL
endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
if endpoint and "/openai/v1" in endpoint:
    endpoint = endpoint.split("/openai/v1")[0]

client = AzureOpenAI(
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
    api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=endpoint
)

deployment_name = os.environ.get("DEPLOYMENT_NAME", "gpt-5.5")

def get_completion(context):
    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a code/text completion assistant. Your task is to output the characters/code "
                        "that should immediately follow the provided prefix code, to complete the line and/or subsequent lines. "
                        "Do NOT repeat the prefix, do NOT wrap your answer in markdown code blocks (like ```), "
                        "and do NOT include any introductory or explanatory text. Your response will be appended "
                        "directly to the prefix, so it must form a syntactically correct and logical continuation. "
                        "Provide ONLY the completion content."
                    )
                },
                {"role": "user", "content": f"Prefix code:\n{context}\n\nProvide the completion for the code after the prefix."}
            ]
        )
        text = response.choices[0].message.content
        if not text:
            return ""
        
        # Clean up code blocks if the model wrapped the response in them
        if text.startswith("```"):
            lines = text.splitlines()
            if len(lines) >= 2:
                if lines[-1].startswith("```"):
                    text = "\n".join(lines[1:-1])
                else:
                    text = "\n".join(lines[1:])
        return text
    except Exception as e:
        return f"Error: {e}"

# Simple protocol: read one line of context, output completion inside delimiters
for line in sys.stdin:
    if not line:
        continue
    # Decode double-escaped newlines and backslashes
    context = line.strip().replace("\\n", "\n").replace("\\\\", "\\")
    if context == "QUIT":
        break
    completion = get_completion(context)
    # Output completion, separated by a delimiter to handle multi-line returns
    print(f"COMPLETION_START\n{completion}\nCOMPLETION_END")
    sys.stdout.flush()
