from clearml.automation.controller import PipelineDecorator
from clearml import TaskTypes

@PipelineDecorator.component(
    return_values=['X_train', 'X_test', 'y_train', 'y_test'], 
    cache=True, task_type=TaskTypes.data_processing
)
def one(url):
    from step1 import step_one
    print("One Imported")
    return step_one(url)
############################################################################
@PipelineDecorator.component(
        return_values=['X_train','encoder'],
        cache=True, task_type=TaskTypes.data_processing
        )
def two(X_train):
    from step2 import step_two
    print("Two Imported")
    return step_two(X_train)
############################################################################
@PipelineDecorator.component(
        return_values=['model'],
        cache=True, task_type=TaskTypes.training
        )
def three(X_train,y_train):
    from step3 import step_three
    print("Three Imported")
    return step_three(X_train,y_train)
############################################################################
@PipelineDecorator.component(
        return_values=['accuracy'],
        cache=True, task_type=TaskTypes.qc
        )
def four(model,X_test,y_test, encoder):
    from step4 import step_four
    print("Four Imported")
    return step_four(model, X_test,y_test, encoder)
############################################################################
@PipelineDecorator.pipeline(
    name='pipeline_test_decorator', project='decorator_check',version='0.0.1'
    )

def executing_pipeline(url):
    print("Data URL",url)

    print("LAUNCH 1")
    X_train, X_test, y_train, y_test = one(url)

    print("LAUNCH 2")
    X_train,encoder = two(X_train)

    print("LAUNCH 3")
    model = three(X_train,y_train)

    print("LAUNCH 4")
    accuracy = four(model,X_test,y_test,encoder)
    print(f"Accuracy={accuracy}%")

############################################################################
if __name__ == "__main__":
    PipelineDecorator.set_default_execution_queue('services')
    executing_pipeline(url='https://github.com/hotshotdragon/clearml_pipeline_trial/blob/main/data/possum.csv?raw=true')

    print("process completed")
