# 代码生成时间: 2025-10-04 20:35:37
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import binascii
import base64

def generate_key():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key


def sign_data(private_key, data):
    hash = SHA256.new(data)
    signer = pkcs1_15.new(RSA.import_key(private_key))
    signature = signer.sign(hash)
    return base64.b64encode(signature)


def verify_signature(public_key, data, signature):
    try:
        hash = SHA256.new(data)
        verifier = pkcs1_15.new(RSA.import_key(public_key))
        verifier.verify(hash, base64.b64decode(signature))
        return True
    except (ValueError, TypeError):
        return False

class DigitalSignatureToolView(View):
    @method_decorator(csrf_exempt, name='dispatch')
    def dispatch(self, request, *args, **kwargs):
        return super(DigitalSignatureToolView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to generate a digital signature.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            JsonResponse: A JSON response with the generated signature.
        """
        try:
            data = request.POST.get('data')
            private_key, _ = generate_key()
            signature = sign_data(private_key, data.encode())
            return JsonResponse({'signature': signature.decode('utf-8')})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to verify a digital signature.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            JsonResponse: A JSON response indicating whether the signature is valid.
        """
        try:
            data = request.GET.get('data')
            signature = request.GET.get('signature')
            public_key = request.GET.get('public_key')
            isValid = verify_signature(public_key, data, signature)
            return JsonResponse({'is_valid': isValid})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

urlpatterns = [
    path('digital_signature_tool/', DigitalSignatureToolView.as_view(), name='digital_signature_tool')
]