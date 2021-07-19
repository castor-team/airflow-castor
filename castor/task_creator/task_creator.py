import os
import sys 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from task_creator.task_strategy import TaskStrategy
from task_creator.strategies.python_operator_strategy import PythonOperatorStrategy
from task_creator.strategies.dummy_operator_strategy import DummyOperatorStrategy
from task_creator.strategies.notebook_operator_strategy import NotebookOperatorStrategy


class TaskCreator:
    def __init__(self, task) -> None:
        self.name = task['name']
        self.args = task['args'] if 'args' in task else None
        self._strategy = task['strategy']

    def create_task(self, dag):
        if self._strategy == 'PythonOperatorStrategy':
            self._strategy = PythonOperatorStrategy(self.name, self.args)
        elif self._strategy == 'DummyOperatorStrategy':
            self._strategy = DummyOperatorStrategy(self.name)
        elif self._strategy == 'NotebookOperatorStrategy':
            self._strategy = NotebookOperatorStrategy(self.name, self.args)
        else:
            msg = "Unknown Castor strategy: {}"
            raise NameError(msg.format(self._strategy))

        task = self._strategy.create_task(dag)
        return task