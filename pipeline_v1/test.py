def step_five(model, X_test, y_test, encoder):
    print('STEP 5')
    import pandas as pd
    from sklearn.tree import DecisionTreeRegressor
    from sklearn.metrics import accuracy_score
    columns_to_encode = ['Pop','sex']
    encoded_data  = encoder.transform(X_test[columns_to_encode])
    encoded_df = pd.DataFrame(encoded_data.toarray(), columns=encoder.get_feature_names_out(columns_to_encode))
    X_test= pd.concat([X_test, encoded_df], axis=1)
    X_test.drop(['Pop','sex'], axis=1,inplace=True)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test,y_pred,normalize=True)
    print(acc)
    return acc