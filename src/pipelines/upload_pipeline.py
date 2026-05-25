from kfp.registry import RegistryClient

PROJECT_ID = "project-c2c38c0d-53a2-459c-a19"
REGION = "southamerica-west1"
REPOSITORY = "mlops-iris"

client = RegistryClient(host=f"https://{REGION}-kfp.pkg.dev/{PROJECT_ID}/{REPOSITORY}")

template_name, version_name = client.upload_pipeline(
    file_name="pipeline.yaml",
    tags=["v1", "latest"],
    extra_headers={"description": "Pipeline Iris v1 - Mish"},
)

print("Template:", template_name)
print("Version:", version_name)
