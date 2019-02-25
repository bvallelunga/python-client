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

The package needs to be configured with your account's api key which is available in your [Doppler account](https://doppler.com/workplace/api_key), pipeline identifier and the environment name:


### Environment Variables Required
Please add these environment variables to your `.env` file or infra provider.

```
DOPPLER_API_KEY = <API Key>
DOPPLER_PIPELINE = <Pipeline ID>
DOPPLER_ENVIRONMENT = <Environment Name>
```

### Simple Install
This installation method will expect the `DOPPLER_API_KEY`, `DOPPLER_PIPELINE`, `DOPPLER_ENVIRONMENT` as environment variables.

``` python
from doppler_client import Doppler
Doppler()


# Rest of Application
example_variable = os.getenv("EXAMPLE_VARIABLE")
```

### Install with Arguments
This installation method will expect the `api_key`, `pipeline`, `environment` as arguments.

``` python
from doppler_client import Doppler

Doppler({
  "api_key": os.getenv("DOPPLER_API_KEY"),
  "pipeline": os.getenv("DOPPLER_PIPELINE"),
  "environment": os.getenv("DOPPLER_ENVIRONMENT")
})


# Rest of Application
example_variable = os.getenv("EXAMPLE_VARIABLE")
```

## Key Best Practices

So if Doppler stores my environment variables, where should I keep my Doppler API keys?

That is a great question! We recommend storing your `DOPPLER_API_KEY`, `DOPPLER_PIPELINE`, and `DOPPLER_ENVIRONMENT` 
in a `.env` file or with your infra provider. That means the only variables you should be storing in your local environment are the Doppler keys. All other variables should be be fetched by the Doppler client.


## Ignoring Specific Variables

In the case you would want to ignore specific variables from Doppler, say a port set by Heroku, you can add it the `ignore_variables` field.

``` js
from doppler_client import Doppler

Doppler({
  "ignore_variables": ["PORT"]
})
```

## Fallback to Backup

The Doppler client accepts a `backup_filepath` on init. If provided the client will write
the Doppler variables to a backup file. If the Doppler client fails to connect to our API
endpoint (very unlikely), the client will fallback to the keys provided in the backup file.

``` js
from doppler_client import Doppler

Doppler({
  "backup_filepath": "./backup.env"
})
```

## Extra Information

  - [Doppler](https://doppler.com)
  - [API KEY](https://doppler.com/workplace/api_key)
