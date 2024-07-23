from django.urls import path
from django.conf import settings

from . import views
from .views import (SignUpView, inscriereView, homeView, verify_uploads, list_students, grade_student,
                    final_grades, toggle_afisare_note, generate_pdf, view_grades)
from django.conf.urls.static import static

urlpatterns = [
    path('', homeView, name="acasa"),
    path('home/', homeView, name="home"),
    path('upload/', inscriereView, name="inscriere"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path('verify_uploads/', verify_uploads, name="verify_uploads"),
    path('list/', list_students, name='list_students'),
    path('final_grades/', final_grades, name='final_grades'),
    path('toggle_afisare_note/', toggle_afisare_note, name='toggle_afisare_note'),
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'),
    path('view_grades/', view_grades, name='view_grades'),
    path('grade_student/<int:student_id>/', grade_student, name='grade_student'),
    path('toggle_afisare_note/', toggle_afisare_note, name='toggle_afisare_note'),
    path('view_grades/', view_grades, name='view_grades'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)