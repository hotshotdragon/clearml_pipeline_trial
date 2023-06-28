import joblib
import matplotlib.pyplot as plt
import numpy as np
from sklearn.tree import DecisionTreeRegressor

from clearml import Task

task = Task.init(project_name="PIPE_TEST",task_name="Pipeline step 3 process dataset")
# task.set_base_docker("clearml_pipeline")
args = {
    'dataset_task_id':'REPLACE_WITH'
 }

task.connect(args)
task.execute_remotely()

print("RETREIVING DATASET")

dataset_task = Task.get_task(task_id = args['dataset_task_id'])
X_train = dataset_task.artifacts['X_train'].get()
X_test = dataset_task.artifacts['X_test'].get()

y_train = dataset_task.artifacts['y_train'].get()

y_test = dataset_task.artifacts['y_test'].get()

print('Dataset loaded')

model = DecisionTreeRegressor()
model.fit(X_train,X_test)
joblib.dump(model,'model.pkl',compress=True)

loaded_model = joblib.load('model.pkl')

result = loaded_model.score(X_test,y_test)

print('Done')