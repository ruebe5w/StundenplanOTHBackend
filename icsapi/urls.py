from django.urls import path
from . import views
from .views import TimetableICSView, TimetableUpdateView, ModuleIcsView, ModuleListView,TimetableListView, CourseListView

urlpatterns = [
    path('timetable/<str:timetable_name>', TimetableICSView.as_view(), name='timetable-ics'),
    path('update', TimetableUpdateView.as_view(),name='update'),
    path('modules/<str:module_names>',ModuleIcsView.as_view(),name='module-ics'),
    path('list/modules/<str:timetable_name>', ModuleListView.as_view(), name='module-list'),
    path('list/timetables/<str:course_name>', TimetableListView.as_view(), name='timetable-list'),
    path('list/courses', CourseListView.as_view(), name='course-list'),
    
]
