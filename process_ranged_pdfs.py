import pandas as pd
from paddleocr import PaddleOCR
import fitz
import constants

input_path=input(constants.processing_input_prompt)
output_path=input(constants.processing_output_prompt)
df=pd.read_csv(input_path)                            #input path to the csv which contains indices which define the range of the document in question.
categories=[['discharge_summary','not_kyc']]                        #this can be applied to any of the document categories, just change your labels.


ocr = PaddleOCR(use_angle_cls=True, lang="ch",use_gpu=True)        #initializing the paddleOCR text recognition model.

def process_ranged_pdfs(df):

#all pdfs stored in the dataframe are taken one at a time. Each pdf is split into individual pages, and based on the range of the document specified, we have different loops, if the page lies outside the range,
#it is classified as not_<doc_category>, if it lies inside the range, it is classified as <doc_category>. We use paddleOCR to extract text from that page and append the results of each page into an array of strings.
#We then concatenate each of these arrays to the content array and assign the corresponding label to to label_array.
    
    label_array=[]
    content_array=[]
    for index,row in df.iterrows():
        values=row[['filepath','start_index','end_index']].to_list()
        values[0] = values[0].replace("\\", "/")
        pdf_document = fitz.open(values[0])
        """for page_number in range(values[1]):
            page = pdf_document[page_number]
            pix = page.get_pixmap(dpi=300)
            pix.pil_save(f'{values[0]}-{page_number}.jpg', optimize = False, dpi = (1000, 1000))
            page_content = ocr.ocr(f'{values[0]}-{page_number}.jpg', cls=True)
            page_array=[]
            for idx in range(len(page_content)):
                res = page_content[idx]
                if res==None:
                    continue
                else:
                    for line in res:
                        page_array.append(line[1][0])
            content_array.append(page_array)
            label_array.append(categories[0][1])"""

        for page_no in range(values[1],values[2]+1):
            page = pdf_document[page_no]
            pix = page.get_pixmap(dpi=300)
            pix.pil_save(f'{values[0]}-{page_no}.jpg', optimize = False, dpi = (1000, 1000))
            page_content = ocr.ocr(f'{values[0]}-{page_no}.jpg', cls=True)
            page_array=[]
            for idx in range(len(page_content)):
                res = page_content[idx]
                if res==None:
                    continue
                else:
                    for line in res:
                        page_array.append(line[1][0])
            content_array.append(page_array)
            label_array.append(categories[0][0])

        """for pg_no in range(values[2]+1,pdf_document.page_count):
            page = pdf_document[pg_no]
            pix = page.get_pixmap(dpi=300)
            pix.pil_save(f'{values[0]}-{pg_no}.jpg', optimize = False, dpi = (1000, 1000))
            page_content = ocr.ocr(f'{values[0]}-{pg_no}.jpg', cls=True)
            page_array=[]
            for idx in range(len(page_content)):
                res = page_content[idx]
                if res==None:
                    continue
                else:
                    for line in res:
                        page_array.append(line[1][0])
            content_array.append(page_array)
            label_array.append(categories[0][1])"""
    

    return content_array,label_array

content,label=process_ranged_pdfs(df)

data_list=[]
for i in range(len(label)):
    data_list.append((content[i],label[i]))

#we stack the content and label arrays together in a tuple and create an array of tuples eventually.
#then we proceed to create a dataframe with this array of tuples and assign 2 columns to it.



table_df=pd.DataFrame(data_list,columns=['content','label'])
#saves your dataframe in csv format at the specified location.
table_df.to_csv(constants.generic_datapath+output_path)             