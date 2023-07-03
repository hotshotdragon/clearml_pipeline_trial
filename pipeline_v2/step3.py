import joblib
import numpy as np
from sklearn.tree import DecisionTreeRegressor
import pandas as pd
from clearml import Task

task = Task.init(project_name="PIPE_TEST_1",task_name="Pipeline step 3 process dataset")
# task.set_base_docker("clearml_pipeline")
args = {
    'dataset_task_id':'e3a5da49cfd349d6b0685ae0eeff67da'
 }

task.connect(args)
task.execute_remotely(queue_name='default')

print("RETREIVING DATASET")

dataset_task = Task.get_task(task_id = args['dataset_task_id'])
X_train = dataset_task.artifacts['X_train'].get()
print(X_train)
X_test = dataset_task.artifacts['X_test'].get()
print(X_test)
y_train = dataset_task.artifacts['y_train'].get()
print(y_train)
y_test = dataset_task.artifacts['y_test'].get()
print(y_test)
print('Dataset loaded')
encoder = dataset_task.artifacts['OneHotEncoder'].get()


model = DecisionTreeRegressor()
model.fit(X_train,y_train)
joblib.dump(model,'model.pkl',compress=True)
task.upload_artifact('model',model)
loaded_model = joblib.load('model.pkl')

columns_to_encode = ['Pop','sex']
X_test_encoded = pd.DataFrame(encoder.transform(X_test[columns_to_encode]).toarray())
X_test = pd.concat([X_test.reset_index(drop=True),X_test_encoded],axis=1)
X_test.drop(columns_to_encode,axis=1,inplace=True)
X_test.columns = X_test.columns.astype(str)

result = loaded_model.score(X_test,y_test)
print(result)
print('Done')