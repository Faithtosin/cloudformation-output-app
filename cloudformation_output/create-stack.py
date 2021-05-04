import json
import base64
import boto3
import os


client = boto3.client('cloudformation')
TemplateURL="https://klic-livestream-deployment-us-east-1.s3.amazonaws.com/live-streaming-on-aws/v2.5.4/live-streaming-on-aws.template"

Stack_Name= os.environ['STACKNAME']
Stack_Num= os.environ['STACKNUMBER']
i= 1
while i <= int(Stack_Num):
    response = client.create_stack(
        StackName= Stack_Name + "-" + str(i),
        TemplateURL=TemplateURL,
        
        #TimeoutInMinutes=123,
        Capabilities=[
            'CAPABILITY_IAM','CAPABILITY_NAMED_IAM','CAPABILITY_AUTO_EXPAND',
        ]
        #OnFailure='DO_NOTHING'|'ROLLBACK'|'DELETE',
    )

    print(response)

    i+=1
