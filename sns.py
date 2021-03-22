#!./flask/Scripts/python
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Purpose

Shows how to use the AWS SDK for Python (Boto3) with Amazon Simple Notification
Service (Amazon SNS) to create notification topics, add subscribers, and publish
messages.
"""

import json
import logging
import time
import boto3
from botocore.exceptions import ClientError
from config import sns_config

logger = logging.getLogger(__name__)

topic_name = sns_config()

sns_client = boto3.client('sns')
##sns = boto3.resource('sns')





class SNS_Subscription:
    def subscribe(email):
        topic = sns_client.create_topic(Name=topic_name) ##returns exising if topic with such name exists 
        TopicArn=topic['TopicArn']
        response = sns_client.subscribe(
            TopicArn=TopicArn,
            Protocol='email',
            Endpoint=email,
            ReturnSubscriptionArn=True
        )
        
        return response['SubscriptionArn'];
    def un_subscribe(email):
        return 'not impmelemnted yet'   






if __name__ == '__main__':
    usage_demo()
