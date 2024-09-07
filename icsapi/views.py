from django.shortcuts import render
from rest_framework import generics, permissions
from django.http import HttpResponse
from rest_framework.views import APIView
from .serializers import TimetableSerializer
import json
from icalendar import Calendar, Event
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Course, Timetable, Module
 

 
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import permissions
from icalendar import Calendar, Event
from datetime import timedelta
from .models import Timetable, Module
from .serializers import TimetableSerializer

class TimetableICSView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, timetable_name, format=None):
        cal = Calendar()
        # Hole alle Timetables für das angegebene Semester
        timetables = Timetable.objects.filter(name=timetable_name)
        
        for timetable in timetables:
            modules = Module.objects.filter(timetable=timetable)
            for module in modules:
                response=get_Module(module,cal)
                if type(response) is HttpResponse:
                    return response
        
        response = HttpResponse(cal.to_ical(), content_type='text/calendar')
        response['Content-Disposition'] = 'attachment; filename="timetable.ics"'
        return response

def get_datetime(day, block):
    # Liste der Startzeiten für die Blöcke

    block_start_times = [
        datetime(2024, 1, 1, 8, 0),   # Block 1
        datetime(2024, 1, 1, 9, 45),  # Block 2
        datetime(2024, 1, 1, 11, 30), # Block 3
        datetime(2024, 1, 1, 13, 45), # Block 4
        datetime(2024, 1, 1, 15, 30), # Block 5
        datetime(2024, 1, 1, 17, 15), # Block 6
        datetime(2024, 1, 1, 19, 0)   # Block 7
    ]
    
    # Berechne das Startdatum für den angegebenen Tag und Block
    start_time = block_start_times[block - 1] + timedelta(days=day - 1)
    return start_time


def get_Module(module,calendar):
    event_data = {
                'tag': module.tag,
                'name': module.name,
                'longname': module.longname,
                'dozent': module.dozent,
                'raum': module.raum,
                'startBlock': module.startBlock,
                'endBlock': module.endBlock,
                'notes': module.notes,
            }
    serializer = TimetableSerializer(data=event_data)
    if serializer.is_valid():
        event_data = serializer.validated_data
        ical_event = Event()
        ical_event.add('summary', event_data['name'])
        ical_event.add('dtstart', get_datetime(event_data['tag'], event_data['startBlock']))
        ical_event.add('dtend', get_datetime(event_data['tag'], event_data['endBlock']) + timedelta(minutes=90))
        ical_event.add('location', event_data['raum'])
        
        description = event_data['dozent'] + "\n"
        if 'notes' in event_data:
            description += event_data['notes'] + "\n"
        if 'longname' in event_data:
            description += event_data['longname'] + "\n"
        ical_event.add('description', description)
        calendar.add_component(ical_event)
    else:
        return HttpResponse(serializer.errors, status=400)

class TimetableUpdateView(APIView):
    def post(self,request):
        try:
            data = json.loads(request.body)
            # Lösche alle Daten aus der Datenbank
            Module.objects.all().delete()
            Timetable.objects.all().delete()
            Course.objects.all().delete()

            # Verarbeite das JSON-File
            for course_name in data:
                course=Course.objects.create(name=course_name)
                for timetable_name in data[course_name]:
                    timetable = Timetable.objects.create(name=timetable_name, course=course)

                    for module_data in data[course_name][timetable_name]:
                        Module.objects.create(
                            tag=module_data.get('tag', 0),
                            name=module_data.get('name', ''),
                            longname=module_data.get('longname', ''),
                            dozent=module_data.get('dozent', ''),
                            raum=module_data.get('raum', ''),
                            startBlock=module_data.get('startBlock', 1),
                            endBlock=module_data.get('endBlock', 1),
                            notes=module_data.get('notes', ''),
                            timetable=timetable
                        )

            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        
class ModuleIcsView(APIView):

    permission_classes = [permissions.AllowAny]
    def get(self,request,module_names, format=None):
        cal = Calendar()
        # Hole alle Timetables für das angegebene Semester
        modules=module_names.split('+')
        for module_name in modules:
            module=Module.objects.filter(name=module_name)
            print(module_name)
            response=get_Module(module[0],cal)
            if type(response) is HttpResponse:
                return response
        response = HttpResponse(cal.to_ical(), content_type='text/calendar')
        response['Content-Disposition'] = 'attachment; filename="timetable.ics"'
        return response

class ModuleListView(APIView):
    permission_classes=[permissions.AllowAny]
    def get(self,request, timetable_name):
        timetable=Timetable.objects.filter(name=timetable_name)[0]
        modules=Module.objects.filter(timetable=timetable)
        moduleList=[]
        for module in modules:
            moduleList.append(module.name)
        
        response = HttpResponse(json.dumps(moduleList), content_type="application/json")
        return response

class TimetableListView(APIView):
    permission_classes=[permissions.AllowAny]
    def get(self,request, course_name):
        course=Course.objects.filter(name=course_name)[0]
        timetables=Timetable.objects.filter(course=course)
        timetableList=[]
        for timetable in timetables:
            timetableList.append(timetable.name)
        
        response = HttpResponse(json.dumps(timetableList), content_type="application/json")
        return response

class CourseListView(APIView):
    permission_classes=[permissions.AllowAny]
    def get(self,request):
        
        courses=Course.objects.all()
        courseList=[]
        for course in courses:
            courseList.append(course.name)
        
        response = HttpResponse(json.dumps(courseList), content_type="application/json")
        return response

from rest_framework import viewsets
from .models import Snippet
from .serializers import SnippetSerializer

class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

