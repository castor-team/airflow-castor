import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))
from task_creator.task_strategy import TaskStrategy
from operator_factory.airflow_operator_factory import AirflowOperatorFactory

class PythonOperatorStrategy(TaskStrategy):

    def __init__(self, task_name, args):
        self.task_name = task_name
        self.args = args

    def create_task(self, dag):
        self.args['python_callable'] = self.get_script_main()
        task = self.get_airflow_operator(dag)
        return task

    def get_script_main(self):
        file = 'py_scripts.' + self.args['python_callable']
        module = __import__(file, fromlist=[None])
        script = getattr(module, 'Script')
        return script.main

    def get_airflow_operator(self, dag):
        task = AirflowOperatorFactory.get_python_operator(
            dag,
            self.task_name,
            self.args
        )
        return task
