# 🔐 Affinidi Login Integration Guide (Django)

<div align="center">
  <img src="./images/Affinidi Stacked_FC_RGB.jpg" alt="Affinidi Login Architecture" width="180"/>
</div>

>

> ⚠️ **Warning:**
> This documentation is intended for learning, experimentation, and prototyping only.
> **Do not use this code or configuration as-is in production environments.**
> Affinidi provides no warranty or guarantee for copy-paste usage.
> Please review, test, and secure your implementation before deploying to production.


## 📖 Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Setup Instructions](#setup-instructions)
- [Configuration Example](#configuration-example)
- [Integration Changes](#integration-changes)
- [Code Reference](#code-reference)
- [Further Reading](#further-reading)
- [FAQ](#faq)
- [Disclaimer](#disclaimer)


## 🧭 Overview

**Affinidi Login** enables secure, privacy-preserving, passwordless authentication for your applications using decentralized identity and OID4VP (OpenID for Verifiable Presentations).
It is compatible with industry standards and simplifies authentication flows for both developers and end-users.

# Architecture
Affinidi Login enables developers to adopt password-less authentication flows for their applications with decentralised identity controlled by the user. Affinidi Login can be integrated with applications that support OIDC flow.

<div align="center">
  <img src="./images/login-arch.png" alt="Affinidi Login Architecture" width="800"/>
</div>


## ⚙️ Setup Instructions

### 1. Create Your Affinidi Login Configuration

You can create your configuration using the [Affinidi CLI](https://github.com/affinidi/affinidi-cli#set-up-affinidi-login-for-your-applications) or via the [Affinidi Portal](https://portal.affinidi.com/).

> [!IMPORTANT]
> Add `http://127.0.0.1:8010/callback` to your authorized redirect URIs for local Django development.

### 2. Fill in Client Credentials

After creating your configuration, copy the `Client ID`, `Client Secret`, and `Issuer URL` into your Django `.env` file or set them as environment variables.

## Configuration Example

To create a Login Configuration, you can either use Affinidi CLI or [Affinidi Portal](https://portal.affinidi.com/login)

### Install Affinidi CLI

Follow the guide below if you haven’t installed yet

1. Install Affinidi CLI using NPM

`npm install -g @affinidi/cli`

2. Verify that the installation is successful

`affinidi --version`

> Note: that Affinidi CLI requires Node version 18 and above.

### Create login configuration

1. Log in to Affinidi CLI by running

`affinidi start`

2. Once logged in successfully, create Login Configuration by running

`affinidi login create-config --name='Login Config Name' --redirect-uris='https://example.com/authCallback'`

`--name` is what you want you login configuration to be called

`--redirect-uris` will be the URL where the user will be redirected after successful authorization.

- If you are using Affinidi directly without an identity provider, it should be a URL to your app
  - For Django it would be `http://127.0.0.1:8010/callback`
- If you are using Auth0 as an identity provider it would be `https://{auth0_domain}/login/callback`

**Sample response from Affinidi CLI**

```json
{
  "ari": "ari:identity:ap-southeast-1:xxxx:login_configuration/yyyy",
  "projectId": "xxxx",
  "id": "yyyy",
  "name": "Login Config Name",
  "auth": {
    "clientId": "<CLIENT_ID>",
    "clientSecret": "<CLIENT_SECRET>",
    "issuer": "https://apse1.api.affinidi.io/vpa/v1/login/project/<PROJECT-ID>",
    "tokenEndpointAuthMethod": "client_secret_post"
  },
  "redirectUris": ["http://127.0.0.1:8010/callback"],
  "clientMetadata": {
    "name": "Login Config Name",
    "logo": "https://oidc-vp-adapter-frontend.affinidi.com/default-client-logo.png",
    "origin": "https://example.com"
  },
  "creationDate": "2023-08-11T06:26:37Z"
}
```

> [!IMPORTANT]
> **Keep your Client ID and Client Secret secure.**
> The **Client Secret** is only be shown once.

3. Update login configuration

By default Affinidi Login aks for an Email VC. To request user profile data update login configuration with instruction provided below.

To update first create JSON configuration file with such content:

```json
{
    "presentationDefinition": {
    "id": "vp_combined_email_user_profile_combined",
    "submission_requirements": [
      {
        "rule": "pick",
        "min": 1,
        "from": "A"
      }
    ],
    "input_descriptors": [
      {
        "id": "email_vc",
        "name": "Email VC",
        "purpose": "Check if data contains necessary fields",
        "group": ["A"],
        "constraints": {
          "fields": [
            {
              "path": [
                "$.type"
              ],
              "purpose": "Check if VC type is correct",
              "filter": {
                "type": "array",
                "contains": {
                  "type": "string",
                  "pattern": "Email"
                }
              }
            },
            {
              "path": [
                "$.credentialSubject.email"
              ],
              "purpose": "Check if VC contains email field",
              "filter": {
                "type": "string"
              }
            },
            {
              "path": [
                "$.issuer"
              ],
              "purpose": "Check if VC Issuer is Trusted",
              "filter": {
                "type": "string",
                "pattern": "^did:key:zQ3shtMGCU89kb2RMknNZcYGUcHW8P6Cq3CoQyvoDs7Qqh33N"
              }
            }
          ]
        }
      },
      {
        "id": "profile_vc",
        "name": "Country VC",
        "purpose": "Check if data contains necessary fields",
        "group": ["A"],
        "constraints": {
          "fields": [
            {
              "path": ["$.type"],
              "purpose": "Check if VC type is correct",
              "filter": {
                "type": "array",
                "pattern": "UserProfile"
              }
            },
            {
              "path": ["$.credentialSubject.address.country"],
              "purpose": "Check if VC contains address field",
              "filter": {
                "type": "string"
              }
            }
          ]
        }
      }
    ]
},
  "idTokenMapping": [
    {
      "sourceField": "$.credentialSubject.email",
      "idTokenClaim": "email"
    },
    {
      "sourceField": "$.credentialSubject.address.country",
      "idTokenClaim": "country"
    }
  ]
}

```

After saving file run command:

`affinidi login update-config --id=<LOGIN_CONFIG_ID> --file="<./<name_of_your_file>.json"`

> `--id` identifier of you login configuration
>
> `--file` JSON file path containing you login configuration data


# Integration-related Changes (Django)
To enable passwordless login with Affinidi Login in Django:

- Use the `authlib` library to enable OIDC authentication flows.
- Register Affinidi Login as an OIDC provider in your Django code (see Code Reference below).
- Store client credentials in your `.env` file or as environment variables.



## 💻 Code Reference

When the **Affinidi Login** button is clicked, the following flow is triggered (using Django and Authlib):

1. **User Clicks Login Button:**
  The frontend triggers a redirect to your backend’s `/login` endpoint.

2. **Initiate OIDC Authorization Request:**
  Backend uses Authlib to create an authorization URL for Affinidi’s OIDC provider, including required scopes and redirect URI.

3. **User Authenticates with Affinidi:**
  User is redirected to Affinidi’s login page, authenticates, and consents.

4. **Affinidi Redirects Back:**
  After authentication, Affinidi redirects the user to your backend’s `/callback` endpoint with an authorization code.

5. **Exchange Code for Tokens:**
  Backend uses Authlib to exchange the authorization code for ID and access tokens.

6. **Verify and Extract User Info:**
  Backend verifies the ID token and extracts user claims (e.g., decentralized identifier).

7. **Create Session:**
  Backend creates a session for the user and redirects to the application.

**Example (Django + Authlib):**
```python
from django.shortcuts import render, redirect, reverse
import os
from authlib.integrations.django_client import OAuth
import dotenv
dotenv.load_dotenv()

PROVIDER_ISSUER = os.environ.get("PROVIDER_ISSUER")
PROVIDER_CLIENT_ID = os.environ.get("PROVIDER_CLIENT_ID")
PROVIDER_CLIENT_SECRET = os.environ.get("PROVIDER_CLIENT_SECRET")

oauth = OAuth()
oauth.register(
   "affinidi",
   client_id=PROVIDER_CLIENT_ID,
   client_secret=PROVIDER_CLIENT_SECRET,
   client_kwargs={
      "scope": "openid offline_access",
      "token_endpoint_auth_method": "client_secret_post",
   },
   server_metadata_url=f"{PROVIDER_ISSUER}/.well-known/openid-configuration",
)

def login(request):
   redirect_uri = request.build_absolute_uri(reverse("callback"))
   return oauth.affinidi.authorize_redirect(request, redirect_uri)

def callback(request):
   token = oauth.affinidi.authorize_access_token(request)
   request.session["user"] = token["userinfo"]
   return redirect(request.build_absolute_uri(reverse("dashboard")))

def logout(request):
   request.session.pop("user", None)
   return redirect(request.build_absolute_uri(reverse("home")))
```

**Summary:**
- Button click → `/login` endpoint
- Authlib initiates OIDC flow
- User authenticates with Affinidi and is redirected back
- Authlib exchanges code for tokens and signs in the user


## 📚 Further Reading

- [Affinidi Login Documentation](https://docs.affinidi.com/docs/affinidi-login/)
- [Affinidi CLI](https://github.com/affinidi/affinidi-cli)
- [Affinidi Portal](https://portal.affinidi.com/)


## ❓ FAQ

### What is Affinidi Login?

Affinidi Login is a passwordless authentication solution using decentralized identity and verifiable presentations, compatible with OIDC standards.

### How do I secure my credentials?

Keep your Client ID and Client Secret confidential. Never commit secrets to source control.

### Can I customize the login flow?

Yes, you can update your login configuration to request different credentials or user profile data.

---

## _Disclaimer_

_This documentation is provided for informational purposes only and is not a legal document. For legal terms, conditions, and limitations, please refer to the official Affinidi documentation and your service agreement._


