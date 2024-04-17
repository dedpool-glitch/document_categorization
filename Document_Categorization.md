# Documentation

* **Problem Statement**: During the Claim Process, a certain set of scanned documents are submitted by the hospitals on the customers' behalf, to enable the TPAs to validate/invalidate the claim request submitted by the customer. These documents can be Pre-auth forms, Consultation Papers, ID Proofs, Policy Copies, Vidal ID Cards, and Admission Notes (for the initial stage, these documents are usually submitted). In the enhancement stage of the claim process, we encounter Discharge Summaries, Implant Stickers, Final Bills, OT Notes, Nursing notes, etc. Therefore, in Document Categorization, our objective is to develop an ML Model that can identify various categories of documents mentioned above to speed up the claim process.

* **Data Source**: The company had an Oracle database resource of Network Claims for IPD (In-patient diagnosis) and an OPD folder for OPD (Out-patient documents). The training and testing samples were collected from there.

* **Dataset Creation**- The dataset creation procedure is generic for all document categories. Since all the submitted documents were initially scanned images before being converted to PDFs, we chose to use OCR Engines to recognize text from these PDFs. Currently, our dataset has a total of 1134 samples, somewhat balanced across 5 categories: Pre_auth forms, KYC docs, ecard, Discharge Summaries, and an Others category. We split each pdf page-wise, convert each page to an image, and consequently assign a category to that image. At the same time, the PaddleOCR engine was used to extract text from these pages, and we ended up with a dataset containing 2 columns, content & label, for each category of document. The script for this can be found [here](dataset_creation/process_ranged_pdfs.py).

## Pre-processing, Model Training & Evaluation:

* **Pre-processing**: Once we have the dataset, we remove the stopwords present in each instance of the dataset, and convert all of the features to lowercase.
  
* **Feature-creation**: Based on an iterative trial and error process, we either go ahead with the TF-IDF method of creating features or use a Bag-of-Words model.
  
* **Model Training**: The dataset was split following the 70-30 train-test split. There were around 341 samples for testing and the rest for training. For model training, the Random Forest Classifier was used with the grid_search_cv method, cv set to 10, and evaluation metric set to accuracy. Grid Search returned the following optimal hyperparameter values:

   * Best Parameters:  {'max_depth': 30, 'max_features': 10, 'min_samples_leaf': 2, 'min_samples_split': 5, 'n_estimators': 50}
   * Data Split: 341 test samples, (pa_count,ecard_count,kyc_count,others_count,ds_count)=(91 53 67 63 67)

* ** Evaluation Metrics**: The results were as follows, you can go through the confusion matrix given below:
   
   * On 341 samples, the classification report can be seen below:
     precision    recall  f1-score   support

          ds       0.99      0.99      0.99        67
       ecard       0.88      0.85      0.87        53
         kyc       0.79      0.90      0.84        67
      others       0.97      0.92      0.94        63
    pre_auth       1.00      0.96      0.98        91

    accuracy                           0.93       341
   macro avg       0.92      0.92      0.92       341
weighted avg       0.93      0.93      0.93       341
   
   * Train accuracy= 0.9596469104665826
   *  Test_accuracy= 0.9266862170087976
 













 



