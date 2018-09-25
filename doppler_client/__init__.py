import requests
from requests_futures.sessions import FuturesSession
import json
import os
from enum import Enum


class Doppler:
  
  class Priority(Enum):
    Local = 1
    Remote = 2 
  
  host = os.getenv('DOPPLER_HOST', "https://api.doppler.market")
  max_retries = 10
  remote_keys = {}
  
  
  def __init__(self, api_key, pipeline, environment, priority=Priority.Remote):
    if api_key is None:
      raise ValueError("Please provide an 'api_key' on initialization.")
      
    if pipeline is None:
      raise ValueError("Please provide an 'pipeline' on initialization.")
      
    if environment is None:
      raise ValueError("Please provide an 'environment' on initialization.")
      
    self.api_key = str(api_key)
    self.pipeline = str(pipeline)
    self.environment = str(environment)
    self.defaultPriority = priority or Priority.Remote
    self.startup()
  
  
  
  def startup(self):
    response = self._request("/fetch_keys", {
      "local_keys": os.environ.copy()
    })
    
    if response:
      self.remote_keys = response["keys"]
      
  
      
  def get(self, key_name, priority=None):
      priority = priority or self.defaultPriority
      
      if key_name in self.remote_keys:
        if priority == Doppler.Priority.Local:
          return os.getenv(key_name, self.remote_keys[key_name])
          
        return self.remote_keys[key_name]
        
      self._request("/missing_key", {
        "key_name": key_name
      }, async=True)
      
      return os.getenv(key_name)
    
  
    
  def _request(self, endpoint, body, retry_count=0, async=False):
    try:
      endpoint = self.host + "/environments/" + self.environment + endpoint
      requester = requests
      
      if async:
        requester = FuturesSession()
      
      response = requester.post(endpoint, json=body, headers={
        "api-key": self.api_key,
        "pipeline": self.pipeline
      }, timeout=1500)
      
      if not response or async: return None
      
      response = response.json()
      
      if not response["success"]:
        raise ValueError(". ".join(response["messages"]))
        
      return response
      
    except requests.exceptions.RequestException:
      retry_count += 1
      
      if retry_count > self.max_retries: 
        print("DOPPLER: Failed to reach Doppler servers. Stopping retries...\n")
        return None
      
      print("DOPPLER: Failed to reach Doppler servers. Retrying for the " + retry_count + " time now...\n")
      return self._request(endpoint, body, retry_count)
