def step_three(X_train,y_train):
    print('STEP 3')

    import pandas as pd
    from sklearn.tree import DecisionTreeRegressor

    model = DecisionTreeRegressor(random_state=42)
    model.fit(X_train,y_train)
    return model