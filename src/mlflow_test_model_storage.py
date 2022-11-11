import argparse
from random import random, randint
from sklearn.ensemble import RandomForestRegressor

import mlflow
import mlflow.sklearn


def test_model_run_and_storage(experiment_id: str):
    with mlflow.start_run(experiment_id=experiment_id, run_name="YOUR_RUN_NAME") as run:
        params = {"n_estimators": 5, "random_state": 42}
        sk_learn_rfr = RandomForestRegressor(**params)

        # Log parameters and metrics using the MLflow APIs
        mlflow.log_params(params)
        mlflow.log_param("param_1", randint(0, 100))
        mlflow.log_metrics({"metric_1": random(), "metric_2": random() + 1})

        # Log the sklearn model and register as version 1
        mlflow.sklearn.log_model(
            sk_model=sk_learn_rfr,
            artifact_path="sklearn-model",
            registered_model_name="sk-learn-random-forest-reg-model"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script que verifica la correcta creación de un nuevo experimento contra un servidor mlflow."
    )
    parser.add_argument(
        "-experiment-id",
        "--experiment-id",
        type=str,
        help="Id del experimento MLFlow previamente creado.",
        default="0",
    )
    args = parser.parse_args()
    test_model_run_and_storage(args.experiment_id)
