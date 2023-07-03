from clearml import Task, StorageManager

# create an dataset experiment
task = Task.init(project_name="PIPE_TEST_1", task_name="Pipeline step 1 dataset artifact")
# task.set_base_docker("clearml_pipeline")
# only create the task, we will actually execute it later
task.execute_remotely(queue_name='default')

# simulate local dataset, download one, so we have something local
local_data = StorageManager.get_local_copy(
    remote_url='https://github.com/hotshotdragon/clearml_pipeline_trial/blob/main/data/possum.csv?raw=true')

# add and upload local file containing our toy dataset
task.upload_artifact('dataset', artifact_object=local_data)

print('uploading artifacts in the background')

# we are done
print('Done')