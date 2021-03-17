#!./flask/Scripts/python
# relational database module
import psycopg2
from config import db_config
import json
import logging
SQL_GET_FILES='''SELECT sf.Id, sf.PublicUrl, sf.FileName, sf.Created_At FROM public.S3_Files sf;'''
SQL_SET_FILES="INSERT INTO public.S3_Files (PublicUrl, FileName) VALUES ('{0}','{1}')"

##inserts only, kind of log, no merge and unique by name

params = db_config()

def test_connect():
    """ Connect to the PostgreSQL database server """
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
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
def get_s3_files():
    """ query parts from the parts table """
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
        json_output = json.dumps(objects)
        return json_output
        #print("The number of parts: ", cur.rowcount)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        logging.exception("SOME DB lever error")
        return "exception has occured.."
    finally:
        if conn is not None:
            conn.close()

def set_s3_files(file_name, s3_url):
    conn = None
    try:
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        x=len(s3_url)
        sql=SQL_SET_FILES.format(s3_url, file_name) #todo - figure out how we can levarage parameters
        cur.execute(sql)       
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        logging.exception("SOME DB lever error")
        raise
        #return "exception has occured.."
    finally:
        if conn is not None:
            conn.commit()
            conn.close()



if __name__ == '__main__':
    output=test_connect();
    print(output);