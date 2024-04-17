from sklearn.metrics import confusion_matrix
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
import seaborn as sns


def show_eval_metrics(Y_test,Y_pred,categories):
    """

    This method is used to compute some evaluation metrics to help make decisions on model performance.

    Input: Y_test (actual values), Y_pred (predicted values), categories 

    Output: prints a confusion matrix in the form of a heatmap, alongwith a classification report showing precision, recall and test accuracy as well.

    """
    
    cm_rfc=confusion_matrix(Y_test,Y_pred)
    sns.heatmap(cm_rfc, 
            annot=True,
            fmt='g', 
            xticklabels=categories,
            yticklabels=categories)
    plt.ylabel('Actual',fontsize=13)
    plt.xlabel('Prediction',fontsize=13)
    plt.title('Confusion Matrix',fontsize=17)
    plt.show()
    
    print(classification_report(Y_test, Y_pred, target_names=categories))
    #printing train and test accuracies
    accuracy_score_rfc=metrics.accuracy_score(Y_pred,Y_test)
    print("Test accuracy_RandomForest= ",accuracy_score_rfc)

