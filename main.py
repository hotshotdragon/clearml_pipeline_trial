from clearml.automation.controller import PipelineController

def step_two(pickle_data_url:str, test_size = 0.2, random_state = 42):
    print('STEP 2')
    import sklearn
    from sklearn.model_selection import train_test_split
    import pandas as pd
    import pickle as pkl
    from clearml import StorageManager


    local_data_pkl = StorageManager.get_local_copy(remote_url=pickle_data_url)
    with open(local_data_pkl, 'rb') as f:
        try:
            df = pkl.load(f)
        except pkl.UnpicklingError as e:
            df = pd.read_pickle(f)

    y = df['age']
    X = df[(c for c in df.columns if c != 'age')]

    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=test_size,random_state=random_state)
    return X_train, X_test, y_train, y_test

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


def step_four(X_train,y_train):
    print('STEP 4')

    import pandas as pd
    from sklearn.tree import DecisionTreeRegressor

    model = DecisionTreeRegressor(random_state=42)
    model.fit(X_train,y_train)
    return model


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

if __name__ == '__main__':
    # PipelineDecorator.set_default_execution_queue('default')
    
    pipeline = PipelineController(project='ClearML_Pipeline_Function_Test', 
                                  name='test_1', 
                                  version='0.1',
                                  docker='clearmlpipeline')
    pipeline.set_default_execution_queue('default')
    pipeline.add_parameter(
        name='url',
        description='url to pickle file',
        default='https://github.com/hotshotdragon/clearml_pipeline_trial/blob/main/data/data.pkl'
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
        function_kwargs=dict(X_train='${step_two.X_train}',
                             X_test='${step_two.X_test}',
                             y_train='${step_two.y_train}',
                             y_test='${step_two.y_test}'),
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
    
    
    # pipeline.start(queue='default')
    pipeline.start_locally(run_pipeline_steps_locally=True)
    
    print('Process Completed')
