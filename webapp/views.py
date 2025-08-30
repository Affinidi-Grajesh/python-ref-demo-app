from django.shortcuts import render, redirect, reverse
import os
from authlib.integrations.django_client import OAuth
import dotenv
dotenv.load_dotenv()
import json

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

# Create your views here.
def home(request):
    return render(request, "webapp/home.html")

def cis(request):
    return render(request, "webapp/cis.html")

def idv(request):
    config_id_idv = os.environ.get("IOTA_CONFIG_ID_IDV", "")
    query_id_dl = os.environ.get("IOTA_CREDENTIAL_QUERY_IDV_DL", "")
    query_id_passport = os.environ.get("IOTA_CREDENTIAL_QUERY_IDV_PASSPORT", "")
    query_id_anydoc = os.environ.get("IOTA_CREDENTIAL_QUERY_IDV_ANYDOC", "")
    response_code = request.GET.get("response_code", "")

    return render(
        request,
        "webapp/idv.html",
        {
            "config_id_idv": config_id_idv,
            "query_id_dl": query_id_dl,
            "query_id_passport": query_id_passport,
            "query_id_anydoc": query_id_anydoc,
            "response_code": response_code,
        },
    )


def iota(request):
    config_id = os.environ.get("IOTA_CONFIG_ID", "")
    query_id_personalInformation = os.environ.get("IOTA_CREDENTIAL_QUERY_PERSONAL", "")
    query_id_education = os.environ.get("IOTA_CREDENTIAL_QUERY_EDUCATION", "")
    query_id_employment = os.environ.get("IOTA_CREDENTIAL_QUERY_EMPLOYMENT", "")
    query_id_address = os.environ.get("IOTA_CREDENTIAL_QUERY_ADDRESS", "")
    query_id_selective_sharing = os.environ.get(
        "IOTA_CREDENTIAL_QUERY_SELECTIVE_SHARING", ""
    )
    response_code = request.GET.get("response_code", "")

    return render(
        request,
        "webapp/iota.html",
        {
            "config_id": config_id,
            "query_id_personalInformation": query_id_personalInformation,
            "query_id_education": query_id_education,
            "query_id_employment": query_id_employment,
            "query_id_address": query_id_address,
            "query_id_selective_sharing": query_id_selective_sharing,
            "response_code": response_code,
        },
    )


def revoke(request):
    return render(request, "webapp/revoke.html")

def verify(request):
    return render(request, "webapp/verify.html")

def completed(request):
    return render(request, "webapp/completed.html")

def dashboard(request):
    user = request.session.get("user")
    if user:
        if user["custom"] and len(user["custom"][1]) > 0:
            email = user["custom"][1]
        else:
            email = None
    else:
        email = None

    if email is None:
        return render(
            request,
            "webapp/dashboard.html",
            context={
                "session": email,
                "pretty": json.dumps(request.session.get("user"), indent=4),
            },
        )
    else:
        return render(
            request,
            "webapp/dashboard.html",
            context={
                "session": email,
                "pretty": json.dumps(request.session.get("user"), indent=4),
            },
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
