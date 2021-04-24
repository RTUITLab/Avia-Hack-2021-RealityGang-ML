import base64
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .predicting import process_file
# from pydantic import BaseModel



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
        # corrects, incorrects = make_files(base64_str.file, answers)

        # print(type(in_file))
        # with open(request.FILES['file'], 'rb') as fd:
        #     data = fd.read()
        #     print(type(data))
        # with open(fn, 'wb') as fd:
        #     fd.write(data)
        # file.read().encode('utf-8')
        # answers = process_file(base64.b64encode(request.FILES['file']))
        # print(answers)
        # answers = process_file(file.file)
        return Response(True)
