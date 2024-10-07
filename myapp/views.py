from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Summary 
from .serializers import SummarySerializer
from django.conf import settings
from rest_framework import status
import google.generativeai as genai

model = genai.GenerativeModel('gemini-1.5-flash')

class SummaryView(APIView):
    def post(self, request):
        file = request.FILES.get('file')
        if file:
            file_content = file.read().decode('utf-8')
            prompt = "Please provide Title and summary for the following content without \n" + file_content
            response = model.generate_content(prompt)
            
            a = response.text
            str_ing = " ".join(a.split())
            import pdb ; pdb.set_trace()
            
            data = str_ing.split("## Summary: ")
            t = data[0]
            s = data[1]
            temp = t.split("## Title: ")
            title = " ".join(temp[1].split())
            summary = " ".join(s.split())
            
            Summary.objects.create(title=title, summary=summary)
            serializer = SummarySerializer(Summary.objects.all(), many=True)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        
        return Response({"Error":"Some Error"}, status=status.HTTP_400_BAD_REQUEST)  
    
class SummaryList(APIView):
    def get(self, request):
        summaries = Summary.objects.all()
        if summaries:
            serializer = SummarySerializer(summaries, many=True)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"Error":"Some Error"}, status=status.HTTP_400_BAD_REQUEST)