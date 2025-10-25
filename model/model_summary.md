# Model Evaluation Summary

This summary outlines the results from the notebook [model.ipynb](model.ipynb), in which several models were trained and evaluated based on their predictive performance. The outcomes are subsequently analyzed and discussed.

## 1. Overview

**Goal**: Train a ML model to predict genuine (0) or malicious (1) network trafic (Binary Classification) for an IDS

---
**Evaluation metrics**: 
1.  `Accuracy`:  Proprotion of all correct classifications (0 and 1)
2.  `Precision`: Proportion of all malicious (1) detections that were correct
3.  `Recall`:    Proportion of all malicious (1) cases that were correctly detected

Accuracy gives a general overview of the model performance. In unbalanced dataset it can be misleading, but this is not the case here. Additionally looking at precision and recall metrics provides useful insight.  
-   When it is preferred that detections are correct -->  opt for high precision (with increased risk to miss malicious traffic)
-   When it is preferred to detect as many cases as possible --> opt for high recall (with increased risk for false alarms)

---

**Model evaluation**: 

- How accurately can a model detect malicious network trafic (1)?
-  Does the model perform equally well on unseen data?
    -   Dataset comparison `train vs test`: Compare model performance between the dataset the model was trained on and a new dataset.

-   Class distribution in both datasets: 


|Class | Train |Test| 
|:------:|:--------:|:--------:|
|0|67343 |9711|
|1|58630 (47%)|12833 (56%)|
|Total| 125973|22544|

**Model comparison**: 

-   Which model performes best? 
-   Compare how accurately different models can detect malicious network traffic (1).
-   Four simple `Baseline Models (BM)` were created as a benchmark for more complex `Random Forest Models (RF)`. 



## 2. Baseline Models (BM)

### Description
| Model | Description |
|:------|:--------|
|`BM_malicious` |   Always predict class 1 (malicious network traffic)|
|`BM_genuine`   |   Always predict class 0 (genuine network traffic)|
|`BM_random`    |   Randomly predict class 0 or 1|
|`BM_protocol`  |   Predict class 1 when the protocol type is 'imcp' </br>(simple heuristic derived from eda)|
    
### Metrics 

| Model | Dataset | Accuracy | Precision | Recall |
|:------|:--------|:----------:|:----------:|:----------:|
| BM_malicious | train | 0.47 | 0.47 | 1.00 |
|  | test | 0.57 | 0.57 | 1.00 |
|  |  |  |  |  |
| BM_genuine | train | 0.54 | 0.00 | 0.00 |
|  | test | 0.43 | 0.00 | 0.00 |
|  |  |  |  |  |
| BM_random | train | 0.50 | 0.47 | 0.50 |
|  | test | 0.50 | 0.57 | 0.50 |
|  |  |  |  |  |
| BM_protocol | train | 0.58 | 0.84 | 0.12 |
|  | test | 0.47 | 0.91 | 0.07 |

### Interpretation

- `BM_random`: 
    -   The accuracy is around 50% for both data sets, nicely demonstrating chance level performance.
- `BM_malicious`:
    -   When always predicting class 1, the accuracy is slighly lower than 50% in the train and slighlty higher than 50% in the test data set. This reflects the small class imbalance:
        -   47% of cases are class 1 in train data 
        -   57% of cases are class 1 in test data 
    - Recall is perfect, because no class 1 detection is missed.
    - Conversely, the model is not very precise. Precision reflects the proportion of class 1. 
- `BM_genuine`: 
    - Similar to the previous model, when always predicting class 0, the accuracy is varing between the train and test data depending on the proportion of class 0 occurences reflecting the small class imbalance. 
        - 54% of cases are class 0 in train data
        - 43% of cases are class 0 in train data
    - Pecision and Recall are both 0, because no malicious network traffic case is predicted. 
- `BM_protocol`:
    - This is the frist model that includes a simple heuristic to predict malicious network traffic: predict class 1 when the protocol type is 'icmp'.
        -  EDA results of the training data set showed that 84% of network traffic was malicious when protocol type 'icmp' was used vs. 48% with 'tcp' and 17% with 'udp'. 
    - In the training data set the Accuracy of this model was 58%, which is the highest value compared to all other baseline models. However in the test data set the Accuracy is only 47%.
    - Taking a look at the Precision and Recall metrics gives further insight.
        - The Precision is high in both the train and test data set (84% and 91%) indicating that most of the class 1 predictions were correct.
        -   However, the Recall for training and test data is very low (12% and 7%) indicating that only a small proportion of actual malicious network traffic could be detected. 
    - The EDA also revealed that only a small number of cases 'icmp' is used.
    - This model is still too simple to make accurate predictions.  
    

## 3.  Random Forest Models (RF)

### Metrics

| Model | Dataset | Accuracy | Precision | Recall |
|:------|:--------|:----------:|:----------:|:----------:|
| RF_basic | train | 0.99 | 0.98 | 0.99 |
|  | test | 0.81 | 0.91 | 0.74 |
|  |  |  |  |  |
| RF_best | train | 0.98 | 0.97 | 0.98 |
|  | test | 0.84 | 0.92 | 0.80 |

### Interpretation

- `RF_basic`:
    - The discrepancy in prediction Accuracy between the train and test data set (99% vs 81%) indicates that the basic RF model is overfitting: it performs very well on the training data but fails to generalize effectively to unseen data.
    - This tendency is also true for Precision (98% vs 91%) and Recall (99% vs 74%). 
    - Precision Recall tradeoff:
         -  With a Precision of 91% on test data this model performes already resonably well, if the goal is to be sure that a detection alarm is only raised when the network traffick is truly malicious. 
         - Howerer the Recall is only 74%, indicating that the model is more likely to misse actual malicious network traffic. 
    - Implication
        - In an nIDS it is usually more important to catch as many attacks as possible instead of missing them, therefore a higher Recall would be preferable. 
- `RF_best`:
    - Compared to the basic Random Forest model, this model does perform slightly better: with an overall accuracy of 84% with unseen data. The Precision is similar with 92% and the Recall is better with 80%. The implications are the same.
    
## 3. Model comparison and implications
- With an Accucary of 81% vs 84% in unseen data both RF models can detect malicious network traffic better than the Baseline models (which performed at chance level). Good. 
- However, it can be argued that With a Recall of 74% vs 80% with unseen data the best models still miss too many attacks.
    - Example: From 1000 cases of malicious network traffic the best model would detect 800 cases (True positives = recall x total class 1) and miss the other 200 cases (False negatives = total class 1 - detected)

-  Future Improvements:
    - Hyperparameter tuning and feature enginnering could improve the performance of Random Forest Models
    - Use other models like XGBoost  

