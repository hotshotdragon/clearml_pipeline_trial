from clearml import Task, StorageManager
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
task = Task.init(project_name="PIPE_TEST", task_name="Pipeline step 2 process dataset")
# task.set_base_docker("clearml_pipeline")

args = {
'dataset_task_id':'',
'dataset_url':'',
'random_state':42,
'test_size':0.2
}

task.connect(args)
task.execute_remotely()

if args['dataset_task_id']:
    dataset_upload_task = Task.get_task(task_id = args['dataset_task_id'])
    print('Input task id={} artifacts {}'.format(args['dataset_task_id'], list(dataset_upload_task.artifacts.keys())))

    data_csv = dataset_upload_task.artifacts['dataset'].get_local_copy()

elif args['dataset_url']:
    data_csv = StorageManager.get_local_copy(remote_url=args['dataset_url'])

else:
    raise ValueError("Missing Data Link")

df = pd.read_csv(data_csv)
print(df.head())
df.replace('NA',np.nan,inplace=True)
df.dropna(inplace=True)
print(df.shape)

y = df['age']
print("y shape",y.shape)
X = df[(c for c in df.columns if c != 'age')]
print("X shape",X.shape)

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=args['test_size'], random_state=args['random_state'])
print(X_train.shape, y_train.shape, X_test.shape, y_test.shape)

columns_to_encode = ['Pop','sex']
encoder = OneHotEncoder()
X_train_encoded = pd.DataFrame(encoder.fit_transform(X_train[columns_to_encode]).toarray())
X_train = pd.concat([X_train.reset_index(drop=True),X_train_encoded],axis=1)
X_train.drop(columns_to_encode,axis=1,inplace=True)
X_train.columns = X_train.columns.astype(str)

# upload processed data
print('Uploading process dataset')
task.upload_artifact('OneHotEncoder',encoder)
task.upload_artifact('X_train', X_train)
task.upload_artifact('X_test', X_test)
task.upload_artifact('y_train', y_train)
task.upload_artifact('y_test', y_test)

print('Notice, artifacts are uploaded in the background')
print('Done')