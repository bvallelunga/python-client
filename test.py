from doppler_client import Doppler
import os

os.environ["TESTER"] = "123"

API_KEY = os.getenv("DOPPLER_API_KEY", "vSNdjLhatIkD8w6F1W0IEDvKfflbTUkRh8AvghaA")
PIPELINE = os.getenv("DOPPLER_PIPELINE_ID", "31")
ENVIRONMENT = os.getenv("DOPPLER_ENVIRONMENT", "development_python")

doppler = Doppler({
  "api_key": API_KEY,
  "pipeline": PIPELINE,
  "environment": ENVIRONMENT,
  "priority": Doppler.Priority.Remote
})

print(doppler.get("abc"))
print(doppler.get("TESTER"))