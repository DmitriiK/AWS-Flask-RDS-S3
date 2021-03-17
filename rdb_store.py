#!./flask/Scripts/python
# relational database module
import psycopg2
from config import db_config
import json
import logging
SQL_GET_FILES='''SELECT sf."Id", sf."AWS_Identifier", sf."Created_At"
FROM public."S3_Files" sf;'''

def test_connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = db_config()
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
        params = db_config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(SQL_GET_FILES)

        rows = cur.fetchall()
        objects = [
            {
                'Id': row[0],
                'AWS_Identifier':row[1]
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


if __name__ == '__main__':
    output=get_s3_files();
    print(output);