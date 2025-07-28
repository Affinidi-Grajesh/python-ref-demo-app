import logging
import affinidi_tdk_auth_provider
import affinidi_tdk_credential_issuance_client
import os
import jwt
import time
import affinidi_tdk_credential_verification_client
from dotenv import load_dotenv
load_dotenv()

# Environment variables
api_gateway_url = os.environ.get("API_GATEWAY_URL", "")
token_endpoint = os.environ.get("TOKEN_ENDPOINT", "")
project_id = os.environ.get("PROJECT_ID", "")
private_key = os.environ.get("PRIVATE_KEY", "")
if private_key:
    private_key = private_key.replace("\\n", "\n")
token_id = os.environ.get("TOKEN_ID", "")
passphrase = os.environ.get("PASSPHRASE", "")
key_id = os.environ.get("KEY_ID", "")
vault_url = os.environ.get("VAULT_URL", "")

configuration_id = os.environ.get("CONFIGURATION_ID", "")

TOKEN_FILE_PATH = "token/pst_response.jwt"


def pst():
    print("Fetching project scoped token...")

    stats = {
        "apiGatewayUrl": api_gateway_url,  # Assuming these are defined elsewhere
        "tokenEndpoint": token_endpoint,
        "projectId": project_id,
        "privateKey": private_key,
        "tokenId": token_id,
        "vaultUrl": vault_url,
    }

    # Check if the token file exists and if it has a valid, unexpired token
    if os.path.exists(TOKEN_FILE_PATH):
        try:
            with open(TOKEN_FILE_PATH, "r") as f:
                stored_token = (
                    f.read().strip()
                )  # Read token from file and remove leading/trailing whitespace

            if stored_token:  # Check if the file is not empty
                decoded_token = jwt.decode(
                    stored_token, options={"verify_signature": False}
                )  # Decode without signature verification for expiry check

                if "exp" in decoded_token and decoded_token["exp"] > time.time():
                    print("Using stored valid token from file.")
                    return stored_token  # Return the stored token if it's valid and not expired
                else:
                    print(
                        "Stored token expired or 'exp' claim missing. Fetching new token."
                    )
        except (
            FileNotFoundError,
            jwt.PyJWTError,
            Exception,
        ) as e:  # Catch file errors, JWT decode errors, and other potential issues
            print(f"Error reading or decoding stored token: {e}. Fetching new token.")
            # In case of any error, proceed to fetch a new token
    else:
        print("Token file not found. Fetching new token.")

    # If no valid stored token is found (or file doesn't exist or errors occurred), fetch a new one
    authProvider = affinidi_tdk_auth_provider.AuthProvider(stats)
    projectScopedToken = authProvider.fetch_project_scoped_token()
    print("projectScopedToken (newly fetched)", projectScopedToken)

    # Store the newly fetched token to the file for future use
    try:
        os.makedirs(
            os.path.dirname(TOKEN_FILE_PATH), exist_ok=True
        )  # Ensure directory exists
        with open(TOKEN_FILE_PATH, "w") as f:
            f.write(projectScopedToken)
        print(f"New token stored in {TOKEN_FILE_PATH}")
    except IOError as e:
        print(f"Error writing token to file {TOKEN_FILE_PATH}: {e}")
        # Consider what to do if saving the token fails. Maybe return the token anyway, or raise an exception.
        # For now, we'll just print an error and return the token

    return projectScopedToken


