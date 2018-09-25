# Doppler Python Library

[![image](https://img.shields.io/pypi/v/doppler-client.svg)](https://pypi.org/project/doppler-client)
[![image](https://img.shields.io/pypi/dm/doppler-client.svg)](https://pypi.org/project/doppler-client)

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

doppler = Doppler(
  api_key = os.getenv("API_KEY"),
  pipeline = os.getenv("PIPELINE_ID"),
  environment = os.getenv("ENVIRONMENT_NAME")
)

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
doppler = Doppler(
  api_key = os.getenv("API_KEY"),
  pipeline = os.getenv("PIPELINE_ID"),
  environment = os.getenv("ENVIRONMENT_NAME"),
  priority = Doppler.Priority.Local
)

```


## Extra Information

- [Doppler](https://doppler.market)
- [API KEY](https://doppler.market/workplace/api_key)

