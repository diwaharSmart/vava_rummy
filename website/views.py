from django.shortcuts import render
from website.models import Page
from rest_framework.views import APIView
from rest_framework.response import Response
from website.models import Api
from rest_framework import status

# Create your views here.
def get_page(key):
    return Page.objects.get(key=key)

def index(request):
    data         = dict()
    try:
        data["page"] = get_page("index")
    except:
        data["page"] = get_page("404")
    return render(
        request,
        template_name="website/page.html",
        context=data
    )

def PageView(request,key):
    data         = dict()
    try:
        if key == None:
            data["page"] = get_page("index")
        else:
            data["page"] = get_page(key)
    except:
        data["page"] = get_page("404")
    return render(
        request,
        template_name="website/page.html",
        context=data
    )


class ApiRequest(APIView):
    def get(self, request, format=None):
        response_data = {}
        api_key = request.query_params.get("api_key", None)

        try:
            api = Api.objects.get(key=api_key)
        except Api.DoesNotExist:
            return Response({"error": "Invalid API key"}, status=status.HTTP_400_BAD_REQUEST)

        # Pass connected JsonSerializer content to exec block
        for json_serializer in api.serializers.all():
            try:
                exec(json_serializer.content, globals(), locals())
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            exec(api.content, globals(), locals())  # Execute the API content
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        status_code = response_data.pop('status_code', 200)  # Default to 200 if status_code is not provided
        return Response(response_data, status=status_code)



