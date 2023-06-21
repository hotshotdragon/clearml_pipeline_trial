from clearml.automation.controller import PipelineController
from clearml import TaskTypes

@PipelineDecorator.component(return_values=['X_train,X_test, y_train, y_test'],
                             cache=True,TaskTypes.data_processing)
from train_test_split import *

@PipelineDecorator.component(return_values=['X_train,encoder'],
                             cache=True,TaskTypes.data_processing)
from preprocessor import *

@PipelineDecorator.component(return_values=['model'],
                             cache=True,TaskTypes.training)
from train import *

@PipelineDecorator.component(return_values=['accuracy'],
                             cache=True,TaskTypes.qc)
from test import *


@PipelineDecorator.pipeline(name='custom_pipeline_test',project='test',version='0.1')
from pipeline import *

if __name__ == '__main__':
    PipelineDecorator.set_default_execution_queue('default')

    executing_pipeline(pickle_url='https://github.com/hotshotdragon/clearml_pipeline_trial/blob/main/data/data.pkl')
    print('Process Completed')