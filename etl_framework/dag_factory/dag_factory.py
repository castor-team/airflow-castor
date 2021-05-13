import os
import sys

from airflow import DAG

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from task_creator.task_creator import TaskCreator
from task_creator.strategies.python_operator_strategy import PythonOperatorStrategy
from operator_factory.airflow_operator_factory import AirflowOperatorFactory

class DAGFactory:

    def __init__(self, dag_name, default_args, schedule, catchup):
        self.dag_name = dag_name
        self.default_args = default_args
        self.schedule = schedule
        self.catchup = catchup

    def create_dag(self, dag_name, default_args, schedule, catchup):
        dag = DAG(
            dag_name, 
            default_args = default_args,
            schedule_interval = schedule,
            catchup = catchup)
        return dag

    def get_airflow_dag(self, tasks):
        dag = self.create_dag(self.dag_name, self.default_args, self.schedule, self.catchup)

        start = AirflowOperatorFactory.get_dummy_operator(dag, 'start')
        end = AirflowOperatorFactory.get_dummy_operator(dag, 'end')

        tasks_dict = {}
        tasks_dict['start'] = start
        tasks_dict['end'] = end

        for task in tasks:
            if task['strategy'] == 'PythonOperatorStrategy':
                strategy = PythonOperatorStrategy(
                    task['name'],
                    task['args'])
                task_creator = TaskCreator(strategy)
                tasks_dict[task['name']] = task_creator.create_task(dag)
            else:
                msg = "Estrategia desconocida: {}"
                raise NameError(msg.format(task['strategy']))

        all_depends_on = []
        for task in tasks:
            task_depends_on = 'start' if task['depends_on'] is None else task['depends_on'] # !
            depends_on_list = task_depends_on.split(',') # !
            all_depends_on.extend(depends_on_list)
            for depends_on in depends_on_list:
                tasks_dict[depends_on] >> tasks_dict[task['name']]

        name_list = [task['name'] for task in tasks]
        # no_blocking_tasks = list(set(name_list) - set(all_depends_on))
        no_blocking_tasks = list(filter(lambda task: task not in all_depends_on, name_list))

        for task_name in no_blocking_tasks:
            tasks_dict[task_name] >> end

        return dag