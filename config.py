
from configparser import ConfigParser

MAIN_CONFIG_FILE='settings.ini'

parser = ConfigParser()
parser.read(MAIN_CONFIG_FILE)

def get_config_value(section, key ):
    if parser.has_section(section):
        config_value=parser[section][key]
        return config_value
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

def db_config():
    # get section, default to postgresql
    section='postgresql'
    db = {}
    # for ubuntu it is not working for some reason ; return {'host': 'postges.cbzpdv2uvyom.eu-central-1.rds.amazonaws.com', 'database': 'AWS_Edu', 'user': 'postgres', 'password': 'ppostgres'}

    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return db

def s3_config( ):
    return get_config_value('s3',"bucket_name")


def sns_config( ):
    return get_config_value('sns',"bucket_name")


if __name__ == '__main__':
    print (s3_config())