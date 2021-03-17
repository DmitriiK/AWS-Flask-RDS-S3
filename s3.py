#!./flask/Scripts/python
# aws s3 iteraction  module
import boto3
from config import s3_config

bucket_name = s3_config()
s3 = boto3.client('s3')
def upload_file_stream(fs, file_name): 
    ret= s3.upload_fileobj(fs, bucket_name, file_name)
    return ret

if __name__ == '__main__':
    output=upload_file_stream("xxx", "xxx");
    print(output);