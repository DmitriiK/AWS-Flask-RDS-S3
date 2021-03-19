#!./flask/Scripts/python
# relational database module
import psycopg2
from config import db_config
import json
import logging

##SQL QUERIES
SQL_GET_FILES='SELECT sf.Id, sf.PublicUrl, sf.FileName, sf.Created_At FROM public.S3_Files sf'
SQL_GET_FILE_BY_NAME=SQL_GET_FILES+" WHERE sf.FileName LIKE %s ORDER BY sf.Created_At DESC LIMIT 1"

SQL_GET_RANDOM_FILE='''WITH aggr AS (
	SELECT MAX(sf.Id) AS ID 
		FROM public.S3_Files sf
		GROUP BY sf.FileName
	)
SELECT sf.id,  sf.PublicUrl, sf.FileName, sf.Created_At 
FROM aggr
JOIN public.S3_Files sf on sf.Id=aggr.Id
ORDER BY RANDOM() LIMIT 1'''

SQL_SET_FILES="INSERT INTO public.S3_Files (PublicUrl, FileName) VALUES (%s,%s)"
##inserts only, kind of log, no merge and unique by name
###

params = db_config()

logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s -%(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.ERROR)
# for some reason for ubuntu we should write absolute path wothout first slash:  filename='home/ubuntu/flaskapp/app.log'
def test_connect():
    """ Connect to the PostgreSQL database server """
    logging.error("test log")
    conn = None
    try:
        # read connection parameters
        conn = psycopg2.connect(**params)		
        # create a cursor
        cur = conn.cursor()
        cur.execute('SELECT version()')
        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        return db_version[0]
       
	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
def get_s3_files():
    conn = None
    try:
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(SQL_GET_FILES)

        rows = cur.fetchall()
        objects = [
            {
                'Id': row[0],
                'PublicUrl':row[1]
                # 'Created_At':row[2] #Object of type datetime is not JSON serializable
            } for row in rows
        ] #
        json_output = json.dumps(objects, indent=4, sort_keys=True)
        return json_output
        #print("The number of parts: ", cur.rowcount)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        logging.exception("SOME DB lever error")
        raise
        #return "exception has occured.."
    finally:
        if conn is not None:
            conn.close()

def get_single_s3_file(file_name=None):
    conn = None
    try:
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        if (file_name==None):
            cur.execute(SQL_GET_RANDOM_FILE)
        else:
             cur.execute(SQL_GET_FILE_BY_NAME,(file_name,))
        rows = cur.fetchone()
        if (rows==None): return None
        return rows[1]
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        logging.exception("SOME DB lever error")
        raise
        #return "exception has occured.."
    finally:
        if conn is not None:
            conn.close()

def set_s3_files(file_name, s3_url):
    conn = None
    try:
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        x=len(s3_url)
        cur.execute(SQL_SET_FILES, (s3_url, file_name,) )       
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        logging.exception("SOME DB lever error in set_s3_files method s3_url=%s, filename=%s",s3_url, file_name)
        raise
        #return "exception has occured.."
    finally:
        if conn is not None:
            conn.commit()
            conn.close()



if __name__ == '__main__':
    output=test_connect();
    print(output);