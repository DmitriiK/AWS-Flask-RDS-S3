
from configparser import ConfigParser

MAIN_CONFIG_FILE='settings.ini'

parser = ConfigParser()
parser.read(MAIN_CONFIG_FILE)
def db_config(filename=MAIN_CONFIG_FILE):
    # get section, default to postgresql
    section='postgresql'
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return db

def s3_config(filename=MAIN_CONFIG_FILE, ):
    section='s3'
    if parser.has_section(section):
        bucket_name=parser[section]["bucket_name"]
        return bucket_name
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return db