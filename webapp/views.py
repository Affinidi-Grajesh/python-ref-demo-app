from django.shortcuts import render
import os

import dotenv
dotenv.load_dotenv()

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
