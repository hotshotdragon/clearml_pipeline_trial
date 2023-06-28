from clearml.automation.controller import PipelineController

def step_two(pickle_data_url:str, test_size = 0.2, random_state = 42):
    print('STEP 2')
    import sklearn
    import numpy as np
    from sklearn.model_selection import train_test_split
    import pandas as pd
    import pickle as pkl
    # from clearml import StorageManager


    # local_data_pkl = StorageManager.get_local_copy(remote_url=pickle_data_url)
    # with open(local_data_pkl, 'rb') as f:
    #     try:
    #         df = pkl.load(f)
    #     except pkl.UnpicklingError as e:
    df = pd.read_csv(pickle_data_url)
    print(df.shape)
    df.replace('NA',np.nan,inplace=True)
    df.dropna(inplace=True)
    print(df.shape)

    y = df['age']
    print("y shape",y.shape)
    X = df[(c for c in df.columns if c != 'age')]
    print("X shape",X.shape)

    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=test_size,random_state=random_state)
    print(X_train.shape, y_train.shape, X_test.shape, y_test.shape)
    return X_train, X_test, y_train, y_test

def step_three(X_train):
    print('STEP 3')    
    import pandas as pd
    from sklearn.preprocessing import OneHotEncoder

    columns_to_encode = ['Pop','sex']
    encoder = OneHotEncoder()
    X_train_encoded = pd.DataFrame(encoder.fit_transform(X_train[columns_to_encode]).toarray())
    X_train = pd.concat([X_train.reset_index(drop=True),X_train_encoded],axis=1)
    X_train.drop(columns_to_encode,axis=1,inplace=True)
    X_train.columns = X_train.columns.astype(str)
    print("ENCODER X_TRAIN",X_train.shape)
    return X_train, encoder


def step_four(X_train,y_train):
    print('STEP 4')

    import pandas as pd
    from sklearn.tree import DecisionTreeRegressor
    print(X_train.shape)
    print(y_train.shape)

    model = DecisionTreeRegressor()
    model.fit(X_train,y_train)
    return model


def step_five(model, X_test, y_test, encoder):
    print('STEP 5')
    import pandas as pd
    from sklearn.tree import DecisionTreeRegressor
    from sklearn.metrics import accuracy_score
    columns_to_encode = ['Pop','sex']
    X_test_encoded = pd.DataFrame(encoder.transform(X_test[columns_to_encode]).toarray())
    X_test = pd.concat([X_test.reset_index(drop=True),X_test_encoded],axis=1)
    X_test.drop(columns_to_encode,axis=1,inplace=True)
    X_test.columns = X_test.columns.astype(str)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test,y_pred,normalize=True)
    print(acc)
    return acc

if __name__ == '__main__':
    # PipelineDecorator.set_default_execution_queue('default')
    
    pipeline = PipelineController(project='ClearML_Pipeline_Function_Test', 
                                  name='test_3', 
                                  version='0.1',
                                  docker='clearmlpipeline')
    pipeline.set_default_execution_queue('default')
    pipeline.add_parameter(
        name='url',
        description='url to pickle file',
        default='https://github.com/hotshotdragon/clearml_pipeline_trial/blob/main/data/possum.csv?raw=true'
    )

    pipeline.add_function_step(
        name='step_two',
        function=step_two,
        function_kwargs=dict(pickle_data_url='${pipeline.url}'),
        function_return=['X_train', 'X_test', 'y_train', 'y_test'],
        cache_executed_step=True,
    )
    pipeline.add_function_step(
        name='step_three',
        function=step_three,
        function_kwargs=dict(X_train='${step_two.X_train}'),
        function_return=['X_train','encoder'],
        cache_executed_step=True,
    )
    pipeline.add_function_step(
        name='step_four',
        function=step_four,
        function_kwargs=dict(X_train='${step_three.X_train}',
                             y_train='${step_two.y_train}'),
        function_return=['model'],
        cache_executed_step=True,
    )
    pipeline.add_function_step(
        name='step_five',
        function=step_five,
        function_kwargs=dict(model='${step_four.model}',
                             X_test='${step_two.X_test}',
                             y_test='${step_two.y_test}',
                             encoder='${step_three.encoder}'),
        function_return=['accuracy'],
        cache_executed_step=True,
    )
    # Set custom Docker image as the base image
    # pipeline.set_base_docker(
    #     image='my_custom_image'
    # )
    
    
    pipeline.start(queue='default')
    # pipeline.start_locally(run_pipeline_steps_locally=True)
    
    print('Process Completed')
