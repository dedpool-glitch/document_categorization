import numpy as np


def confidence_array(proba_predictions):
    
    """
    This method takes input as category wise confidence scores for each page and returns: a confidence array whose each element contains:
            
    1. Page No.
    2. Category predicted
    3. Confidence score for that category

    """
    confidence_array=[]
    for i in range(len(proba_predictions)):
        max_element=np.max(proba_predictions[i])
        max_element_index=np.argmax(proba_predictions[i])
        if max_element_index==0:
            confidence_array.append([i+1,'ds',max_element])
        elif max_element_index==1:
            confidence_array.append([i+1,'ecard',max_element])
        elif max_element_index==2:
            confidence_array.append([i+1,'kyc',max_element])
        elif max_element_index==3:
            confidence_array.append([i+1,'others',max_element])
        else:
            confidence_array.append([i+1,'pre_auth',max_element])

    return confidence_array