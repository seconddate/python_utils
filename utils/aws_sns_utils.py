import boto3
import json
import os

with open(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")) + '/config/config.json', 'r') as f:
    config = json.load(f)

class AwsSnsUtils():
    
    def __init__(self):
        self.sns = boto3.resource('sns')
        self.topic = self.sns.Topic(config['DEVOPS_SNS_ARN'])
        
    def publish(self, subject, message):
        response = self.topic.publish(
            Message=message,
            Subject=subject,
            MessageStructure='string'
        )
