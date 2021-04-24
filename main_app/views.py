from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .predicting import process_file


class MakePredictionView(APIView):
    """
    Makes prediction
    """

    def post(self, request):
        answers = process_file(request.FILES['file'])
        print(answers)
        # answers = process_file(file.file)
        return Response()
