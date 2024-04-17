#importing scripts
from dataset_creation import pdf_preprocessing
from Testing import get_model_predictions
from Testing import get_output_array
from Testing import save_csv
from NER_CODE import mainPy
import joblib
import os
import constants

def main():

    """
   The Main function is used for the complete pre-processing and classification process of a pdf.

   It takes in a file path as input, trains our model on the existing dataset, returns the model and vectorizer instance to create features. 
   We pass our filepath to a pre-processing function, which returns a dataframe as output.
   This dataframe is passed along with our trained model and the vectorizer to a function which returns the predictions.
   We pass the predictions along with their confidence to get_confidence_array which returns an output dataframe consisting of categories, page no. and confidence scores.
   
    """
    directory_path= constants.directory_path
    for file in os.scandir(directory_path):
        if file.is_file():

            model=joblib.load(constants.rfc_model_state)
            cv=joblib.load(constants.cv_instance)
            test_df=pdf_preprocessing.preprocess_pdf(file.path)
            preds,preds_prob,raw_content=get_model_predictions.get_predictions(test_df['content'],cv,model)
            confidence_array=get_output_array.confidence_array(preds_prob)
            output_df,filename=save_csv.save_to_csv(file.name,confidence_array,raw_content)
            #mainPy.main(output_df,filenam) => call to NER's main script

main()