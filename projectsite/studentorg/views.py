from typing import Any
from django.db.models.query import QuerySet
from django.db.models import Q
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from studentorg.models import Organization, Student, OrgMember, College, Program
from studentorg.forms import OrganizationForm, StudentForm, OrgMemberForm, CollegeForm, ProgramForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.db import connection
from django.http import JsonResponse

from django.db.models import Count
from datetime import datetime

method_decorator(login_required, name='dispatch')
class HomePageView(ListView):
    model = Organization
    context_object_name = 'home'
    template_name = "home.html"

class OrganizationList(ListView):
    model = Organization
    context_object_name = 'organization'
    template_name = 'org_list.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super(OrganizationList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(name__icontains=query) |
                            Q(description__icontains=query))
        return qs

class OrganizationCreateView(CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_add.html'
    success_url = reverse_lazy('organization-list')

class OrganizationUpdateView(UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_edit.html'
    success_url = reverse_lazy('organization-list')

class OrganizationDeleteView(DeleteView):
    model = Organization
    template_name = 'org_del.html'
    success_url = reverse_lazy('organization-list')

class StudentList(ListView):
    model = Student
    context_object_name = 'student'
    template_name = 'student_list.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super(StudentList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(name__icontains=query) |
                            Q(description__icontains=query))
        return qs

class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'student_add.html'
    success_url = reverse_lazy('student-list')

class StudentUpdateView(UpdateView):
    model =Student
    form_class = StudentForm
    template_name = 'student_edit.html'
    success_url = reverse_lazy('student-list')

class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'student_delete.html'
    success_url = reverse_lazy('student-list')

#OrgMember
class OrgMemberList(ListView):
    model = OrgMember
    context_object_name = 'orgmember'
    template_name = 'orgmember_list.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super(OrgMemberList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(name__icontains=query) |
                            Q(description__icontains=query))
        return qs

class OrgMemberCreateView(CreateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = 'orgmember_add.html'
    success_url = reverse_lazy('orgmember-list')

class OrgMemberUpdateView(UpdateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = 'orgmember_edit.html'
    success_url = reverse_lazy('orgmember-list')

class OrgMemberDeleteView(DeleteView):
    model = Student
    template_name = 'orgmember_delete.html'
    success_url = reverse_lazy('orgmember-list')

#College
class CollegeList(ListView):
    model = College
    context_object_name = 'college'
    template_name = 'college_list.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super(CollegeList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(name__icontains=query) |
                            Q(description__icontains=query))
        return qs

class CollegeCreateView(CreateView):
    model = College
    form_class = CollegeForm
    template_name = 'college_add.html'
    success_url = reverse_lazy('college-list')

class CollegeUpdateView(UpdateView):
    model = College
    form_class = CollegeForm
    template_name = 'college_edit.html'
    success_url = reverse_lazy('college-list')

class CollegeDeleteView(DeleteView):
    model = College
    template_name = 'college_delete.html'
    success_url = reverse_lazy('college-list')

#program
class ProgramList(ListView):
    model = Program
    context_object_name = 'program'
    template_name = 'program_list.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super(ProgramList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(name__icontains=query) |
                            Q(description__icontains=query))
        return qs

class ProgramCreateView(CreateView):
    model = Program
    form_class = ProgramForm
    template_name = 'program_add.html'
    success_url = reverse_lazy('program-list')

class ProgramUpdateView(UpdateView):
    model = Program
    form_class = ProgramForm
    template_name = 'program_edit.html'
    success_url = reverse_lazy('program-list')

class ProgramDeleteView(DeleteView):
    model = Program
    template_name = 'program_delete.html'
    success_url = reverse_lazy('program-list')

class ChartView(ListView):
    template_name = 'chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def get_queryset(self, *args, **kwargs):
        pass

def PieCountStudentsPerProgram(request):
    query = '''
        SELECT p.prog_name, COUNT(s.id) as student_count
        FROM studentorg_student s
        JOIN studentorg_program p ON s.program_id = p.id
        GROUP BY p.prog_name
    '''
    data = {}
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    if rows:
        # Construct the dictionary with program name as keys and count as values
        data = {program: count for program, count in rows}
    else:
        data = {}
    
    return JsonResponse(data)

def LineCountbyMonth(request):
    query = """
        SELECT 
            strftime('%m', date_joined) AS month,
            COUNT(*) AS member_count
        FROM 
            studentorg_orgmember
        WHERE 
            strftime('%Y', date_joined) = strftime('%Y', 'now')
        GROUP BY 
            strftime('%m', date_joined)
        ORDER BY 
            month;
    """
    
    month_names = {
        '01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr', 
        '05': 'May', '06': 'Jun', '07': 'Jul', '08': 'Aug',
        '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'
    }

    result = {name: 0 for name in month_names.values()}
    
    with connection.cursor() as cursor:
        cursor.execute(query)
        for month_num, count in cursor.fetchall():
            result[month_names[month_num]] = count

    return JsonResponse(result)

def HorizontalBarChart(request):
    # Initialize an empty dictionary to store counts for each organization
    result = {}

    # Query the OrgMember model to count the number of students in each organization
    org_members_count = OrgMember.objects.values('organization') \
        .annotate(student_count=Count('student_id'))  # Assuming student_id is related to the student model
    
    # Populate the result dictionary with organization names and corresponding student counts
    for org in org_members_count:
        result[org['organization']] = org['student_count']
    
    # Return the data as JSON response, which can be used to plot a horizontal bar chart
    return JsonResponse(result)


def DoughnutChart(request):
    # Initialize an empty dictionary to store counts for each college
    result = {}

    # Query the Student model and count the number of students in each college
    college_members_count = Student.objects.values('program__college') \
        .annotate(student_count=Count('student_id'))  # Group by college and count students

    # Get the total number of students for percentage calculation
    total_students = Student.objects.count()

    # Populate the result dictionary with college names, student counts, and percentages
    for college in college_members_count:
        college_obj = College.objects.get(id=college['program__college'])
        college_name = college_obj.college_name
        student_count = college['student_count']
        percentage = (student_count / total_students) * 100
        result[college_name] = {
            'student_count': student_count,
            'percentage': round(percentage, 2)
        }

    # Return the data as JSON response, suitable for a doughnut chart
    return JsonResponse(result)

def RankedOrganizationChart(request):
    # Query to get college data with organization count and student count
    query = """
        SELECT 
            c.college_name,
            COUNT(DISTINCT o.id) as organization_count,
            COUNT(DISTINCT s.id) as student_count
        FROM 
            studentorg_college c
        LEFT JOIN 
            studentorg_organization o ON c.id = o.college_id
        LEFT JOIN 
            studentorg_student s ON c.id = s.program_id
        GROUP BY 
            c.college_name
        ORDER BY 
            organization_count DESC
    """
    
    result = {
        'labels': [],
        'datasets': [{
            'label': 'Colleges',
            'data': [],
            'backgroundColor': []
        }]
    }
    
    colors = ["#1d7af3", "#f3545d", "#fdaf4b", "#28a745", "#6f42c1"]
    
    with connection.cursor() as cursor:
        cursor.execute(query)
        for i, (college_name, org_count, student_count) in enumerate(cursor.fetchall()):
            result['labels'].append(college_name)
            result['datasets'][0]['data'].append({
                'x': org_count,
                'y': student_count,
                'r': 10 + (org_count * 2)  # Bubble size based on org count
            })
            result['datasets'][0]['backgroundColor'].append(colors[i % len(colors)])
    
    return JsonResponse(result)