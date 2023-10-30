from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .integrator_serializers import IntegrationRequestSerializer, IntegrationRequestResponse


def IntegratorFactory(Source):

  @api_view(['POST'])
  def integrationView(request):
      # TODO: Increment 'request-start' metric for tag:source

    request_serializer = IntegrationRequestSerializer(data=request.data)
    if not request_serializer.is_valid():
        # TODO: Increment 'request-validation' error metric for tag:source
        return Response({'errors': request_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    source = Source()

    try:
      auth = source.authenticate(request.data.get('username'), request.data.get('password'))

      if auth == None:
        raise Exception('Unable to authenticate user.')
    except Exception as e:
      print(e)
      # TODO: Increment 'authentication' error metric for tag:source
      return Response({'message': 'Authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
      fetched = source.fetch(auth, request.data.get('start_date'), request.data.get('end_date'))

      if fetched == None:
        raise Exception('There was a problem fetching the data.')
    except Exception as e:
      print(e)
      # TODO: Increment 'request' error metric for tag:source
      return Response({'message': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)

    try:
      response = source.parse(fetched)

      if response == None:
        raise Exception('There was a problem parsing the data.')
    except Exception as e:
      print(e)
      # TODO: Increment 'parse' error metric for tag:source
      return Response({'message': 'Internal serverl error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    response_serializer = IntegrationRequestResponse(data=response)
    if not response_serializer.is_valid():
      print(response_serializer.errors)
      # TODO: Increment 'response-validation' error metric for tag:source
      return Response({'message': 'Internal serverl error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # TODO: Increment 'success-response' metric for tag:source
    return Response(response)

  return integrationView