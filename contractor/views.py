"""
Views for the user API
"""

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from contractor.serializers import ContractorSerializer, AuthTokenSerializer


class CreateContractorView(generics.CreateAPIView):
    """Create a new contractor in the system."""

    serializer_class = ContractorSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a auth token for contractor"""

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageContractorView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated contractor."""

    serializer_class = ContractorSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return authenticated contractor."""
        return self.request.user
