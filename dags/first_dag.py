from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash_operator import BashOperator


with DAG(
    dag_id="primeiro_dag",
    start_date=days_ago(1),
    schedule_interval='@daily'
) as dag:
    
    
    task_1 = EmptyOperator(
        task_id='task_1')
    
    task_2 = EmptyOperator(
        task_id='task_2')
    
    task_3 = EmptyOperator(
        task_id='task_3')
    
    task_4 = BashOperator(
        task_id='cria_pasta',
        bash_command="mkdir -p /Users/mikeiasoliveira/Documents/Projetos/etl-crypto/data/pasta_test") 
    
    task_1 >> [task_2, task_3] 
    task_3 >> task_4