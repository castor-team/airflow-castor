import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))
from task_creator.task_strategy import TaskStrategy
from operator_factory.airflow_operator_factory import AirflowOperatorFactory


class NotebookOperatorStrategy(TaskStrategy):

    def __init__(self, task_name, args):
        self.task_name = task_name
        self.args = args

    def create_task(self, dag):
        if self.args['runner'] and self.args['runner'] == "DATABRICKS":
            return AirflowOperatorFactory.get_databricks_operator(dag, self.task_name, self.args)
        else:
            msg = "Unknown Notebook strategy runner: {}, Supported runner `DATABRICKS`"
            raise NameError(msg.format(self.args['runner']))