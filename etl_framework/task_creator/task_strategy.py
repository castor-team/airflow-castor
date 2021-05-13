import os
import sys 

from abc import ABCMeta, abstractmethod

class TaskStrategy:

    @abstractmethod
    def create_task(self, dag):
        pass