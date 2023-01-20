import boto3
import json

client = boto3.client("lambda")

print("Running Test")
print("Memoory, download, upload")

for memorysize in range(256, 10*1024, int((10*1024-256)/5)):

    response = client.update_function_configuration(
        FunctionName='netspeed',
        MemorySize=memorysize
    )
    waiter = client.get_waiter('function_updated')
    waiter.wait(FunctionName='netspeed')

    response = client.invoke(
        FunctionName='netspeed',
        InvocationType='RequestResponse'
    )

    response_payload = json.loads(response['Payload'].read().decode("utf-8"))
    body = json.loads(response_payload['body'])
    print(body['memory_limit_in_mb'], body['download'],  body['upload'], sep=", ")
