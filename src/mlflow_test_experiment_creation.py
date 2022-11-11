import argparse
from pathlib import Path
from random import random

import mlflow

def create_experiment(experiment_name: str):
    # El nombre del experimento debe ser único, en caso contratio obtendremos excepción.
    experiment_id = mlflow.create_experiment(
        experiment_name,
        tags={"version": "v1", "priority": "P1"},
    )

    print(f"Experimento creado correctamente con el id: {experiment_id}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script que verifica la correcta creación de un nuevo experimento contra un servidor mlflow."
    )
    parser.add_argument(
        "-experiment-name",
        "--experiment-name",
        type=str,
        help="Nombre del experimento a crear.",
        default="Mi experimento Mileva "+str(random() + 1),
    )
    args = parser.parse_args()
    create_experiment(args.experiment_name)
