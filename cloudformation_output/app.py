import json
import yaml
import boto3
import base64



cloudformation = boto3.client('cloudformation')

def lambda_handler(event, context):
    
    print('Received request')
    
    #List all cloudformation stacks in the target aws account
    response_list_stack = cloudformation.list_stacks(StackStatusFilter=['CREATE_COMPLETE','UPDATE_COMPLETE'])
    output_stack = response_list_stack["StackSummaries"]
    
    stacks_output_list = []
    
    
    decklink_device=1
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
                slug="Channel"+str(decklink_device)
                label= "Klic Channel "+str(decklink_device)
                device= "Klic "+str(decklink_device)
                yaml_list ={'Slug':slug, 
                'Label':label,
                'MediaLive':{'ChannelID': ChannelID,'InputEndpoints':[MediaLivePrimaryEndpoint,MediaLiveSecondaryEndpoint]},
                'MediaPackage':{'PlaylistUrl':MediaPackageHlsEndpoint},
                'DeckLinkDevice': device,
                'DeckLinkInput': 'sdi'
                }
    
                
                stacks_output_list.append(yaml_list)
                #stacks_output_list.insert(0,yaml_list)
                
                final_file={'Streams':stacks_output_list}
                #print(yaml.dump(final_file))    
                
                decklink_device += 1
               
    
    return {
        "statusCode": 200,
        "body": yaml.dump(final_file),
        #"body": json.dumps(yaml_file),
    }