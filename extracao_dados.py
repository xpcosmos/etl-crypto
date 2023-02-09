import os 
from os.path import join
import pandas as pd
from datetime import datetime, timedelta
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

start_date = datetime.today()
end_date = start_date + timedelta(days=7)

start_date = start_date.strftime(r'%Y-%m-%d')
end_date = end_date.strftime(r'%Y-%m-%d')

city = 'Boston'
key = 'GRRE2CPXXTR3X8M8DQW99XYKM'

URL = join('https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/',
            f'{city}/{start_date}/{end_date}?unitGroup=metric&include=days&key={key}&contentType=csv')

data = pd.read_csv(URL)
file = pd.read_csv(URL)

file_path = f'data/semana={start_date}/'
os.mkdir(file_path)

data.to_csv(file_path + 'raw_data.csv')
data[['datetime', 'tempmin', 'temp', 'tempmax']].to_csv(file_path + 'temp_raw.csv')
data[['datetime', 'description', 'icon']].to_csv(file_path + 'cond_raw.csv')


# ======================================= Introdução =============================================

# ----------------------------------
# ----------------------------  DAG:
# ----------------------------------
#   Fluxo de dados definido em Python: Um conjunto de 
#   instruções que precisam ser excutadas
#   em uma determinada ordem. 

# ----------------------------------
# ---------------------------  Task:
# ---------------------------------
#   Unidade mais básica do DAG que constroem um DAG. 
#   Utilizada para implementar lógica no fluxo.
#   É correto afimar que uma Task é um conjunto de DAGs

# ----------------------------------
# ------------------------  DAG Run:
# ----------------------------------
#   A execução do DAG no tempo. Contém metadados sobre o DAG 
#   propriamente dito.


# ----------------------------------
# ------------------  Task Instance:
# ----------------------------------
#   A execução de uma tarefa em um ponto específico no tempo

# ----------------------------------
# -----------------------  Operators
# ----------------------------------
#   Blocos de construção do DAGs. Contém a lógica de processamento dos 
#   dados, em que cada tarefa é definida pela instância de um operador.

# ======================================= Arquitetura =============================================

#   O usuário pode acessar uma pasta com os DAGs que contém os Data 
#   Pipelines. O banco de dados armazena todos os meta dados dos DAGs. 
#   Outro componente é o scheduler, responsável por ler o status das tarefas 
#   e definir ordem de execução.