from clearml.automation.controller import PipelineController, PipelineDecorator
from clearml import TaskTypes
from train_test_split import *
from preprocessor import *
from train import *
from test import *
from pipeline import *

@PipelineDecorator.component(return_values=['X_train', 'X_test', 'y_train', 'y_test'],
                             cache=True, task_type=TaskTypes.data_processing)
def split_data_task(pickle_url):
    return step_two(pickle_url)

@PipelineDecorator.component(return_values=['X_train', 'encoder'],
                             cache=True, task_type=TaskTypes.data_processing)
def preprocess_data_task(X_train, X_test, y_train, y_test):
    return step_three(X_train, X_test, y_train, y_test)

@PipelineDecorator.component(return_values=['model'],
                             cache=True, task_type=TaskTypes.training)
def train_model_task(X_train, encoder):
    return step_four(X_train, encoder)

@PipelineDecorator.component(return_values=['accuracy'],
                             cache=True, task_type=TaskTypes.qc)
def test_model_task(X_test, model):
    return step_five(X_test, model)

@PipelineDecorator.pipeline(name='custom_pipeline_test',project='test',version='0.1')
def pipeline_execute(pickle_url):
    return executing_pipeline(pickle_url)

if __name__ == '__main__':
    PipelineDecorator.set_default_execution_queue('default')
    executing_pipeline(
        pickle_url='https://github.com/hotshotdragon/clearml_pipeline_trial/blob/main/data/data.pkl')
    # Set input arguments for the first step   
    print('Process Completed')
