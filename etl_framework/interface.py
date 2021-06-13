import sys
import os
import sys
import yaml
import json

dir_absolute_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(dir_absolute_path)
from dag_factory.dag_factory import DAGFactory

# Iterate over /config_files directory
for filename in os.listdir('{}/config_files/'.format(dir_absolute_path)):
    # If the file is a YAML, it tries pass it to the DAG factory
    if filename.endswith(".yaml"):
        with open('{}/config_files/{}'.format(dir_absolute_path, filename)) as file:
            config_file = yaml.safe_load(file)
            print(config_file)
            
            # # DAG attrs
            # dag_id = config_file['dag']['name']
            # default_args = json.loads(config_file['dag']['default_args'])
            # schedule = config_file['dag']['schedule']
            # catchup = config_file['dag']['catchup']
            
            # List of tasks to be performed by the DAG
            tasks = config_file['tasks']
            print(tasks)

            dag = DAGFactory(**config_file['dag'])
            globals()[config_file['dag']['dag_id']] = dag.get_airflow_dag(tasks)