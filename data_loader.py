def step_one(data):
    print('STEP 1')
    import pandas as pd
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    import pickle as pkl


    df = pd.read_csv(data)
    df.dropna(axis=0,inplace=True)
    df.drop(['case'], axis=1,inplace=True)
    pd.to_pickle(df,"data\data.pkl")

step_one(r"data\possum.csv")