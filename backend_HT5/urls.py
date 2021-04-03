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
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin  # noqa
from django.urls import path, include  # noqa
from rest_framework import routers

from home.views import AddStudent, ShowStudent, UpdateStudent, StudentBook, JsonView, CsvView, MainView, \
    StudentBookUpdate, SubjectList, SubjectUpdate, TeacherUpdate, TeachersList, SendEmailView, SignUpView, \
    ActivateView, SignOutView, SignInView, StudentViewSet, TeacherViewSet, SubjectViewSet, BookViewSet  # noqa
# noqa
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

...

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

router = routers.DefaultRouter()
router.register(r'students', StudentViewSet, basename='students')
router.register(r'teachers', TeacherViewSet, basename='teachers')
router.register(r'subjects', SubjectViewSet, basename='subjects')
router.register(r'books', BookViewSet, basename='books')

urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'), # noqa
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'), # noqa
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'), # noqa

    path('admin/', admin.site.urls),
    path('add/', AddStudent.as_view(), name='page_add_student'),
    path('list/', ShowStudent.as_view(), name='page_list_students'),
    path('list/up/<pk>', UpdateStudent.as_view(), name='page_update_students'),  # noqa
    path('list/books', StudentBook.as_view(), name='page_books_students'),
    path('list/books/up/<id>', StudentBookUpdate.as_view(), name='page_books_update'),  # noqa

    path('email/', SendEmailView.as_view(), name='page_send_email'),

    path('json_view', JsonView.as_view(), name='data_json'),
    path('csv_view', CsvView.as_view(), name='data_csv'),

    path('', MainView.as_view(), name='main_page'),
    path('api/', include(router.urls)),

    path('subject_list/', SubjectList.as_view(), name='page_subject_list'),
    path('subject_list/up/<id>', SubjectUpdate.as_view(), name='page_subject_update'),  # noqa

    path('teacher_list/', TeachersList.as_view(), name='page_teacher_list'),
    path('teacher_list/up/<id>', TeacherUpdate.as_view(), name='page_teacher_update'),  # noqa

    path('signup/', SignUpView.as_view(), name='signup_page'),
    path('activate/<uid>/<token>', ActivateView.as_view(), name='activate_page'),  # noqa
    path('signout/', SignOutView.as_view(), name='signout_page'),
    path('signin/', SignInView.as_view(), name='signin_page'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
