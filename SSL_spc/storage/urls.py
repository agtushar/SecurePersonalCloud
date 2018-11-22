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
    path('keyVerify/', csrf_exempt(views.keyVerify), name='keyVerify'),
    path('begin/', csrf_exempt(views.begin), name='begin'),
    path('end/', csrf_exempt(views.end), name='end'),
    path('lockfree/', csrf_exempt(views.lockfree), name='lockfree'),
    path('files/', csrf_exempt(views.display), name='display'),

]
