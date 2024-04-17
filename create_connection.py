import mysql.connector
import constants

def create_connection():
    db_connection = mysql.connector.connect(
        host=constants.HOSTNAME,
        user=constants.DATABASE_USERNAME,
        password=constants.DATABASE_PASSWORD,
        database=constants.DATABASE_NAME  
    )
    return db_connection