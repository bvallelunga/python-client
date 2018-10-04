from doppler_client import Doppler
import os

os.environ["TESTER"] = "789"

API_KEY = os.getenv("DOPPLER_API_KEY", "RbZ7vIrfbOkZF6hDMKDDdhVoYA0AzBqL8An9OAOL")
PIPELINE = os.getenv("DOPPLER_PIPELINE_ID", "31")
ENVIRONMENT = os.getenv("DOPPLER_ENVIRONMENT", "development_python")

doppler = Doppler(
  api_key = API_KEY, 
  pipeline = PIPELINE, 
  environment = ENVIRONMENT,
  priority = Doppler.Priority.Remote
)

print(doppler.get("abc"))
print(doppler.get("TESTER"))