from kfp.dsl import Input, Model, component


@component(
    base_image="python:3.10-slim",
    packages_to_install=[
        "google-cloud-aiplatform==1.71.1",
        "scikit-learn==1.5.2",
        "joblib==1.4.2",
    ],
)
def upload_model(
    project_id: str,
    location: str,
    model: Input[Model],
):
    from google.cloud import aiplatform

    staging_bucket = "gs://mlops-iris-mish"

    aiplatform.init(
        project=project_id,
        location=location,
        staging_bucket=staging_bucket,
    )

    uploaded_model = aiplatform.Model.upload_scikit_learn_model_file(
        model_file_path=model.path,
        display_name="IrisModelv5",
        project=project_id,
        location=location,
        staging_bucket=staging_bucket,
        serving_container_image_uri="us-docker.pkg.dev/vertex-ai/prediction/sklearn-cpu.1-5:latest",
        sync=True,
    )

    print("Modelo registrado correctamente:")
    print(uploaded_model.resource_name)
