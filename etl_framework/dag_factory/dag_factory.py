from datetime import timedelta
import json
import os
import sys

from airflow import DAG

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from task_creator.task_creator import TaskCreator
from operator_factory.airflow_operator_factory import AirflowOperatorFactory


class DAGFactory:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.type_casting()
        self.dag = DAG(**kwargs)

    def type_casting(self) -> None:
        if 'user_defined_macros' in self.kwargs:
            self.kwargs.update(default_args = json.loads(self.kwargs['user_defined_macros']))
        if 'user_defined_filters' in self.kwargs:
            self.kwargs.update(default_args = json.loads(self.kwargs['user_defined_filters']))
        if 'default_args' in self.kwargs:
            self.kwargs.update(default_args = json.loads(self.kwargs['default_args']))
        if 'params' in self.kwargs:
            self.kwargs.update(default_args = json.loads(self.kwargs['params']))
        if 'access_control' in self.kwargs:
            self.kwargs.update(default_args = json.loads(self.kwargs['access_control']))
        if 'jinja_environment_kwargs' in self.kwargs:
            self.kwargs.update(default_args = json.loads(self.kwargs['jinja_environment_kwargs']))

    def get_airflow_dag(self, tasks):
        '''
        - tasks_dict: Dictionary where the key is the task name and value is the task object returned by the task creator
            {'start': start_obj, 't1': t1, ... , 'tn': tn, 'end': end}
        - task_dependencies: dictionary where the key is the task name and the value is an array of strings with the dependencies of the task
            {'t1': ['start'], 't2' : ['t1'], 't3': ['t1', 't2'], 'end' : ['t3']}
        '''
        tasks_dict = {}
        task_dependencies = {}

        for task in tasks:
            task_creator = TaskCreator(task)
            tasks_dict[task['name']] = task_creator.create_task(self.dag)
            
            if 'depends_on' in task:
                task_dependencies[task['name']] = task['depends_on'] 

        for task, dependencies in task_dependencies.items():
            task_obj = [tasks_dict[dependency] for dependency in dependencies]
            task_obj >> tasks_dict[task] 
        return self.dag