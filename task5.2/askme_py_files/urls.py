"""askme_py_files URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from askme import views

from askme_py_files import settings

urlpatterns = [
    path('', views.index, name="index"),
    path('admin/', admin.site.urls),
    path('question/<int:question_id>', views.question, name="question"),
    path('ask/', views.ask, name="ask"),
    path('login/', views.login, name="login"),
    path('tag/<str:tag_name>', views.tag, name="tag"),
    path('signup/', views.signup, name="signup"),
    path('user/', views.user, name="user"),
    path('base/', views.base, name="base"),
    path('hot/', views.hot, name="hot"),
    path('logout/', views.logout, name='logout'),
    path('vote_question/', views.vote_question, name='vote_question'),
    path('vote_answer/', views.vote_answer, name='vote_answer'),
    path('vote_correct/', views.vote_correct, name='vote_answer'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)