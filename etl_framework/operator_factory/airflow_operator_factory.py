import os
import yaml
import sys

from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

class AirflowOperatorFactory():
    
    @staticmethod
    def get_dummy_operator(dag, task_id):
        task = DummyOperator(
            dag = dag,
            task_id = task_id
        )
        return task

    @staticmethod
    def get_python_operator(dag, task_id, args):
        task = PythonOperator(
            dag = dag,
            task_id = task_id,
            **args
        )
        return task
