from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.utils.task_group import TaskGroup
from airflow.operators.dummy_operator import DummyOperator

dag = DAG('test_task_groups', start_date=days_ago(2))
t0 = DummyOperator(task_id='start', dag = dag)

# Start Task Group definition
with TaskGroup(group_id='group1', dag = dag) as tg1:
    t1 = DummyOperator(task_id='task1', dag = dag)
    t2 = DummyOperator(task_id='task2', dag = dag)

    t1 >> t2
# End Task Group definition
    
t3 = DummyOperator(task_id='end', dag = dag)

# Set Task Group's (tg1) dependencies
t0 >> tg1 >> t3