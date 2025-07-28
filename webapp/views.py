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
    avvanz_query_id_idv = os.environ.get("IOTA_AVVANZ_CREDENTIAL_QUERY_IDV", "")
    response_code = request.GET.get("response_code", "")

    return render(
        request,
        "webapp/idv.html",
        {
            "config_id_idv": config_id_idv,
            "avvanz_query_id_idv": avvanz_query_id_idv,
            "response_code": response_code,
        },
    )


def iota(request):
    config_id = os.environ.get("IOTA_CONFIG_ID", "")
    avvanz_query_id = os.environ.get("IOTA_AVVANZ_CREDENTIAL_QUERY", "")
    response_code = request.GET.get("response_code", "")

    return render(
        request,
        "webapp/iota.html",
        {
            "config_id": config_id,
            "avvanz_query_id": avvanz_query_id,
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
