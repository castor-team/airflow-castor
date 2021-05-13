import os
import sys 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from task_creator.task_strategy import TaskStrategy

class TaskCreator:
    def __init__(self, strategy: TaskStrategy) -> None:
        self._strategy = strategy
        
    @property
    def strategy(self) -> TaskStrategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: TaskStrategy) -> None:
        self._strategy = strategy

    def create_task(self, dag):
        task = self._strategy.create_task(dag)
        return task