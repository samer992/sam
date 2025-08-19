from django.shortcuts import render
# from rest_framework.decorators import api_view
from tsne3.models import DortTsne3
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
# Create your views here.
@api_view(['GET'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def x(request):
    s = DortTsne3.objects.get(usermanage=request.user.manageid)

