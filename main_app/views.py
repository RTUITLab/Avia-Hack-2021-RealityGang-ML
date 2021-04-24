import base64
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .predicting import process_file, make_files


class MakePredictionView(APIView):
    """
    Makes prediction
    """

    def post(self, request):
        in_file = request.FILES['file']
        in_file = in_file.read()
        base64_str = base64.b64encode(in_file).decode('utf-8')

        answers = process_file(base64_str)

        print(answers)
        corrects, incorrects = make_files(base64_str, answers)
        return Response({
            'answers': answers,
            'corrects': corrects,
            'incorrects': incorrects,
        })
