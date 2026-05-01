from .forms import RegisterForm
from django.shortcuts import render, redirect

# Create your views here.

def home(request):
    return render(request, 'home.html')


def register(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')

    return render(request, 'register.html', {'form': form})

from .models import Internship

def internships(request):
    data = Internship.objects.all()

    profile = None
    if request.user.is_authenticated:
        profile = StudentProfile.objects.filter(user=request.user).first()

    applied_ids = []
    if request.user.is_authenticated:
        applied_ids = Application.objects.filter(student=request.user).values_list('internship_id', flat=True)

    internship_list = []

    for i in data:
        match = 0

        if profile:
            student_skills = [s.strip().lower() for s in profile.skills.split(',')]
            required_skills = [s.strip().lower() for s in i.required_skills.split(',')]

            matched = set(student_skills) & set(required_skills)

            if len(required_skills) > 0:
                match = int((len(matched) / len(required_skills)) * 100)

        internship_list.append({
            'obj': i,
            'match': match
        })

    return render(request, 'internships.html', {
        'internships': internship_list,
        'applied_ids': applied_ids
    })

from .models import StudentProfile
from .forms import StudentProfileForm
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    profile, created = StudentProfile.objects.get_or_create(user=request.user)

    form = StudentProfileForm(instance=profile)

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')

    return render(request, 'profile.html', {'form': form})

from .models import Application

@login_required
def apply_internship(request, id):
    internship = Internship.objects.get(id=id)

    profile = StudentProfile.objects.filter(user=request.user).first()

    # Check if profile exists and required fields filled
    if not profile or not profile.phone or not profile.college or not profile.education or not profile.skills or not profile.resume:
        return redirect('profile')  # force user to fill profile

    already_applied = Application.objects.filter(
        student=request.user,
        internship=internship
    ).exists()

    if not already_applied:
        Application.objects.create(
            student=request.user,
            internship=internship
        )

    return redirect('internships')

@login_required
def my_applications(request):
    apps = Application.objects.filter(student=request.user)
    return render(request, 'my_applications.html', {'applications': apps})