def startIssuance(payload_for_issuance_api):
    try:
        if not payload_for_issuance_api:
            return {"success": False, "error": "No credentials request provided"}
        configuration = affinidi_tdk_credential_issuance_client.Configuration()
        configuration.api_key["ProjectTokenAuth"] = pst()
        with affinidi_tdk_credential_issuance_client.ApiClient(
            configuration
        ) as api_client:
            api_instance = affinidi_tdk_credential_issuance_client.IssuanceApi(
                api_client
            )
            projectId = project_id
            request_json = {"data": [payload_for_issuance_api], "claimMode": "TX_CODE"}
            print("request_json", request_json)

            start_issuance_input = (
                affinidi_tdk_credential_issuance_client.StartIssuanceInput.from_dict(
                    request_json
                )
            )
            api_response = api_instance.start_issuance(
                projectId, start_issuance_input=start_issuance_input
            )

            response = api_response.to_dict()
            response["vaultLink"] = (
                vault_url
                + f"/claim?credential_offer_uri={response['credentialOfferUri']}"
            )
            print("response", response)
        return response
    except Exception as e:
        logging.error(f"Error processing checks: {e}")
        return {"success": False, "error": str(e)}

def get_credentials(issuance_id):
    try:
        if not issuance_id:
            return {"success": False, "error": "No issuanceId provided"}

        print("Fetching credentials for issuanceId:", issuance_id)
        print("Using configuration_id:", configuration_id)
        print("Using project_id:", project_id)
        configuration = affinidi_tdk_credential_issuance_client.Configuration()
        configuration.api_key["ProjectTokenAuth"] = pst()
        with affinidi_tdk_credential_issuance_client.ApiClient(configuration) as api_client:
            api_instance = affinidi_tdk_credential_issuance_client.CredentialsApi(api_client)
            projectId = project_id
            response = api_instance.get_issuance_id_claimed_credential(projectId, configuration_id, issuance_id)
            print("response", response)
            return response.to_dict()
    except Exception as e:
        logging.error(f"Error fetching credentials: {e}")
        return {"success": False, "error": str(e)}


def listIssuanceDataRecords():
    try:
        configuration = affinidi_tdk_credential_issuance_client.Configuration()
        configuration.api_key["ProjectTokenAuth"] = pst()
        with affinidi_tdk_credential_issuance_client.ApiClient(configuration) as api_client:
            api_instance = affinidi_tdk_credential_issuance_client.DefaultApi(api_client)
            response = api_instance.list_issuance_data_records(project_id, configuration_id)
            return response.to_dict()
    except Exception as e:
        logging.error(f"Error listing issuance data records: {e}")
        return {"success": False, "error": str(e)}


def revoke_credential_util(revoke_credential_input):
    try:
        if not revoke_credential_input:
            return {"success": False, "error": "No issuanceId provided"}

        configuration = affinidi_tdk_credential_issuance_client.Configuration()
        configuration.api_key["ProjectTokenAuth"] = pst()
        with affinidi_tdk_credential_issuance_client.ApiClient(configuration) as api_client:
            api_instance = affinidi_tdk_credential_issuance_client.DefaultApi(
                api_client
            )

            response = api_instance.change_credential_status(
                project_id,
                configuration_id,
                change_credential_status_input=affinidi_tdk_credential_issuance_client.ChangeCredentialStatusInput.from_dict(
                    revoke_credential_input
                ),
            )
            return response.to_dict()
    except Exception as e:
        logging.error(f"Error revoking credential: {e}")
        return {"success": False, "error": str(e)}

def verify_credential_util(verify_credential_input):
    try:
        if not verify_credential_input:
            return {"success": False, "error": "No Credential provided to verify"}

        print("Verifying credential for issuanceId:", verify_credential_input)
        configuration = affinidi_tdk_credential_verification_client.Configuration()
        configuration.api_key["ProjectTokenAuth"] = pst()
        with affinidi_tdk_credential_verification_client.ApiClient(configuration) as api_client:
            api_instance = affinidi_tdk_credential_verification_client.DefaultApi(api_client)
            response = api_instance.verify_credentials(
                verify_credential_input=affinidi_tdk_credential_verification_client.VerifyCredentialInput.from_dict(
                    verify_credential_input
                ),
            )
            return response.to_dict()
    except Exception as e:
        logging.error(f"Error verifying credential: {e}")
        return {"success": False, "error": str(e)}
