import boto3
import pprint

cloudformation = boto3.client('cloudformation')

response_describe= cloudformation.describe_stacks(StackName="aws-cloud9-OnlineIDE-cb6def53bfd64aadb409d1aa552bb65a")
check= response_describe["Stacks"][0]
if "cloudformation" in response_describe["Stacks"][0] :
    print("yes")
else:
    print("no")
