import os
import yaml
import sys

from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.databricks.operators.databricks import DatabricksSubmitRunOperator

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

    @staticmethod
    def get_databricks_operator(dag, task_id, args):
        notebook_task_params = AirflowOperatorFactory._get_databricks_job_params(args)
        conn_id = args['databricks_conn_id'] if "databricks_conn_id" in args else 'databricks_default'

        return DatabricksSubmitRunOperator(
            task_id=task_id,
            databricks_conn_id=conn_id,
            dag=dag,
            json=notebook_task_params)

    @staticmethod
    def _get_databricks_job_params(args):
        notebook_task_params: dict = dict()
        if 'cluster_id' in args:
            notebook_task_params.update({'existing_cluster_id': args['cluster_id']})
        elif 'new_cluster' in args:
            notebook_task_params.update({'new_cluster': args['new_cluster']})
        else:
            new_cluster = {
                'spark_version': os.getenv('DATABRICKS_SPARK_VERSION', '2.1.0-db3-scala2.11'),
                'node_type_id': os.getenv('DATABRICKS_NODE_TYPE_ID', 'r3.xlarge'),
                'aws_attributes': {
                    'availability': os.getenv('DATABRICKS_AWS_ATTRIBUTES_AVAILABILITY', 'ON_DEMAND'),
                },
                'num_workers': os.getenv('DATABRICKS_NUM_WORKERS', 8),
            }
            notebook_task_params.update({'new_cluster': new_cluster})

        if 'notebook_path' in args:
            notebook_task_params.update({
                'notebook_task': {
                    'notebook_path': args['notebook_path'],
                },
            })
        return notebook_task_params
