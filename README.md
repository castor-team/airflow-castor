# Castor - An orchestration framework for Apache Airflow

A framework for building Airflow DAGs via YAML files. Castor comprises four modules:
- Config files 
- DAG factory 
- Task creator
- Task strategies 
- Operator Factory

# Config Files
A set of YAMLs files defined by the user. Each DAG represents an Airflow DAG.

# DAG Factory
The DAG Factory is responsible for creating the DAGs based on the configuration defined in the YAML file.

# Task Creator
The Task Creator is responsible for creating DAG tasks based on task strategies. 

# Task Strategies
A task strategy represents a strategy in which a task can be executed. A strategy can be based on an Airflow operator (*e.g.,* PythonOperatorStrategy).

The strategies supported by Castor at this moment in time are:
- [DummyOperatorStrategy](castor/task_creator/strategies/python_operator_strategy.py)
- [PythonOperatorStrategy](castor/task_creator/strategies/dummy_operator_strategy.py)


# Operator factory
It is responsible for creating Airflow Operators based on a set of parameters supplied by the DAG Factory.

The operators supported by Castor at this moment in time are:
- [DummyOperator](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/operators/dummy/index.html)
- [PythonOperator](https://airflow.apache.org/docs/apache-airflow/stable/_modules/airflow/operators/python.html#PythonOperator)