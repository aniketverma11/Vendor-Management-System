from django.urls import path

from vendormanagement.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
)

from rest_framework_simplejwt.views import TokenBlacklistView

from vendormanagement.users.api.v1.views import (
    LoginViewSet,
    CreateProfileViewSet,
    RefreshTokenView,
)


app_name = "users"
urlpatterns = [
    path(
        "login/",
        LoginViewSet.as_view(
            {
                "post": "create",
            }
        ),
    ),
    path("refresh/", RefreshTokenView.as_view(), name="token_refresh"),
    path("logout/", TokenBlacklistView.as_view(), name="token_blacklist"),
    path(
        "signup/",
        CreateProfileViewSet.as_view(
            {
                "post": "create",
            }
        ),
    ),
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
