from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
import re

class SecurityHeadersMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        # Cache control for authenticated pages
        if hasattr(request, 'user') and request.user.is_authenticated:
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        
        return response

class InputValidationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Block directory traversal attempts
        suspicious_patterns = [
            r'\.\.',
            r'\/etc\/',
            r'\/proc\/',
            r'\/sys\/',
            r'\\\\',
            r'<script',
            r'javascript:',
            r'vbscript:',
            r'onload=',
            r'onerror=',
        ]
        
        # Check URL path
        for pattern in suspicious_patterns:
            if re.search(pattern, request.path, re.IGNORECASE):
                return HttpResponseForbidden('Forbidden request')
        
        # Check query parameters
        for key, value in request.GET.items():
            for pattern in suspicious_patterns:
                if re.search(pattern, str(value), re.IGNORECASE):
                    return HttpResponseForbidden('Forbidden request')
        
        return None