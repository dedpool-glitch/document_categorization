import create_connection

def file_not_in_db(filepath):
    """
    this function checks if a particular image is already present in the db or not, and returns a boolean value
    """
    db_connection=create_connection.create_connection()
    cursor=db_connection.cursor()
    query = "SELECT COUNT(1) FROM train_document_details WHERE document_name = %s"
    cursor.execute(query, (filepath,))
    exists = cursor.fetchone()[0]
    db_connection.close()
    return exists == 0