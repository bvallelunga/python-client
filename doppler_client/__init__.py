import requests
from requests_futures.sessions import FuturesSession
import json
import os
from enum import Enum
import pkg_resources


try:
  set
except NameError:
  from sets import Set as set


# Doppler Class
class Doppler:
  
  host = os.getenv('DOPPLER_HOST', "https://api.doppler.com")
  max_retries = 10
  remote_keys = {}
  
  
  def __init__(self, data={}):
    data["api_key"] = data.get("api_key", os.getenv("DOPPLER_API_KEY"))
    data["pipeline"] = data.get("pipeline", os.getenv("DOPPLER_PIPELINE"))
    data["environment"] = data.get("environment", os.getenv("DOPPLER_ENVIRONMENT"))
    
    if data.get("api_key") is None:
      raise ValueError("Please provide an 'api_key' on initialization.")
      
    if data.get("pipeline") is None:
      raise ValueError("Please provide an 'pipeline' on initialization.")
      
    if data.get("environment") is None:
      raise ValueError("Please provide an 'environment' on initialization.")
      
    self.api_key = str(data.get("api_key"))
    self.pipeline = str(data.get("pipeline"))
    self.environment = str(data.get("environment"))
    self.ignore_variables = set(data.get("ignore_variables", []))
    self.backup_filepath = data.get("backup_filepath")
    self.startup()
  
  
  
  def startup(self):
    response = self._request("/fetch_keys", {})
    
    if response:
      self.remote_keys = response["keys"]
      self.override_keys()
      self.write_backup()
      
  
  def override_keys(self):
    for key in self.remote_keys:
      if key not in self.ignore_variables:
        os.environ[key] = self.remote_keys.get(key)
        
        
  def write_backup(self):
    if not self.backup_filepath: return
    
    body = ""
    
    for key in self.remote_keys:
      body += key + "=" + self.remote_keys.get(key) + "\n"
    
    f = open(self.backup_filepath, "w")
    f.write(body)
    f.close()
  
  
  def _request(self, endpoint, body, retry_count=0, isAsync=False):
    try:
      endpoint = self.host + "/environments/" + self.environment + endpoint
      requester = requests
      
      if isAsync:
        requester = FuturesSession()
      
      response = requester.post(endpoint, json=body, headers={
        "api-key": self.api_key,
        "pipeline": self.pipeline,
        "client-sdk": "python",
        "client-version": pkg_resources.require("doppler-client")[0].version
      }, timeout=1500)
      
      if response is None or isAsync: return None
      
      response = response.json()
      
      if not response["success"]:
        raise ValueError(". ".join(response["messages"]))
        
      return response
      
    except requests.exceptions.RequestException:
      retry_count += 1
      
      if retry_count > self.max_retries:
        if self.backup_filepath is not None and os.path.isfile(self.backup_filepath):
          f = open(self.backup_filepath, "r")
          body = f.read()
          
          keys = {}
          for line in body.split("\n"):
            parts = line.split("=")
            
            if len(parts) == 2:
              keys[parts[0]] = parts[1]
            
          return { "keys": keys }

        print("DOPPLER: Failed to reach Doppler servers after " + retry_count + " retries...\n")
        return None

      return self._request(endpoint, body, retry_count)
