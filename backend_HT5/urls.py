"""backend_HT5 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from django.contrib import admin  # noqa
from django.urls import path  # noqa
from home.views import AddStudent, ShowStudent, UpdateStudent  # noqa

urlpatterns = [
    path('admin/', admin.site.urls),
    path('add/', AddStudent.as_view(), name='page_add_student'),
    path('list/', ShowStudent.as_view(), name='page_list_students'),
    path('list/up/<id>/', UpdateStudent.as_view(), name='page_update_students'),  # noqa
]
