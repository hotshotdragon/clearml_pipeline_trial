from clearml import Task
from clearml.automation import PipelineController
# def pre_execute_callback_example(a_pipeline, a_node, current_param_override):
#     # type (PipelineController, PipelineController.Node, dict) -> bool
#     print(
#         "Cloning Task id={} with parameters: {}".format(
#             a_node.base_task_id, current_param_override
#         )
#     )
#     # if we want to skip this node (and subtree of this node) we return False
#     # return True to continue DAG execution
#     return True

# def post_execute_callback_example(a_pipeline, a_node):
#     # type (PipelineController, PipelineController.Node) -> None
#     print("Completed Task id={}".format(a_node.executed))
#     # if we need the actual executed Task: Task.get_task(task_id=a_node.executed)
#     return

pipe = PipelineController(name='PIPE_TEST_1',project='PIPE_TEST_1',version="0.0.1",add_pipeline_tags=False)

pipe.add_parameter("url",
                   "https://github.com/hotshotdragon/clearml_pipeline_trial/blob/main/data/possum.csv?raw=true",
                   "dataset_url"
                   )

pipe.set_default_execution_queue('default')

pipe.add_step(name="stage_data",
    base_task_project="PIPE_TEST_1",
    base_task_name="Pipeline step 1 dataset artifact",
    parameter_override={"General/dataset_url": "${pipeline.url}"})

pipe.add_step(
    name="stage_process",
    parents=["stage_data"],
    base_task_project="PIPE_TEST_1",
    base_task_name="Pipeline step 2 process dataset",
    parameter_override={
        "General/dataset_url": "${stage_data.artifacts.dataset.url}",
        "General/test_size": 0.25,
    }
)

pipe.add_step(
    name="stage_train",
    parents=["stage_process"],
    base_task_project="PIPE_TEST_1",
    base_task_name="Pipeline step 3 process dataset",
    parameter_override={"General/dataset_task_id": "${stage_process.id}"},
    
)


# pipe.start_locally()
pipe.start(queue='default')



