def step_three(X_train):
    print('STEP 3')    
    import pandas as pd
    from sklearn.preprocessing import OneHotEncoder

    columns_to_encode = ['Pop','sex']
    encoder = OneHotEncoder()
    encoded_data  = encoder.fit_transform(X_train[columns_to_encode])
    encoded_df = pd.DataFrame(encoded_data.toarray(), columns=encoder.get_feature_names_out(columns_to_encode))
    X_train= pd.concat([X_train, encoded_df], axis=1)
    X_train.drop(['Pop','sex'], axis=1,inplace=True)
    
    return X_train, encoder