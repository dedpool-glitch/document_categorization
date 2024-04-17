import numpy as np

def get_predictions(data,cv,rfc):

    """
    
    This method is used to obtain predictions from our trained model.

    Input: test data, a Count Vectorizer instance fitted on our training dataset, and the trained model instance.

    Output: category-wise predictions and confidence scores for each category for each page.

    """
    test=cv.transform(data)
    np.random.seed(12345)
    pred_rfc_test=rfc.predict(test)
    pred_prob=rfc.predict_proba(test)
    return pred_rfc_test,pred_prob,data