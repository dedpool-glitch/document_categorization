import create_connection
def insert_document_details(image_path, page_number, page_content,actual_category):
    """
    this function adds the arguments as values to the train_document_details table present in the db.
    
    """
    insert_query = """INSERT INTO train_document_details (document_name, page_no,raw_content, actual_category) 
                      VALUES (%s, %s, %s, %s)"""
    db_connection=create_connection.create_connection()
    cursor=db_connection.cursor()
    cursor.execute(insert_query, (image_path, page_number, page_content,actual_category))
    db_connection.commit()
    db_connection.close()