#importing necessary libraries
import pandas as pd
import numpy as np
import nltk
from nltk.tokenize import RegexpTokenizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
import joblib
import sys
sys.path.append('../')
import constants
np.random.seed(12345)


def train_model():

    """
The train_model method is responsible for training our Random Forest Classifier on the existing train datasets that we have. It returns the trained model instance along
with a Count Vectorizer instance that we can use to create test features for any new data that comes in.

    """

    #this dataframe consists of samples of both kyc as well as not_kyc classes
    train_kyc_1=pd.read_csv(constants.kyc_paddleocr_datapath,usecols=['content','label'])
    train_kyc_2=pd.read_csv(constants.only_kyc,usecols=['content','label'])
    train_pa_1=pd.read_csv(constants.preauths_paddleocr_datapath,usecols=['content','label'])
    train_pa_2=pd.read_csv(constants.only_pre_auths,usecols=['content','label'])
    train_ecard=pd.read_csv(constants.only_ecards,usecols=['content','label'])
    train_ecard_2=pd.read_csv(constants.only_ecards_extra,usecols=['content','label'])
    train_ds=pd.read_csv(constants.only_ds_data,usecols=['content','label'])
    train_others_1=pd.read_csv(constants.others_1,usecols=['content','label'])
    train_others_2=pd.read_csv(constants.others_2,usecols=['content','label'])
    train_others_3=pd.read_csv(constants.others_3,usecols=['content','label'])
    train_others_4=pd.read_csv(constants.others_4,usecols=['content','label'])
    train_others_5=pd.read_csv(constants.others_5,usecols=['content','label'])

    df_1=pd.concat([train_pa_2,train_ecard,train_kyc_2,train_ecard_2])
    df_2=pd.concat([train_others_1,train_others_2,train_others_3,train_others_4,train_others_5])

    train_kyc_1=train_kyc_1[train_kyc_1['label']=='kyc']
    train_pa_1=train_pa_1[train_pa_1['label']=='pre_auth_form']

    train_combined_df=pd.concat([df_1,df_2,train_kyc_1,train_pa_1,train_ds])

    train_final=train_combined_df
    train_final.reset_index(drop=True)

    train_1=train_final
    nltk.download('stopwords')
    stop_words=nltk.corpus.stopwords.words("english")

    X_train, X_test, Y_train, Y_test = train_test_split(train_1['content'], train_1['label'], test_size=0.30, random_state=5,shuffle=True)

    #uses unigrams to create features and only considers the top 100 features.
    tokenizer = RegexpTokenizer(r'[a-zA-Z0-9]+')
    cv = CountVectorizer(stop_words='english',ngram_range = (1,1),tokenizer = tokenizer.tokenize,max_features=100)
    unigrams_count_train_1 = cv.fit_transform(X_train)

    #initializing a RFC with the optimal hyperparameters suggested by Grid Search
    rfc=RandomForestClassifier(random_state=5,max_depth= 30, max_features=10, min_samples_leaf= 2, min_samples_split=5, n_estimators= 50)
    rfc.fit(unigrams_count_train_1,Y_train)

    joblib.dump(rfc, "rfc.joblib")
    joblib.dump(cv, 'count_vectorizer.pkl')

train_model()
