from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
import pendulum
from os.path import join
import pandas as pd
from airflow.macros import ds_add
import ssl


with DAG(
    dag_id='dados_climaticos',
    start_date=pendulum.datetime(2023, 2, 11, tz='UTC'),
    schedule_interval='0 0 * * 1' # Executar toda segunda feita
    # cron expression:
    # (   0   ) (  0  ) (   *   ) ( * ) (      1      )
    # (minutos) (horas) (dia_mes) (mes) (dia_da_semana)
) as dag:
    
    # Criar_pasta: Cria uma pasta com a data da semana que o DAG foi executado.
    taks_1 = BashOperator(
        task_id = 'criar_pasta',
        bash_command='mkdir -p "/Users/mikeiasoliveira/Documents/Projetos/etl-crypto/data/semana={{data_interval_end.strftime("%Y-%m-%d")}}"'
    )
    
    def extrai_dados(data_interval_end):
        
        ssl._create_default_https_context = ssl._create_unverified_context
        city = 'Boston'
        key = 'GRRE2CPXXTR3X8M8DQW99XYKM'

        URL = join('https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/',
                    f'{city}/{data_interval_end}/{ds_add(data_interval_end, 7)}?unitGroup=metric&include=days&key={key}&contentType=csv')

        data = pd.read_csv(URL)

        file_path = f'/Users/mikeiasoliveira/Documents/Projetos/etl-crypto/data/semana={data_interval_end}/'
        

        data.to_csv(file_path + 'raw_data.csv')
        data[['datetime', 'tempmin', 'temp', 'tempmax']].to_csv(file_path + 'temp_raw.csv')
        data[['datetime', 'description', 'icon']].to_csv(file_path + 'cond_raw.csv')

    
    task_2 = PythonOperator(
        task_id = 'extrai_dados',
        python_callable = extrai_dados,
        op_kwargs = {'data_interval_end': '{{data_interval_end.strftime("%Y-%m-%d")}}'}
    )
    
    taks_1 >> task_2
    
    