# Castor - An orchestration framework for Apache Airflow

A framework for building Airflow DAGs via YAML files. Castor comprises four modules:
- Config files 
- DAG factory 
- Task creator
- Task strategies 
- Operator Factory

# Config Files
A set of YAMLs files defined by the user. Each YAML file represents an Airflow DAG.

## Syntax
The YAML comprises two sections: `dag` and `tasks`.

### DAG section

The `dag` section contains all oficial parameters supported by an Airflow DAG. Check [this](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/models/dag/index.html) for more information.

This is an example of a DAG section in a YAML file:
```
dag:
  dag_id: 'init_castor_dag'
  default_args: '{"owner": "castor", "start_date": "2021-06-13"}'
  schedule_interval: '@once'
  catchup: False
  tags:
    - example
```

### Task section
The parameters a task should include are:
* [Mandatory] **task_name**: Name for the task
* [Mandatory] **strategy**: The strategy that should be used by the Task Creator to create the task (*e.g.,* PythonOperatorStrategy)
* [Optional] **depends_on**: list of dependencies of the task. This are name of other tasks previously defined
* [Optional] **args**: Arguments supported by the Airflow operator associated to the Task Strategy

This is an example of a `task` section in a YAML file:

```
- name: 'task_name'
    strategy: 'strategy_name'
    depends_on: 
    - 'AnotherTask'
    - 'AnotherTask'
    - ...
    args:
        retries: 2
        trigger_rule: 'all_success'
        provide_context: True
        python_callable: 'print_params'
        op_kwargs:
            param1: 'value1' 
```

### Example
This is a YAML file containing a simple Airflow DAG for showing Castor capabilities.
```
dag:
  dag_id: 'init_castor_dag'
  default_args: '{"owner": "castor", "start_date": "2021-06-13"}'
  schedule_interval: '@once'
  catchup: False
  tags:
    - example
tasks:
    - name: 'start'
      strategy: 'DummyOperatorStrategy'
    - name: 't1'
      strategy: 'PythonOperatorStrategy'
      depends_on: 
        - 'start'
      args:
        retries: 2
        trigger_rule: 'all_success'
        provide_context: True
        python_callable: 'print_params'
        op_kwargs:
          param1: 'value1' 
    - name: 't2'
      strategy: 'PythonOperatorStrategy'
      depends_on: 
        - 'start'
      args:
        retries: 2
        trigger_rule: 'all_success'
        provide_context: True
        python_callable: 'print_params'
        op_kwargs:
          param1: 'value1'
    - name: 't3'
      strategy: 'PythonOperatorStrategy'
      depends_on: 
        - 't1'
        - 't2'
      args:
        retries: 2
        trigger_rule: 'all_success'
        provide_context: True
        python_callable: 'print_params'
        op_kwargs:
          param1: 'value1' 
    - name: 't4'
      strategy: 'NotebookOperatorStrategy'
      depends_on:
        - 't3'
      args:
        retries: 2
        trigger_rule: 'all_success'
        provide_context: True
        runner: 'DATABRICKS'
        databricks_conn_id: '<CONNECTION_ID (Optional)>'
        notebook_path: '<NOTEBOOK_PATH_IN_DATABRICKS_WORKSPACE>'
        cluster_id: '<CLUSTER_ID (provide cluster_id or `new_cluster` definition)>'
        new_cluster:
          spark_version: '2.1.0-db3-scala2.11'
          node_type_id: 'r3.xlarge'
          aws_attributes:
            availability: 'ON_DEMAND'
          num_workers: 8
    - name: 'end'
      strategy: 'DummyOperatorStrategy'
      depends_on:
        - 't4'
```

# DAG Factory
The DAG Factory is responsible for creating the DAGs based on the configuration defined in the YAML file.

# Task Creator
The Task Creator is responsible for creating DAG tasks based on task strategies. 

# Task Strategies
A task strategy represents a strategy in which a task can be executed. A strategy can be based on an Airflow operator (*e.g.,* PythonOperatorStrategy).

The strategies supported by Castor at this moment in time are:
- [DummyOperatorStrategy](castor/task_creator/strategies/python_operator_strategy.py)
- [PythonOperatorStrategy](castor/task_creator/strategies/dummy_operator_strategy.py)
- [NotebookOperatorStrategy](castor/task_creator/strategies/notebook_operator_strategy.py)


# Operator factory
It is responsible for creating Airflow Operators based on a set of parameters supplied by the DAG Factory.

The operators supported by Castor at this moment in time are:
- [DummyOperator](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/operators/dummy/index.html)
- [PythonOperator](https://airflow.apache.org/docs/apache-airflow/stable/_modules/airflow/operators/python.html#PythonOperator)
- [DatabricksOperator](https://airflow.apache.org/docs/apache-airflow-providers-databricks/stable/operators.html#databrickssubmitrunoperator)