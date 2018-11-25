# Doppler Python Library

[![image](https://img.shields.io/pypi/v/doppler-client.svg)](https://pypi.org/project/doppler-client)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/fce9d6dc0162463aa8142efd0a1c0d5d)](https://www.codacy.com/app/Doppler/python-client?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=DopplerHQ/python-client&amp;utm_campaign=Badge_Grade)

The Doppler Python library provides convenient access to the Doppler API from
applications written for **only** server-side code.

## Installation

Install the package with:

``` bash
pip install -U doppler-client
```

## Usage

The package needs to be configured with your account's api key which is available in your [Doppler account](https://doppler.market/workplace/api_key), pipeline identifier and the environment name:

``` python
from doppler_client import Doppler
import os

doppler = Doppler({
  "api_key": os.getenv("API_KEY"),
  "pipeline": os.getenv("PIPELINE_ID"),
  "environment": os.getenv("ENVIRONMENT_NAME")
})

# Rest of Application
```

## Key Best Practices

So if Doppler stores my environment keys, where should I keep my Doppler API keys?

That is a great question! We recommend storing your `API_KEY`, `PIPELINE_ID`, and `ENVIRONMENT_NAME` 
in local environment. That means the only keys you should be storing in your local environment are the Doppler keys. All other keys should be be fetched by the Doppler client.

### Fetch Environment Keys

You can fetch your environment keys from Doppler by calling the `get(name)` method.

``` python
doppler.get(KEY_NAME)
```

Here is an example:

``` python
config = {
  segment_key: doppler.get("SEGMENT_API_KEY"),
  algolia_key: doppler.get("ALGOLIA_API_KEY")
}

```

If there are differences between the values your local environment sets and the ones on Doppler, the client will use the ones provided by Doppler. You can override this behavior by passing in a second argument to the `get(key_name, priority)` method that sets the priority to favor your local environment.

For example:

``` python
# Local Enviroment
os.environ["MAGICAL_KEY"] = "123"

# Doppler
MAGICAL_KEY = "456"


# Default Behavior
doppler.get("MAGICAL_KEY") # => "456"

# Override to Local
doppler.get("MAGICAL_KEY", Doppler.Priority.Local) # => "123"
```

You can also set the priority globally on initialization:

``` python
doppler = Doppler({
  "api_key": os.getenv("API_KEY"),
  "pipeline": os.getenv("PIPELINE_ID"),
  "environment": os.getenv("ENVIRONMENT_NAME"),
  "priority": Doppler.Priority.Local
})

```

## Local Key Privacy

By default the Doppler client will only track the local environment keys that are used during `doppler.get()`.
Collecting only those local keys helps us automatically setup your pipelines
for immediate use. After setup we also use your keys to detect when your keys locally have
changed from what is on Doppler. We then provide a way for you to adopt or reject those changes
through our dashboard. This can help help when debugging silent bugs or build failures.

### Track Additional Keys
The Doppler client can also track additional keys by providing an array of keys to the `track_keys` field.

``` python
doppler = Doppler({
  "api_key": os.getenv("API_KEY"),
  "pipeline": os.getenv("PIPELINE_ID"),
  "environment": os.getenv("ENVIRONMENT_NAME"),
  "track_keys": [
    "KEY_TO_TRACK"
  ]
})
```

### Ignoring Specific Keys
Inversely, you can also ignore specific local keys by adding them to the `ignore_keys` array.

``` python
doppler = Doppler({
  "api_key": os.getenv("API_KEY"),
  "pipeline": os.getenv("PIPELINE_ID"),
  "environment": os.getenv("ENVIRONMENT_NAME"),
  "ignore_keys": [
    "SUPER_SECRET_KEY"
  ]
})
```

## Overriding Local Keys

The Doppler client by default will not override your local environment keys because it
can create unknown side effects if the developer didn't take this into account. But 
if you would like Doppler to override your local environment keys, you can do it for 
all variables on Doppler or just the ones you specify.

### Globally
To have all your local keys  overridden by Doppler's remote keys, set the `override_local_keys` attribute to `true`.

``` python
doppler = Doppler({
  "api_key": os.getenv("API_KEY"),
  "pipeline": os.getenv("PIPELINE_ID"),
  "environment": os.getenv("ENVIRONMENT_NAME"),
  "override_local_keys": True # DEFAUTLS => False
})
```

### Individual Key
You can also override specific local keys by setting `override_local_keys` to be an array of keys.

``` python
doppler = Doppler({
  "api_key": os.getenv("API_KEY"),
  "pipeline": os.getenv("PIPELINE_ID"),
  "environment": os.getenv("ENVIRONMENT_NAME"),
  "override_local_keys": [
    "PORT",
    "SPECIAL_KEY"
  ]
})
```

## Extra Information

- [Doppler](https://doppler.market)
- [API KEY](https://doppler.market/workplace/api_key)
