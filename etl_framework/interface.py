import sys
import os
import sys
import yaml
import json

# from airflow.models import Variable

dir_absolute_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(dir_absolute_path)
from dag_factory.dag_factory import DAGFactory

# Iterate over /config_files directory
for filename in os.listdir('{}/config_files/'.format(dir_absolute_path)):
    # If the file is a YAML, it tries pass it to the DAG factory
    if filename.endswith(".yaml"):
        with open('{}/config_files/{}'.format(dir_absolute_path, filename)) as file:
            config_file = yaml.safe_load(file)
            
            # DAG attrs
            dag_name = config_file['dag']['name']
            default_args = json.loads(config_file['dag']['default_args'])
            schedule = config_file['dag']['schedule']
            catchup = config_file['dag']['catchup']
            
            # List of tasks to be performed by the DAG
            tasks = config_file['tasks']

            dag = DAGFactory(dag_name, default_args, schedule, catchup)
            globals()[dag_name] = dag.get_airflow_dag(tasks)