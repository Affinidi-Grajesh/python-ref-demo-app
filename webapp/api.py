from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .services import build_credentials_request
import os
import jwt
import time
from .util import pst, startIssuance
import affinidi_tdk_credential_issuance_client
from dotenv import load_dotenv

load_dotenv()



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
                return JsonResponse({"error": "Missing credentialTypeId or credentialData"}, status=400)

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

            return JsonResponse({"issuanceId": issuanceId, "status": "Credential fetched successfully"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
    return JsonResponse({"error": "Invalid request method."}, status=400)

@csrf_exempt
def revoke_credential(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            issuanceId = data.get("issuanceId")
            if not issuanceId:
                return JsonResponse({"error": "issuanceId is required"}, status=400)

            # Here you would implement the logic to revoke the credential
            return JsonResponse({"issuanceId": issuanceId, "status": "Credential revoked successfully"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
    return JsonResponse({"error": "Invalid request method."}, status=400)

@csrf_exempt
def verify_credential(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            credentialId = data.get("credentialId")
            if not credentialId:
                return JsonResponse({"error": "credentialId is required"}, status=400)
            return JsonResponse({"credentialId": credentialId, "status": "Credential verified successfully"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
    return JsonResponse({"error": "Invalid request method."}, status=400)

