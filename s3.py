#!./flask/Scripts/python
# aws s3 iteraction  module
import boto3
from botocore import errorfactory #.NoSuchBucket
import json
import logging

from config import s3_config

logger = logging.getLogger(__name__)
bucket_name = s3_config()
s3c = boto3.client('s3')
s3r = boto3.resource('s3')  # still now very aware what is the difference between resouce and client, but for educatin we can use both
def upload_file_stream(fs): 
    try:
        if s3r.Bucket(bucket_name).creation_date is None:
            CreateBucket(bucket_name);
        ret= s3c.upload_fileobj(fs, bucket_name, fs.filename)
    except errorfactory.ClientError as err:
        logger.exception(err)
        #err_code=err.response['Error']['Code']
        #if err_code=='NoSuchBucket':            CreateBucket(bucket_name)
        raise 
    expiresIn=7*24*60*60-1 # must be less than a week
    url = s3c.generate_presigned_url(
    ClientMethod='get_object',
    Params={'Bucket': bucket_name,'Key': fs.filename},
    ExpiresIn=expiresIn
    )
    return url

def CreateBucket(bucket_name):
    lambda_client = boto3.client('lambda', region_name='eu-central-1')
    lambda_payload = {"bucket_name":bucket_name}
    d = json.dumps(lambda_payload)
    #lambda_payload64 = base64.b64encode(s.encode('utf-8'))
    resp=lambda_client.invoke(FunctionName='arn:aws:lambda:eu-central-1:314847435785:function:CreateS3Bucket', 
                        InvocationType='RequestResponse',
                        Payload=d)
    #print(resp)

if __name__ == '__main__':
    CreateBucket('xzzzxadf')