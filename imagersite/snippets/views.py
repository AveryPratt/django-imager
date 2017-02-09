from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from imager_images.models import Photos
from snippets.serializers import PhotoSerializer


@api_view(['GET', 'POST'])
def image_list(request, format=None):
    """
    List all images, or create a new image.
    """
    if request.method == 'GET':
        images = Photos.objects.all()
        serializer = PhotoSerializer(images, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def image_detail(request, pk, format=None):
    """
    Retrieve, update or delete a image instance.
    """
    try:
        image = Photos.objects.get(pk=pk)
    except Photos.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PhotoSerializer(image)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PhotoSerializer(image, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
