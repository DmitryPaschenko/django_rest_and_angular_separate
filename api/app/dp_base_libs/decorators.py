import sys
from rest_framework.response import Response
from rest_framework import status


def exception_to_response(catch_exception, status_code=status.HTTP_400_BAD_REQUEST):
    def wrap(func):
        def wrapped(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception, ex:
                return Response({"detail": ex.message}, status=status_code)
        return wrapped
    return wrap