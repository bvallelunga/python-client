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
  
  host = os.getenv('DOPPLER_HOST', "https://deploy.doppler.com")
  max_retries = 10
  remote_keys = {}
  
  
  def __init__(self, data={}):
    env = self.read_env(data.get("env_filepath", ".env")) or {}
    data["api_key"] = data.get("api_key", os.getenv("DOPPLER_API_KEY", env.get("DOPPLER_API_KEY")))
    data["pipeline"] = data.get("pipeline", os.getenv("DOPPLER_PIPELINE", env.get("DOPPLER_PIPELINE")))
    data["environment"] = data.get("environment", os.getenv("DOPPLER_ENVIRONMENT", env.get("DOPPLER_ENVIRONMENT")))
    
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
    self.override = data.get("override", True)
    self.startup()
  
  
  
  def startup(self):
    response = self._request("/v1/variables")
    
    if response:
      self.remote_keys = response["variables"]
      self.write_backup()
      
      if self.override:
        self.override_keys()
      
  
  def override_keys(self):
    for key in self.remote_keys:
      if key not in self.ignore_variables:
        os.environ[key] = self.remote_keys.get(key)
        
        
  def write_backup(self):
    if not self.backup_filepath: return
    
    body = ""
    
    for key in self.remote_keys:
      body += key + "=\"" + self.remote_keys.get(key) + "\"\n"
    
    f = open(self.backup_filepath, "w")
    f.write(body)
    f.close()
    
  
  def read_env(self, path):
    if path is None or not os.path.isfile(path):
      return None

    f = open(path, "r")
    body = f.read()
    
    keys = {}
    for line in body.split("\n"):
      parts = line.split("=")
      
      if len(parts) == 2:
        keys[parts[0].strip()] = parts[1].strip()

    return keys
 
  
  def get(self, name):
    return self.remote_keys.get(name)
    
    
  def get_all(self):
    return self.remote_keys
  
  
  def _request(self, endpoint, retry_count=0, isAsync=False):
    try:
      endpoint = self.host + endpoint
      requester = requests
      
      if isAsync:
        requester = FuturesSession()
      
      response = requester.get(endpoint, params={
        "environment": self.environment,
        "pipeline": self.pipeline
      }, headers={
        "api-key": self.api_key,
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
        backup_env = self.read_env(self.backup_filepath)
        
        if backup_env is not None:
          return { "variables": backup_env }

        raise ValueError("DOPPLER: Failed to reach Doppler servers after " + retry_count + " retries...\n")
        return None

      return self._request(endpoint, retry_count, isAsync)
