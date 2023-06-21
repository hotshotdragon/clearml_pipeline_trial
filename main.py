from clearml.automation.controller import PipelineController, PipelineDecorator
from clearml import TaskTypes
# from pipeline import *

# @PipelineDecorator.component(return_values=['X_train', 'X_test', 'y_train', 'y_test'],
#                              cache=True, task_type=TaskTypes.data_processing)
def split_data_task(pickle_url):
    from train_test import step_two
    return step_two(pickle_url)

# @PipelineDecorator.component(return_values=['X_train', 'encoder'],
#                              cache=True, task_type=TaskTypes.data_processing)
def preprocess_data_task(X_train, X_test, y_train, y_test):
    from preprocessor import step_three
    return step_three(X_train, X_test, y_train, y_test)

# @PipelineDecorator.component(return_values=['model'],
#                              cache=True, task_type=TaskTypes.training)
def train_model_task(X_train):
    from train import step_four
    return step_four(X_train)

# @PipelineDecorator.component(return_values=['accuracy'],
#                              cache=True, task_type=TaskTypes.qc)
def test_model_task(model,X_test,y_test, encoder):
    from test import step_five
    return step_five(model, X_test,y_test, encoder)

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
        function=split_data_task,
        function_kwargs=dict(pickle_url='${pipeline.url}'),
        function_return=['X_train', 'X_test', 'y_train', 'y_test'],
        cache_executed_step=True,
    )
    pipeline.add_function_step(
        name='step_three',
        function=preprocess_data_task,
        function_kwargs=dict(X_train='${step_two.X_train}',
                             X_test='${step_two.X_test}',
                             y_train='${step_two.y_train}',
                             y_test='${step_two.y_test}'),
        function_return=['X_train','encoder'],
        cache_executed_step=True,
    )
    pipeline.add_function_step(
        name='step_four',
        function=train_model_task,
        function_kwargs=dict(X_train='${step_three.X_train}',
                             y_train='${step_two.y_train}'),
        function_return=['model'],
        cache_executed_step=True,
    )
    pipeline.add_function_step(
        name='step_five',
        function=test_model_task,
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
