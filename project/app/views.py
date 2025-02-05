from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import DonorRegister, Stafreg
import re
from .models import *
from django.contrib.auth.decorators import login_required


def get_staf(request):
    """Retrieve the logged-in staff object from the session."""
    if 'staf' not in request.session:
        return None  # No staff logged in

    try:
        return Stafreg.objects.get(email=request.session['staf'])
    except Stafreg.DoesNotExist:
        return None
    
def get_donor(request):
    """Retrieve the logged-in staff object from the session."""
    if 'donor' not in request.session:
        return None  # No staff logged in

    try:
        return DonorRegister.objects.get(email=request.session['donor'])
    except DonorRegister.DoesNotExist:
        return None


def donor_register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        location = request.POST['location']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('donor_register')

        # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messages.error(request, "Invalid email format!")
            return redirect('donor_register')

        # Check if email already exists
        if DonorRegister.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('donor_register')

        # Save donor
        donor = DonorRegister(name=name, email=email, phone=phone, location=location, password=password , confirm_password=confirm_password)
        donor.save()
        messages.success(request, "Registration successful! Please log in.")
        return redirect('login')

    return render(request, 'donor/donor_register.html')


def staff_register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        location = request.POST['location']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('staff_register')

        if Stafreg.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('staff_register')

        staff = Stafreg(name=name, email=email, phone=phone, location=location, password=password ,confirm_password=confirm_password)
        staff.save()
        messages.success(request, "Staff registered successfully!")
        return redirect('login')

    return render(request, 'staf/staff_register.html')


