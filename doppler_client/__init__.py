import requests
from requests_futures.sessions import FuturesSession
import json
import os
from enum import Enum
from sets import Set


class Doppler:
  
  class Priority(Enum):
    Local = 1
    Remote = 2 
  
  host = os.getenv('DOPPLER_HOST', "https://api.doppler.market")
  max_retries = 10
  remote_keys = {}
  
  
  def __init__(self, api_key, pipeline, environment, priority=Priority.Remote, send_local_keys=True, ignore_keys=[]):
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
    self.send_local_keys = send_local_keys
    self.ignore_keys = ignore_keys
    self._set_ignore_keys = None
    self.startup()
  
  
  
  def startup(self):
    keys_to_send = {}
    local_keys = os.environ.copy()
    self._set_ignore_keys = Set(self.ignore_keys)
    
    if self.send_local_keys:   
      for key in local_keys:
        value = local_keys[key]
        
        if key not in self._set_ignore_keys:
          keys_to_send[key] = value
    
    
    print(keys_to_send)
    response = self._request("/fetch_keys", {
      "local_keys": keys_to_send
    })
    
    if response:
      self.remote_keys = response["keys"]
      

      
  def get(self, key_name, priority=None):
      priority = priority or self.defaultPriority
      
      if key_name in self.remote_keys:
        if priority == Doppler.Priority.Local:
          return os.getenv(key_name, self.remote_keys[key_name])
          
        return self.remote_keys[key_name]
      
      if key_name not in self._set_ignore_keys:
        self._request("/missing_key", {
          "key_name": key_name
        }, isAsync=True)
      
      return os.getenv(key_name)
    
  
    
  def _request(self, endpoint, body, retry_count=0, isAsync=False):
    try:
      endpoint = self.host + "/environments/" + self.environment + endpoint
      requester = requests
      
      if isAsync:
        requester = FuturesSession()
      
      response = requester.post(endpoint, json=body, headers={
        "api-key": self.api_key,
        "pipeline": self.pipeline
      }, timeout=1500)
      
      if response is None or isAsync: return None
      
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
