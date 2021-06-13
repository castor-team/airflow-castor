import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))
from task_creator.task_strategy import TaskStrategy
from operator_factory.airflow_operator_factory import AirflowOperatorFactory

class DummyOperatorStrategy(TaskStrategy):

    def __init__(self, task_name):
        self.task_name = task_name

    def create_task(self, dag):
        task = self.get_airflow_operator(dag)
        return task

    def get_airflow_operator(self, dag):
        task = AirflowOperatorFactory.get_dummy_operator(
            dag,
            self.task_name
        )
        return task
