# Affinidi Django Reference Implementation

This is a template that showcases how you can enable your applications to issue credentials to users and store them in their Affinidi Vault. It accomplishes this through Affinidi Vault using the [OpenID for Verifiable Credential Issuance](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html) and [OpenID for Verifiable Presentations specification.](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html) specification.

Additonaly, It also show capabilites for Affinidi Verification, Affinidi Revocation and Affinidi Identity Verification.

This project is a Django(python) Project and uses Html pages for frontend

## Getting Started

These instructions will help you to get this project up and running on your local machine for development and testing purposes.

copy `.env.example` to `.env`:

```
cp .env.example .env
```

## Build and run the project:

```sh
python manage.py startapp webapp
python manage.py migrate
python manage.py runserver
python manage.py runserver 8010

```

Then visit: http://127.0.0.1:8010/ to browse the reference app

## Affinidi Configurations

1. Click here to [Set up your environment variables for Affinidi Login configuration](./docs/setup-login-config.md)
2. Click here to [Set up your Personnel Access Token to interact with Affinidi services](./docs/create-pat.md)
3. Click here to [Set up your Credential Issuance Configuration](./docs/cis-configuration.md)
4. Click here to [Set up your environment variables for Affinidi Iota configuration](./docs/setup-iota-config.md)
5. Click here to [Set up your environment Variables for Affinidi IDV Configuration](./docs/setup-idv-config.md)

## Read More

Explore our [documentation](https://docs.affinidi.com/docs/) and [labs](https://docs.affinidi.com/labs/) to learn more about integrating Affinidi Login with Affinidi Vault.

## Telemetry

Affinidi collects usage data to improve our products and services. For information on what data we collect and how we use your data, please refer to our [Privacy Notice](https://www.affinidi.com/privacy-notice).

## Feedback, Support, and Community

[Click here](https://github.com/affinidi/reference-app-affinidi-vault/issues) to create a ticket and we will get on it right away. If you are facing technical or other issues, you can [Contact Support](https://share.hsforms.com/1i-4HKZRXSsmENzXtPdIG4g8oa2v).


## FAQ

### What can I develop?

You are only limited by your imagination! Affinidi Reference Applications is a toolbox with which you can build software apps for personal or commercial use.

### Is there anything I should not develop?

We only provide the tools - how you use them is largely up to you. We have no control over what you develop with our tools - but please use our tools responsibly!

We hope that you will not develop anything that contravenes any applicable laws or regulations. Your projects should also not infringe on Affinidi’s or any third party’s intellectual property (for instance, misusing other parties’ data, code, logos, etc).

### What responsibilities do I have to my end-users?

Please ensure that you have in place your own terms and conditions, privacy policies, and other safeguards to ensure that the projects you build are secure for your end users.

If you are processing personal data, please protect the privacy and other legal rights of your end-users and store their personal or sensitive information securely.

Some of our components would also require you to incorporate our end-user notices into your terms and conditions.

### Are Affinidi Reference Applications free for use?

Affinidi Reference Applications are free, so come onboard and experiment with our tools and see what you can build! We may bill for certain components in the future, but we will inform you beforehand.

### Do I need to provide you with anything?

From time to time, we may request certain information from you to ensure that you are complying with the [Terms and Conditions](https://www.affinidi.com/terms-conditions).

### Can I share my developer’s account with others?

When you create a developer’s account with us, we will issue you your private login credentials. Please do not share this with anyone else, as you would be responsible for activities that happen under your account. If you have friends who are interested, ask them to sign up – let's build together!

## _Disclaimer_

_Please note that this FAQ is provided for informational purposes only and is not to be considered a legal document. For the legal terms and conditions governing your use of the Affinidi Reference Applications, please refer to our [Terms and Conditions](https://www.affinidi.com/terms-conditions)._
