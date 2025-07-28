from django.urls import path
from . import views
from . import api

urlpatterns = [
    path("", views.home, name="home"),
    path("cis/", views.cis, name="cis"),
    path("iota/", views.iota, name="iota"),
    path("revoke/", views.revoke, name="revoke"),
    path("verify/", views.verify, name="verify"),
    path("idv/", views.idv, name="idv"),
    path("api/hello/", api.api_hello, name="api_hello"),
    path("api/issue-credential", api.issue_credential, name="issue_credential"),
    path("api/fetch-credential", api.fetch_credential, name="fetch_credential"),
    path("api/revoke-credential", api.revoke_credential, name="revoke_credential"),
    path("api/verify-credential", api.verify_credential, name="verify_credential"),
    path("api/iota-start", api.iota_start, name="iota_start"),
    path("api/iota-complete", api.iota_complete, name="iota_complete"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("callback", views.callback, name="callback"),
    path("dashboard", views.dashboard, name="dashboard"),
]
