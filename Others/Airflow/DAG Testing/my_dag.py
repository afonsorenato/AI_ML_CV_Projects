
from asyncio.proactor_events import BaseProactorEventLoop
import traceback
import airflow

from airflow import DAG
from random import randint
from datetime import timedelta, datetime
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.bash_operator import BashOperator, BranchPythonOperator



def _training_model():
    return randint(1,10)


def _choose_best_model(ti):
    accuracies = ti.xcom_pull(task_ids = [
        'training_model_A',
        'training_model_B',
        'training_model_C'])

    best_accuracy = max(accuracies)

    if (best_accuracy > 8):
        return 'accurate'
    
    return 'innacurate'


with DAG("my_dag", start_date=datetime(2022, 10, 1),
        schedule_interval="@daily",
        catchup = False) as dag:


    training_model_A = PythonOperator(
        task_id="training_model_A",
        python_callable=_training_model
    )

    training_model_B = PythonOperator(
        task_id="training_model_B",
        python_callable=_training_model
    )

    training_model_C = PythonOperator(
        task_id="training_model_B",
        python_callable=_training_model
    )


    # Choose the best model from all
    choose_best_model = BranchPythonOperator(
        taks_id = "choose_best_model",
        python_callable = _choose_best_model
    )


    # Return if the model is accurate or not
    accurate = BashOperator(
        task_id = "accurate",
        bash_command = "echo 'accurate'"
    )

    inaccurate = BashOperator(
        task_id = "inaccurate",
        bash_command = "echo 'inaccurate'"
    )

    # Dependencies
    [training_model_A, training_model_B, training_model_C] >> choose_best_model >> [accurate, inaccurate]