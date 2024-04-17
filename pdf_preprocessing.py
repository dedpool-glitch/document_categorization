import fitz  # PyMuPDF
import azure_api_call,db_filecheck,insert_data
import pandas as pd
import time

def preprocess_pdf(filepath):

    """
    This method is used for creating a dataframe for each pdf that is passed for the purpose of classification.

    Input: filepath of the pdf

    Output: A dataframe consisting of content column, whose each instance contains an array of strings, representing each page of the pdf.

    Process: For each pdf page, it is converted to an image, then paddleOCR model is used to detect text from it, the entire text per page is stored in an array, as an array.
    This content array is appended to a list, which is consequently converted to a dataframe.

    """
    pdf_document = fitz.open(filepath)
    content_array=[]
    for page_number in range(len(pdf_document)):
            page = pdf_document[page_number]
            pix = page.get_pixmap(dpi=300)
            image_path=f'{filepath}-{page_number}.jpg'
            pix.pil_save(image_path, optimize = False, dpi = (1000, 1000))
            result = azure_api_call.getOCR_output(image_path)
            page_array=[]
            page_array = [line.text for text_result in result.analyze_result.read_results for line in text_result.lines if line]
            page_array=','.join(page_array)
            content_array.append(page_array)
    data_list=[]
    for i in range(len(content_array)):
        data_list.append((content_array))
    table_df=pd.DataFrame(data_list)
    table_df=table_df.transpose()
    test_df=table_df.iloc[:,len(pdf_document)-1:]
    test_df.columns=['content']
    test_df.to_csv('test_output.csv')
    test_df=pd.read_csv('test_output.csv',usecols=['content'])
    return test_df
