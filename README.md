# FastAPI - Cognito

**FastAPI library that eases the usage of AWS Cognito Auth.**  
This library provides basic functionalities for decoding, validation, and parsing Cognito JWT tokens.  
Please note: This library does **not** support sign-up and sign-in features for now.

## Requirements

- Python >= 3.8
- FastAPI
- AWS Cognito Service

## How to Install

You can install the package using pip:

```py
pip install fastapi-cognito
```

## How to Use
Here is a simple example of how to use this package in your FastAPI app:

1. Create FastAPI App

```py
from fastapi import FastAPI

app = FastAPI()
```

All mandatory fields are added in CognitoSettings BaseSettings object. Settings can be added in different ways. You can provide all required settings in .yaml or .json files, or your global BaseSettings object. Note that userpools field is Dict and FIRST user pool in a dict will be set as default automatically if userpool_name is not provided in CognitoAuth object. All fields shown in example below, are also required in .json or .yaml file (with syntax matching those files.)

