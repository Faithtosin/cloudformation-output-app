import json
import boto3
# import requests

import json
import base64
import boto3


cloudformation = boto3.client('cloudformation')

def lambda_handler(event, context):
    
    print('Received request')
    
    #List all cloudformation stacks in the target aws account
    response_list_stack = cloudformation.list_stacks(StackStatusFilter=['CREATE_COMPLETE','UPDATE_COMPLETE'])
    output_stack = response_list_stack["StackSummaries"]
    
    #Loop through each stack
    for i in output_stack:
        stack_name = i["StackName"]
    
        #Check each stack decription for output
        response_describe = cloudformation.describe_stacks(StackName=stack_name)
        
        #Extract the needed output from each stack with an output section.
        if "Outputs" in response_describe["Stacks"][0]:
            outputs = response_describe["Stacks"][0]["Outputs"]
            
            InputEndpoints = []
            ChannelID=""
            for output in outputs:
                if output["OutputKey"] == "MediaLiveChannelId":
                    ChannelID= "ChannelID: "+ output["OutputValue"]
                elif output["OutputKey"] == "MediaLivePrimaryEndpoint":
                    MediaLivePrimaryEndpoint = output["OutputValue"]
                    InputEndpoints.append(MediaLivePrimaryEndpoint)
                elif output["OutputKey"] == "MediaLiveSecondaryEndpoint":
                    MediaLiveSecondaryEndpoint = output["OutputValue"]
                    InputEndpoints.append(MediaLiveSecondaryEndpoint)
                
            if InputEndpoints and ChannelID != "" :
                yaml_file = { "Label" : stack_name,
                        "ChannelID":ChannelID ,
                           "InputEndpoints": InputEndpoints
                    }
                
                print(yaml_file)    
                    
                

    return {
        "statusCode": 200,
        "body": json.dumps(yaml_file),
    }