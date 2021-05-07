import json
import boto3
import base64



cloudformation = boto3.client('cloudformation')

def lambda_handler(event, context):
    
    print('Received request')
    
    #List all cloudformation stacks in the target aws account
    response_list_stack = cloudformation.list_stacks(StackStatusFilter=['CREATE_COMPLETE','UPDATE_COMPLETE'])
    output_stack = response_list_stack["StackSummaries"]
    
    stacks_output_list = [] 
    #Loop through each stack
    for i in output_stack:
        stack_name = i["StackName"]
    
        #Check each stack decription for output
        response_describe = cloudformation.describe_stacks(StackName=stack_name)
        
        #Extract the needed output from each stack with an output section.
        if "Outputs" in response_describe["Stacks"][0]:
            outputs = response_describe["Stacks"][0]["Outputs"]
            
            
            ChannelID=""
            CloudFrontHlsEndpoint=""
            MediaPackageHlsEndpoint=""
            MediaLivePrimaryEndpoint=""
            MediaLiveSecondaryEndpoint=""
            for output in outputs:
                if output["OutputKey"] == "MediaLiveChannelId":
                    ChannelID= output["OutputValue"]
                elif output["OutputKey"] == "CloudFrontHlsEndpoint":
                    CloudFrontHlsEndpoint = output["OutputValue"]
                elif output["OutputKey"] == "MediaPackageHlsEndpoint":
                    MediaPackageHlsEndpoint = output["OutputValue"]
                elif output["OutputKey"] == "MediaLivePrimaryEndpoint":
                    MediaLivePrimaryEndpoint = output["OutputValue"]
                elif output["OutputKey"] == "MediaLiveSecondaryEndpoint":
                    MediaLiveSecondaryEndpoint = output["OutputValue"]
                
            if  MediaLivePrimaryEndpoint and ChannelID and MediaLiveSecondaryEndpoint and CloudFrontHlsEndpoint  != "" :
                yaml_file = { "StackName" : stack_name, 
                "ChannelID":ChannelID, 
                "MediaLivePrimaryEndpoint": MediaLivePrimaryEndpoint,
                "MediaLiveSecondaryEndpoint" : MediaLiveSecondaryEndpoint,
                "CloudFrontHlsEndpoint": CloudFrontHlsEndpoint, 
                "MediaPackageHlsEndpoint": MediaPackageHlsEndpoint,
                }
                
                stacks_output_list.append(yaml_file)
                print(yaml_file)    
                    
               
    
    return {
        "statusCode": 200,
        "body": json.dumps(stacks_output_list),
        #"body": json.dumps(yaml_file),
    }