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
topic = sns_client.create_topic(Name=topic_name) ##returns exising if topic with such name exists 
TopicArn=topic['TopicArn']

def list_subscriptions():
    response = sns_client.list_subscriptions_by_topic(
        TopicArn=TopicArn,
        ##NextToken='string' ##assuming we have not more than 100 subsriptions
    )
    return response

def subscribe(email):

    response = sns_client.subscribe(
        TopicArn=TopicArn,
        Protocol='email',
        Endpoint=email,
        ReturnSubscriptionArn=True
    )
    
    return response['SubscriptionArn'];
def un_subscribe(email):
    sbs=list_subscriptions()['Subscriptions']
    unsbs= [s['SubscriptionArn'] for s in sbs if s['Endpoint']==email and s['Protocol']=='email']
    if len(unsbs)>0:
        arn=unsbs[0]
        try:
            sns_client.unsubscribe(SubscriptionArn=arn)
        except ClientError:
            logger.exception("Couldn't unsubscribe for arn= {}".format(arn))
            raise Exception("Couldn't unsubscribe for arn={}".format(arn))
    #  You can't delete a pending confirmation. After 3 days, Amazon SNS deletes it  
    return len(unsbs) 
