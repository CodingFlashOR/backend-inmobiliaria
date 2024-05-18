from rest_framework import serializers
from apps.emails.utils import decode_b64
import base64


class AccountActivationDataSerializer(serializers.Serializer):
    """
    Serializer that handles the data for the account activation view.
    """

    user_uuidb64 = serializers.CharField(max_length=100, required=True)
    token = serializers.CharField(max_length=100, required=True)

    @staticmethod
    def _is_base64(s: str) -> bool:
        """
        Check if the provided string is a valid base64 string.
        """

        try:
            return base64.b64encode(base64.b64decode(s)).decode() == s
        except Exception:

            return False

    def validate_user_uuidb64(self, value: str) -> str:
        if not self._is_base64(s=value):
            raise serializers.ValidationError(
                code="invalid_data", message="Invalid user uuidb64."
            )

        return decode_b64(s=value)