def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Check if user is a donor
        try:
            donor = DonorRegister.objects.get(email=email, password=password)
            request.session['donor'] = donor.email
            return redirect('donorhome')
        except DonorRegister.DoesNotExist:
            pass

        # Check if user is a staff member
        try:
            staf = Stafreg.objects.get(email=email, password=password)
            request.session['staf'] = staf.email
            return redirect('staff_home')
        except Stafreg.DoesNotExist:
            pass

        # Check if user is an admin (superuser)
        user = authenticate(request, username=email, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            request.session['admin'] = email
            return redirect('admin_home')

        messages.error(request, "Invalid login credentials!")
        return redirect('login')

    return render(request, 'login.html')


def user_logout(request):
    if 'donor' in request.session:
        del request.session['donor']
    if 'staf' in request.session:
        del request.session['staf']
    if 'admin' in request.session:
        logout(request)
        del request.session['admin']

    return redirect('login')

def donor_home(request):
    return render(request, 'donor/donorhome.html')

def staff_home(request):
    return render(request, 'staf/stafhome.html')

def admin_home(request):
    return render(request, 'admin/adminhome.html')

def addchild(request):
    staf_user = get_staf(request)
    if not staf_user:
        messages.error(request, "You must be logged in as staff to add a child.")
        return redirect('staff_login')  # Redirect to staff login if not logged in

    if request.method == 'POST':
        name = request.POST['name']
        age = request.POST['age']
        gender = request.POST['gender']
        medical_history = request.POST['medical_history']
        education_status = request.POST['education_status']
        admission_date = request.POST['admission_date']
        guardian_name = request.POST.get('guardian_name', '')
        guardian_contact = request.POST.get('guardian_contact', '')

        # Create child entry linked to staff
        Child.objects.create(
            name=name,
            age=age,
            gender=gender,
            medical_history=medical_history,
            education_status=education_status,
            admission_date=admission_date,
            guardian_name=guardian_name,
            guardian_contact=guardian_contact,
            staf=staf_user  # 🔹 Link child to logged-in staff
        )

        messages.success(request, "Child added successfully!")
        return redirect('viewchild')

    return render(request, 'staf/addchild.html')


def viewchild(request):
    staf_user = get_staf(request)
    if not staf_user:
        messages.error(request, "You must be logged in as staff to view children.")
        return redirect('staff_login')

    # Filter children only added by the logged-in staff
    children = Child.objects.filter(staf=staf_user)

    return render(request, 'staf/viewchild.html', {'children': children})



def editchild(request,id):
    child = Child.objects.get(pk=id)

    if request.method == 'POST':
        child.name = request.POST['name']
        child.age = request.POST['age']
        child.gender = request.POST['gender']
        child.medical_history = request.POST['medical_history']
        child.education_status = request.POST['education_status']
        child.admission_date = request.POST['admission_date']
        child.guardian_name = request.POST['guardian_name']
        child.guardian_contact = request.POST['guardian_contact']
        child.save()
        return redirect('viewchild')

    return render(request, 'staf/editchild.html', {'child': child})

def deletechild(request,id):
    child = Child.objects.get(pk=id)
    child.delete()
    return redirect('viewchild')


def stafprofile(request):
    staf_email = request.session.get('staf')
    
    if staf_email:
        staff = Stafreg.objects.get(email=staf_email)
        return render(request, 'staf/stafprofile.html', {'staff': staff})
    else:
        # If no email found in session, redirect to login
        messages.error(request, "Please login to view your profile.")
        return redirect('login')


def updatestafprofile(request):
    staf_email = request.session.get('staf')
    
    if staf_email:
        # Fetch the staff member's profile
        staff = Stafreg.objects.get(email=staf_email)
        
        if request.method == 'POST':
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            location = request.POST.get('location')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            # Check if passwords match
            if password and password != confirm_password:
                messages.error(request, "Passwords do not match!")
                return redirect('updatestafprofile')
            
            # Update the staff member details
            staff.name = name
            staff.phone = phone
            staff.location = location
            if password:
                staff.password = password  # Update password only if provided
            staff.save()

            messages.success(request, "Profile updated successfully!")
            return redirect('stafprofile')
        
        return render(request, 'staf/updatestafprofile.html', {'staff': staff})
    
    else:
        # Redirect to login page if staff is not logged in
        messages.error(request, "Please login to update your profile.")
        return redirect('login')


def donorprofile(request):
    donor_email = request.session.get('donor')
    
    if donor_email:
        donor = DonorRegister.objects.get(email=donor_email)
        return render(request, 'donor/donorprofile.html', {'donor': donor})
    else:
        # If no email found in session, redirect to login
        messages.error(request, "Please login to view your profile.")
        return redirect('login')


def updatedonorprofile(request):
    donor_email = request.session.get('donor')
    
    if donor_email:
        # Fetch the staff member's profile
        donor = DonorRegister.objects.get(email=donor_email)
        
        if request.method == 'POST':
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            location = request.POST.get('location')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            # Check if passwords match
            if password and password != confirm_password:
                messages.error(request, "Passwords do not match!")
                return redirect('updatedonorprofile')
            
            # Update the staff member details
            donor.name = name
            donor.phone = phone
            donor.location = location
            if password:
                donor.password = password  # Update password only if provided
            donor.save()

            messages.success(request, "Profile updated successfully!")
            return redirect('donorprofile')
        
        return render(request, 'donor/updatedonorprofile.html', {'donor': donor})
    
    else:
        # Redirect to login page if staff is not logged in
        messages.error(request, "Please login to update your profile.")
        return redirect('login')


def givedonations(request):
    if request.method == 'POST':
        donor_email = request.session.get('donor')
        donor = DonorRegister.objects.get(email=donor_email)
        amount = request.POST.get('amount')
        donation_type = request.POST.get('donation_type')
        description = request.POST.get('description')

        # Create a donation record
        donation = Donation(
            donor=donor,
            amount=amount,
            donation_type=donation_type,
            description=description
        )
        donation.save()

        messages.success(request, "Donation made successfully!")
        return redirect('listofdonations')

    return render(request, 'donor/givedonations.html')



def listofdonations(request):
    donor_email = request.session.get('donor')
    donor = DonorRegister.objects.get(email=donor_email)
    donations = Donation.objects.filter(donor=donor)

    context = {
        'donations': donations,
    }

    return render(request, 'donor/listofdonations.html', context)

def viewstaffs(request):
    data=Stafreg.objects.all()
    return render(request,'admin/viewstaffs.html',{'data':data})

def viewdonors(request):
    data=DonorRegister.objects.all()
    return render(request,'admin/viewdonors.html',{'data':data})

def viewdonations(request):
    data=Donation.objects.all()
    return render(request,'admin/viewdonations.html',{'data':data})

def viewchildren(request):
    data=Child.objects.all()
    return render(request,'admin/viewchildren.html',{'data':data})

def about(request):
    return render(request,'donor/about.html')






