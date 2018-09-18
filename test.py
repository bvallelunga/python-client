from doppler_client import Doppler
import os

API_KEY = os.getenv("DOPPLER_API_KEY", "REPLACE_ME")
PIPELINE = os.getenv("DOPPLER_PIPELINE_ID", "REPLACE_ME")
ENVIRONMENT = os.getenv("DOPPLER_ENVIRONMENT", "development_primary")

doppler = Doppler(
  api_key = API_KEY, 
  pipeline = PIPELINE, 
  environment = ENVIRONMENT,
  defaultPriority = Doppler.DefaultPriority.Remote
)

print(doppler.get("TEST_123"))