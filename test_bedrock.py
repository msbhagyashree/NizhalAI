import boto3
from botocore.exceptions import ClientError

client = boto3.client("bedrock-runtime", region_name="ap-southeast-2")

try:
    response = client.converse(
        modelId="global.amazon.nova-2-lite-v1:0",
        messages=[
            {"role": "user", "content": [{"text": "Hello from NizhalAI"}]}
        ]
    )
    print(response["output"]["message"]["content"][0]["text"])

except ClientError as error:
    print("Error details:", error.response)