import pandas as pd
from google.cloud import bigquery
from sklearn.datasets import load_iris

PROJECT_ID = "project-c2c38c0d-53a2-459c-a19"
DATASET_ID = "iris"
TABLE_ID = "iris"
LOCATION = "US"

iris = load_iris(as_frame=True)

df = iris.frame.copy()
df = df.rename(
    columns={
        "sepal length (cm)": "SepalLengthCm",
        "sepal width (cm)": "SepalWidthCm",
        "petal length (cm)": "PetalLengthCm",
        "petal width (cm)": "PetalWidthCm",
        "target": "Species",
    }
)

target_names = iris.target_names
df["Species"] = df["Species"].apply(lambda x: f"Iris-{target_names[x]}")

client = bigquery.Client(project=PROJECT_ID)

dataset_ref = bigquery.Dataset(f"{PROJECT_ID}.{DATASET_ID}")
dataset_ref.location = LOCATION

client.create_dataset(dataset_ref, exists_ok=True)

table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

job = client.load_table_from_dataframe(
    df,
    table_ref,
    job_config=bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE"),
)

job.result()

print(f"Tabla creada correctamente: {table_ref}")
print(df.head())
