from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def health(request):
    response = {'data': {'status': 'ok'}}
  
    return Response(response)