from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, constr
import boto3

# from phone import phone_number

app = FastAPI()

USER_POOL_ID = 'us-east-1_FeS5tGHlV'
CLIENT_ID = 'ft3fomorthrbv3oqco7is8jnd'

client = boto3.client('cognito-idp', region_name='us-east-1')


class Userdata(BaseModel):
    email: EmailStr
    phone_number: constr()


class SocialLoginRequest(BaseModel):
    access_token: str   # Token from the social provider (Google, Facebook, etc.)
    provider_name: str  # Name of the social provider (e.g., Google, Facebook)


class User(BaseModel):
    username: str
    password: str


class VerifyOtpCommand(BaseModel):
    session: str
    code: str
    challenge_name: str
    username: str


# Signup endpoint
@app.post('/signup')
def signup(user: User, request: Userdata):
    try:
        response = client.sign_up(
            ClientId=CLIENT_ID,
            Username=user.username,
            Password=user.password,
            UserAttributes=[
                {'Name': 'email', 'Value': request.email},
                {'Name': 'phone_number', 'Value': request.phone_number},
            ]
        )
        return {'message': 'User signed up successfully'}
    except client.exceptions.UsernameExistsException:
        raise HTTPException(status_code=400, detail='Username already exists')
    except client.exceptions.ClientError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post('/login')
def login(user: User):
    try:
        response = client.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH',  # USER_PASSWORD_AUTH
            AuthParameters={
                'USERNAME': user.username,
                'PASSWORD': user.password
            }
        )
        auth_result = response.get("AuthenticationResult", None)
        challenge_name = response.get("ChallengeName", None)
        if auth_result:
            access_token = auth_result.get('AccessToken')
            refresh_token = auth_result.get('RefreshToken')
            id_token = auth_result.get('IdToken')
            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'id_token': id_token
            }
        elif challenge_name == "SMS_MFA":
            return {'challenge_name': response.get("ChallengeName"), "session": response.get("Session")}
    except client.exceptions.NotAuthorizedException:
        raise HTTPException(status_code=401, detail='Incorrect username or password')
    except client.exceptions.UserNotFoundException:
        raise HTTPException(status_code=404, detail='User does not exist')
    except client.exceptions.ClientError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post('/refresh_token')
def refresh_token(refresh_token: str):
    try:
        response = client.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow="REFRESH_TOKEN",
            AuthParameters={
                "REFRESH_TOKEN": refresh_token
            })
        return response
    except client.exceptions.ClientError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/social-login")
async def social_login(request: SocialLoginRequest):
    try:
        response = client.get_id(
            IdentityPoolId='us-east-1:example-pool-id',  # Replace with your Identity Pool ID
            Logins={
                f'cognito-idp.us-east-1.amazonaws.com/us-east-1_example': request.access_token
            }
        )

        # Exchange the login token for Cognito credentials
        identity_id = response['IdentityId']

        # Authenticate user with Cognito
        cognito_response = client.get_open_id_token_for_developer_identity(
            IdentityPoolId='us-east-1:example-pool-id',  # Replace with your Identity Pool ID
            Logins={
                f'{request.provider_name}.com': request.access_token
            }
        )

        return JSONResponse(content={"message": "Social login successful",
                                     "identity_id": identity_id,
                                     "token": cognito_response['Token']}
                            )

    except client.exceptions.NotAuthorizedException as e:
        raise HTTPException(status_code=401, detail="Invalid credentials or access token.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
