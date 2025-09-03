import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# read churn data from csv file
df_churn = pd.read_csv('data/telco_churn.csv')
df_churn = df_churn[['gender', 'PaymentMethod', 'MonthlyCharges', 'tenure', 'Churn']].copy()
df = df_churn.copy()
df.fillna(0, inplace=True)

# create machine-readable dummy variables for categorical columns
encode = ['gender', 'PaymentMethod']
for col in encode:
    dummy = pd.get_dummies(df[col], prefix=col)
    df = pd.concat([df, dummy], axis=1)
    del df[col]
    
# map the churn column values to binary values
df['Churn'] = np.where(df['Churn']=='Yes', 1, 0)

# define our input and output
X = df.drop('Churn', axis=1)
Y = df['Churn']

# define instance of RandomForestClassifier and fit our model to data
clf = RandomForestClassifier()
clf.fit(X, Y)

# save our model to a pickle file
pickle.dump(clf, open('churn_clf.pkl', 'wb'))
