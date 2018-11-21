from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('upload/', csrf_exempt(views.upload), name='upload'),
    path('download/', csrf_exempt(views.download), name='download'),
    path('download1/', csrf_exempt(views.download1), name='download1'),
    path('md5s/', csrf_exempt(views.md5s), name='md5s'),
    path('deletefile/', csrf_exempt(views.deletefile), name='deletefile'),
    path('direct_Str/', csrf_exempt(views.direct_Str), name='direct_Str'),
    ]
