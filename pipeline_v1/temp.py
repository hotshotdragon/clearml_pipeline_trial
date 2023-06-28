import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

df = pd.read_csv('https://github.com/hotshotdragon/clearml_pipeline_trial/blob/main/data/possum.csv?raw=true',on_bad_lines='skip')
y = df['age']
print("y shape",y.shape)
X = df[(c for c in df.columns if c != 'age')]
print("X shape",X.shape)
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)
print(X_train.shape, y_train.shape, X_test.shape, y_test.shape)
columns_to_encode = ['Pop','sex']
encoder = OneHotEncoder()
X_train_encoded = pd.DataFrame(encoder.fit_transform(X_train[columns_to_encode]).toarray())
X_train = pd.concat([X_train.reset_index(drop=True),X_train_encoded],axis=1)
X_train.drop(columns_to_encode,axis=1,inplace=True)

X_test_encoded = pd.DataFrame(encoder.transform(X_test[columns_to_encode]).toarray())
X_test = pd.concat([X_test.reset_index(drop=True),X_test_encoded],axis=1)
X_test.drop(columns_to_encode,axis=1,inplace=True)
X_train.columns = X_train.columns.astype(str)
X_test.columns = X_test.columns.astype(str)

print(X_train.columns)
print(X_test.columns)

print(X_train.shape)
print(X_test.shape)

