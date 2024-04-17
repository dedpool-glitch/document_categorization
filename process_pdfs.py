import fitz  # PyMuPDF
import azure_api_call,db_filecheck,insert_data
import pandas as pd
import time

def process_ranged_pdfs():
    """
    input: takes in 2 inputs, one is the category with which you want to annotate the corresponding pages, and second is the csv which contains page_ranges of the
    specified doc_category in each pdf that is passed to it. 

    This function splits pdf page by page, goes to the specified index range, and checks if that particular image is present in our db. If yes, it does not do anything.
    If no, it calls azure OCR API, extracts raw content, and adds it along with img_name, page_number and actual_category to the table in our db.
    """
    category_val=input("Enter category whose data you want to annotate:")
    categories=[category_val]  
    df_path=input("Enter df path:")
    df=pd.read_csv(df_path)

    for index, row in df.iterrows():
        values=row[['filepath','start_index','end_index']].to_list()
        #values[0] = values[0].replace("\\", "\")
        pdf_document = fitz.open(values[0])
        
        for page_number in range(values[1], values[2] + 1):
            page = pdf_document[page_number]
            image_path=f'{values[0]}-{page_number}.jpg'
            # Check if the image_path exists in the database
            if db_filecheck.file_not_in_db(image_path):
                page_array=[]
                pix = page.get_pixmap(dpi=300)
                pix.pil_save(image_path, optimize = False, dpi = (1000, 1000))
                result = azure_api_call.getOCR_output(image_path)
                page_array = [line.text for text_result in result.analyze_result.read_results for line in text_result.lines if line]
                page_array=','.join(page_array)
                insert_data.insert_document_details(image_path,page_number,page_array,categories[0])
                print("data inserted successfully")
            else:
                print("identical records found")
                continue
            time.sleep(10)
process_ranged_pdfs()


