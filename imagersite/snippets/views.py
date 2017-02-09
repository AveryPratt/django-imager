from imager_images.models import Photos
from snippets.serializers import PhotoSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ImageList(APIView):
    """
    List all images, or create a new image.
    """
    def get(self, request, format=None):
        images = Photos.objects.all()
        serializer = PhotoSerializer(images, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageDetail(APIView):
    """
    Retrieve, update or delete a image instance.
    """
    def get_object(self, pk):
        try:
            return Photos.objects.get(pk=pk)
        except Photos.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        image = self.get_object(pk)
        serializer = PhotoSerializer(image)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        image = self.get_object(pk)
        serializer = PhotoSerializer(image, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        image = self.get_object(pk)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'POST'])
# def image_list(request, format=None):
#     """
#     List all images, or create a new image.
#     """
#     if request.method == 'GET':
#         images = Photos.objects.all()
#         serializer = PhotoSerializer(images, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = PhotoSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'PUT', 'DELETE'])
# def image_detail(request, pk, format=None):
#     """
#     Retrieve, update or delete a image instance.
#     """
#     try:
#         image = Photos.objects.get(pk=pk)
#     except Photos.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = PhotoSerializer(image)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = PhotoSerializer(image, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         image.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
