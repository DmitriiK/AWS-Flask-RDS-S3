#!./flask/Scripts/python
# aws s3 iteraction  module
import boto3
from botocore import errorfactory #.NoSuchBucket
import json

from config import s3_config

bucket_name = s3_config()
bucket_name='nonexistingbucket3'
s3 = boto3.client('s3')
def upload_file_stream(fs): 
    try:
        ret= s3.upload_fileobj(fs, bucket_name, fs.filename)
    except errorfactory.ClientError as err:
        print(err)
        err_code=err.response['Error']['Code']
        if err_code=='NoSuchBucket':
            CreateBucket(bucket_name)
            ret= s3.upload_fileobj(fs, bucket_name, fs.filename) #one more try
        else:
            raise 
    expiresIn=7*24*60*60-1 # must be less than a week
    url = s3.generate_presigned_url(
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