def step_one(pickle_data_url:str, test_size = 0.2, random_state = 42):
    print('STEP 1')
    import sklearn
    from sklearn.model_selection import train_test_split
    import pandas as pd
    import pickle as pkl
    from clearml import StorageManager


    local_data_pkl = StorageManager.get_local_copy(remote_url=pickle_data_url)
    with open(local_data_pkl,'rb') as f:
        df = pkl.load(f)

    y = df['age']
    X = df[(c for c in df.columns if c != 'age')]

    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=test_size,random_state=random_state)
    return X_train, X_test, y_train, y_test