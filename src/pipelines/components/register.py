from kfp.dsl import Input, Model, component


@component(
    base_image="python:3.10-slim",
    packages_to_install=[
        "google-cloud-aiplatform==1.71.1",
        "google-cloud-storage==2.18.2",
        "scikit-learn==1.5.2",
        "joblib==1.4.2",
    ],
)
def upload_model(
    project_id: str,
    location: str,
    model: Input[Model],
):
    import os
    import uuid

    from google.cloud import aiplatform, storage

    bucket_name = "mlops-iris-mish"
    model_dir = f"models/iris-model/{uuid.uuid4()}"
    model_file_name = "model.joblib"

    local_model_path = model.path
    gcs_model_path = f"{model_dir}/{model_file_name}"
    artifact_uri = f"gs://{bucket_name}/{model_dir}"

    storage_client = storage.Client(project=project_id)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(gcs_model_path)
    blob.upload_from_filename(local_model_path)

    print(f"Modelo subido a: gs://{bucket_name}/{gcs_model_path}")

    aiplatform.init(
        project=project_id,
        location=location,
        staging_bucket=f"gs://{bucket_name}",
    )

    uploaded_model = aiplatform.Model.upload(
        display_name="IrisModelv5",
        artifact_uri=artifact_uri,
        serving_container_image_uri="us-docker.pkg.dev/vertex-ai/prediction/sklearn-cpu.1-5:latest",
        project=project_id,
        location=location,
        sync=True,
    )

    print("Modelo registrado correctamente:")
    print(uploaded_model.resource_name)
