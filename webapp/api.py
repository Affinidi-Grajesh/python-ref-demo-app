from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .services import build_credentials_request
import logging
from .util import get_credentials, pst, startIssuance, listIssuanceDataRecords, revoke_credential_util, verify_credential_util

logger = logging.getLogger(__name__)


def api_hello(request):
    return JsonResponse({"message": "Hello from the backend API!"})


@csrf_exempt
def issue_credential(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            type_id = data.get("credentialType")
            if not type_id:
                return JsonResponse({"error": "typeId is required"}, status=400)

            credentials_request = build_credentials_request(type_id)
            if (
                credentials_request is None
                or not credentials_request
                or credentials_request[0].get("credentialTypeId") is None
                or credentials_request[0].get("credentialData") is None
            ):
                return JsonResponse(
                    {"error": "Missing credentialTypeId or credentialData"}, status=400
                )

            result = startIssuance(credentials_request[0])
            return JsonResponse(result, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method."}, status=400)


@csrf_exempt
def fetch_credential(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            issuanceId = data.get("issuanceId")
            if not issuanceId:
                return JsonResponse({"error": "issuanceId is required"}, status=400)

            result = get_credentials(issuanceId)
            return JsonResponse(result, safe=False, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
    return JsonResponse({"error": "Invalid request method."}, status=400)


@csrf_exempt
def revoke_credential(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            credential_id_to_find = data.get("credentialId")
            revocation_reason = data.get("revocationReason")

            # --- Validation  ---
            if not credential_id_to_find:
                return JsonResponse({"error": "credentialId is required"}, status=400)
            if not revocation_reason:
                return JsonResponse(
                    {"error": "revocationReason is required"}, status=400
                )

            # --- Fetch issuance records ---
            try:
                # Assuming listIssuanceDataRecords handles potential API errors and returns data or raises an exception
                issuance_response = listIssuanceDataRecords()
                logger.debug(
                    f"Raw response from listIssuanceDataRecords: {issuance_response}"
                )
            except Exception as e:
                logger.error(
                    f"Error calling listIssuanceDataRecords: {e}", exc_info=True
                )
                return JsonResponse(
                    {"error": "Failed to fetch issuance records from Affinidi service"},
                    status=500,
                )

            # --- Check response structure and extract flowData ---
            if (
                not isinstance(issuance_response, dict)
                or "flowData" not in issuance_response
                or not isinstance(issuance_response["flowData"], list)
            ):
                logger.error(
                    f"Unexpected structure or missing flowData in list_issuance_data_records response: {issuance_response}"
                )
                return JsonResponse(
                    {"error": "Unexpected response format from Affinidi service"},
                    status=500,
                )

            records_to_search = issuance_response["flowData"]
            logger.debug(
                f"Searching within flowData array. Count: {len(records_to_search)}"
            )

            # --- Find the matching record  ---
            matching_record = None
            for record in records_to_search:
                if (
                    isinstance(record, dict)
                    and record.get("flowId") == credential_id_to_find
                ):
                    matching_record = record
                    break

            if not matching_record:
                logger.warning(
                    f"Issuance record not found for credentialId (flowId): {credential_id_to_find} within the flowData. Searched count: {len(records_to_search)}"
                )
                return JsonResponse({"error": "Credential ID not found"}, status=404)

            if "id" not in matching_record:
                logger.error(
                    f'Matching issuance record is missing the "id" field: {matching_record}'
                )
                return JsonResponse(
                    {"error": "Issuance record format is invalid"}, status=500
                )

            issuance_record_id = matching_record["id"]
            logger.info(
                f"Found issuance record ID: {issuance_record_id} for flowId: {credential_id_to_find}"
            )

            # --- Prepare input for revocation API call  ---
            revoke_credential_input = {
                "issuanceRecordId": issuance_record_id,
                "changeReason": revocation_reason,
            }

            logger.info(f"Revoking credential with input: {revoke_credential_input}")

            # --- Revoke credentials ---
            try:
                # Call the util function to revoke credential
                result = revoke_credential_util(revoke_credential_input)
                logger.info(f"Revocation response: {result}")
            except Exception as e:
                logger.error(f"Error calling revoke_credential: {e}", exc_info=True)
                return JsonResponse(
                    {"error": "Failed to revoke credential via Affinidi service"},
                    status=500,
                )

            # --- Check if revocation failed (aligned with PHP's error check on $result) ---
            if isinstance(result, dict) and "error" in result:
                error_message = result.get("error", "Unknown error")
                logger.error(
                    f"Failed to revoke credential: {error_message}",
                    {"response": result},
                )
                return JsonResponse(
                    {"error": f"Failed to revoke credential: {error_message}"},
                    status=500,
                )

            # --- Return successful response ---
            logger.info(
                f"Credential revoked successfully for issuanceRecordId: {issuance_record_id}"
            )
            return JsonResponse(result, status=200)

        except json.JSONDecodeError:
            logger.error("Invalid JSON format in request body.", exc_info=True)
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}", exc_info=True)
            return JsonResponse(
                {"error": "An internal server error occurred"}, status=500
            )

    return JsonResponse(
        {"error": "Invalid request method. Only POST is allowed."}, status=405
    )  # Use 405 for method not allowed


@csrf_exempt
def verify_credential(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            verifiable_credentials = data.get("verifiableCredentials")

            # --- Validation ---
            if not verifiable_credentials:
                return JsonResponse(
                    {"error": "verifiableCredentials is required"}, status=400
                )
            # if not isinstance(verifiable_credentials, list):
            #     return JsonResponse(
            #         {"error": "verifiableCredentials must be an array"}, status=400
            #     )
            credentials_to_verify_payload = {
                "verifiableCredentials": [verifiable_credentials]
            }

            logger.info(f"Verifying credentials: {credentials_to_verify_payload}")

            # --- Call Affinidi service  ---
            verified_response = verify_credential_util(credentials_to_verify_payload)

            logger.info(f"Verification response received: {verified_response}")

            # --- Return successful response (assuming verify_credential_util handles its own errors or raises exceptions) ---
            return JsonResponse(verified_response, status=200)

        except json.JSONDecodeError:
            logger.error("Invalid JSON format in request body.", exc_info=True)
            return JsonResponse({"message": "Invalid JSON format"}, status=400)
        except ValueError as e:  # Catching specific validation errors from your service
            logger.error(f"Validation failed: {e}", exc_info=True)
            return JsonResponse(
                {"message": f"Invalid input provided: {e}"}, status=422
            )  # Aligned with 422
        except Exception as e:
            logger.error(f"Verification failed: {e}", exc_info=True)
            return JsonResponse({"message": f"Verification failed: {e}"}, 500)

    return JsonResponse(
        {"error": "Invalid request method. Only POST is allowed."}, status=405
    )
