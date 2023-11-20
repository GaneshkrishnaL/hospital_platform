# views.py
from django.db.models import Count, Q
from django.shortcuts import render, redirect
from django.contrib.auth import login as django_login
from django.http import HttpResponse
from .models import User, Hospital, Bed, Reservation
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
import hashlib
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import time

# Wait for 10 seconds


import logging

logger = logging.getLogger(__name__)

def home(request):
    return render(request,'hospital_app/home.html')

def logout_view(request):
    # Clear the session data
    request.session.flush()

    # Optionally, add a message to display after logout
    messages.info(request, 'You have been logged out.')

    # Redirect to the login page or home page
    return redirect('login')  # Replace 'login' with the name of your home page's URL if needed



def redirect_to_login(request):
    return redirect('/login/')

def discharge(request,id):
    print(request.method)
    print(id)
    reservation = get_object_or_404(Reservation, id=id)
    hospital=reservation.hospital
    bed=reservation.bed
    print(hospital)
    print(reservation)
    hospital_main= get_object_or_404(Hospital, id=hospital.id)
    print(bed.bed_type)

    if(bed.bed_type=='ICU'):
        bed.status=1
    if(bed.bed_type=='GEN'):
        bed.status=1
    if(bed.bed_type=='PRI'):
        bed.status=1
    bed.save()
    reservation.status='discharged'
    reservation.save()
    #hospital_main.save()
    #reservation.delete()
    return redirect('hospital_dashboard')



def reservation_status(request):
    user_id = request.session.get('user_id')
    user_type = request.session.get('user_type')

    # Check if user is logged in and is a patient.
    if not user_id or user_type != 'patient':
        messages.error(request, 'You must be logged in as a patient to view reservation status.')
        return redirect('login')

    # Fetch reservations and include the related hospital, bed, and user data.
    reservations = Reservation.objects.filter(user_id=user_id).select_related('hospital', 'bed', 'user')
    return render(request, 'hospital_app/reservation_status.html', {'reservations': reservations})


@csrf_exempt
def login_view(request):

    #logger.debug("This is a debug message")
    if request.method == "POST":
        email = request.POST['email']
        hashed_password = hashlib.sha256(request.POST['password'].encode()).hexdigest()
        user_type = request.POST['user_type']

        # Check user type
        if user_type == "patient":
            try:
                user = User.objects.get(email=email)


                if hashed_password == user.password:
                    # Use Django's built-in session handling
                    request.session.flush()
                    request.session['user_id'] = user.id
                    request.session['user_type'] = 'patient'
                    # Redirect to patient dashboard or some other page
                    return redirect('dashboard')
                else:
                    # Password is incorrect
                    messages.error(request, 'Invalid password')
                    return redirect('login')
            except User.DoesNotExist:
                # User does not exist
                messages.error(request, 'User doesnt exist')
                return redirect('login')
        
        # Add logic for Hospital later when you implement it

        if user_type == "hospital":
            try:
                hospital = Hospital.objects.get(email=email)
                if hashed_password == hospital.password:
                    # Use Django's built-in session handling
                    request.session.flush()
                    request.session['hospital_id'] = hospital.id

                    request.session['user_type'] = 'hospital'
                    # Redirect to hospital dashboard or some other page
                    return redirect('hospital_dashboard')
                else:
                    # Password is incorrect
                    messages.error(request, 'Invalid password')
                    return redirect('login')
            except Hospital.DoesNotExist:
                # Hospital does not exist
                messages.error(request, 'Hospital doesnt exist')
                return redirect('login')

    return render(request, 'hospital_app/login.html')

def registration(request):
    return render(request, 'hospital_app/register.html')


@csrf_exempt
def register_view(request):
    print(request.method)
    if request.method == "POST":
        user_type = request.POST['user_type']
        email = request.POST['email']

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Invalid email address.')
            return redirect('register')

        # Check if email already exists
        if User.objects.filter(email=email).exists() or Hospital.objects.filter(email=email).exists():
            messages.error(request, 'Email already in use. Please choose a different email.')
            return redirect('register')

        if user_type == "patient":
            name = request.POST['name']
            email = request.POST['email']
            phone = request.POST['phone']
            age = request.POST['age']
            gender = request.POST['gender']
            address = request.POST['address']
            bloodGroup = request.POST['bloodGroup']
            password = hashlib.sha256(request.POST['password'].encode()).hexdigest()

            print("registered password", request.POST['password'])
            # print("hashed password", password)
            # Create a new user instance and save to the database
            User.objects.create(
                name=name,
                email=email,
                phone=phone,
                age=age,
                gender=gender,
                address=address,
                bloodGroup=bloodGroup,
                password=password
            )

            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')
        
        if user_type == "hospital":
            hospitalName = request.POST['hospitalName']
            email = request.POST['email']
            phone = request.POST['hospital_phone']
            location = request.POST['location']
            area = request.POST['area']
            password = hashlib.sha256(request.POST['password'].encode()).hexdigest()

            # Create a new hospital instance and save to the database
            hospital = Hospital.objects.create(
                hospitalName=hospitalName,
                email=email,
                phone=phone,
                location=location,
                area=area,
                password=password
            )

            gen_beds_to_create = int(request.POST['gen_beds'])
            icu_beds_to_create = int(request.POST['icu_beds'])
            pri_beds_to_create = int(request.POST['pri_beds'])

            

            for _ in range(gen_beds_to_create):
                Bed.objects.create(
                    hospital=hospital,
                    bed_type='GEN'  # Assume 'GEN' is the code for General beds
                )

            for _ in range(icu_beds_to_create):
                Bed.objects.create(
                    hospital=hospital,
                    bed_type='ICU'  # Assume 'GEN' is the code for General beds
                )
            for _ in range(pri_beds_to_create):
                Bed.objects.create(
                    hospital=hospital,
                    bed_type='PRI'  # Assume 'GEN' is the code for General beds
                )

            messages.success(request, 'Hospital registration successful. Please log in.')
            return redirect('login')

    return render(request, 'hospital_app/register.html')



# def dashboard_view(request):
#     # Existing code...
#     hospitals_data = []
#     for hospital in hospitals:
#         hospital_data = {
#             'hospital': hospital,
#             'available_icu_beds': hospital.available_beds_by_type('ICU'),
#             'available_gen_beds': hospital.available_beds_by_type('GEN'),
#             'available_pri_beds': hospital.available_beds_by_type('PRI'),
#         }
#         hospitals_data.append(hospital_data)

#     return render(request, 'hospital_app/dashboard.html', {'hospitals': hospitals_data})



def dashboard_view(request):
    user_id = request.session.get('user_id')
    user_type = request.session.get('user_type')
    
    # Check if the user is logged in and is a patient.
    if not user_id or user_type != 'patient':
        messages.error(request, 'Only patients can access the dashboard.')
        return redirect('login')  # Replace 'login' with your login view's name

    # If the user is logged in as a patient, proceed to display the dashboard.
    hospitals_data = []
    hospitals = Hospital.objects.all()
    for hospital in hospitals:
        hospital_data = {
            'hospital': hospital,
            'available_icu_beds': hospital.available_beds_by_type('ICU'),
            'available_gen_beds': hospital.available_beds_by_type('GEN'),
            'available_pri_beds': hospital.available_beds_by_type('PRI'),
        }
        hospitals_data.append(hospital_data)
    return render(request, 'hospital_app/dashboard.html', {'hospitals': hospitals_data})


@csrf_exempt

def make_reservation(request):
    if request.method == 'POST':
        hospital_id = request.POST.get('hospital_id')
        hospital = get_object_or_404(Hospital, id=hospital_id)
        

        # Retrieve user_id from the session
        user_id = request.session.get('user_id')
        
        # If there's no user_id in the session, redirect to login
        if not user_id:
            messages.error(request, 'You must be logged in to make a reservation.')
            return redirect('login')  # Replace 'login' with your login view's name

        # Get the user from the User model
        user = get_object_or_404(User, id=user_id)
        

        existing_reservations = Reservation.objects.filter(
            user_id=user_id, 
            status__in=['pending', 'confirmed']
        )
        if existing_reservations.exists():
            
            messages.error(request, 'You already have a pending or confirmed reservation.')

            return redirect('reservation_status')
            
            

        # Check if the user is a patient
        if request.session.get('user_type') == 'patient':
            # Get the first available bed for the given hospital
            bed_type = request.POST.get('bed_type')
            available_bed = hospital.beds.filter(bed_type=bed_type, status=1).first()

            if available_bed:
                # Update the bed's status to 'Occupied'
                available_bed.status = 2  # Assuming '2' is the status code for 'Occupied'
                available_bed.save()

                # Create the reservation with the available bed
                reservation = Reservation(user=user, hospital=hospital, bed=available_bed, status='pending')
                reservation.save()

                # Redirect to the dashboard with a success message
                messages.success(request, 'Reservation made successfully!')
                return redirect('reservation_status')

            else:
                # Redirect to the dashboard with an error message
                messages.error(request, 'No beds available in this hospital.')
                return redirect('dashboard')
        else:
            messages.error(request, 'You are not authorized to make a reservation.')
            return redirect('dashboard')

    # If not a POST request or any other issue, redirect to the dashboard
    return redirect('dashboard')






def hospital_dashboard(request):
    if 'hospital_id' not in request.session:
        return redirect('login')

    hospital_id = request.session['hospital_id']
    hospital = get_object_or_404(Hospital, id=hospital_id)

    # Helper function to get bed counts by type and status
    def get_bed_counts(bed_type):
        return {
            'total': hospital.beds.filter(bed_type=bed_type).count(),
            'occupied': hospital.beds.filter(bed_type=bed_type, status=2).count(),
            'available': hospital.beds.filter(bed_type=bed_type, status=1).count(),
        }

    # Fetch bed counts for each type
    icu_beds = get_bed_counts('ICU')
    general_beds = get_bed_counts('GEN')
    private_beds = get_bed_counts('PRI')

    pending_reservations = hospital.reservation_set.filter(status='pending')

    confirmed_reservations = hospital.reservation_set.filter(status='confirmed')

    context = {
        'hospital': hospital,
        'icu_beds': icu_beds,
        'general_beds': general_beds,
        'private_beds': private_beds,
        'pending_reservations': pending_reservations,
        'confirmed_reservations': confirmed_reservations,
    }

    return render(request, 'hospital_app/hospital_dashboard.html', context)





def update_reservation(request, reservation_id, action):
    if 'hospital_id' not in request.session:
        return redirect('login')

    reservation = get_object_or_404(Reservation, id=reservation_id)
    if action == 'confirm':
        reservation.status = 'confirmed'
        reservation.bed.status = 2  # Update bed status to 'Occupied'
    elif action == 'cancel':
        reservation.status = 'cancelled'
        reservation.bed.status = 1  # Update bed status to 'Available'
    reservation.save()
    reservation.bed.save()
    
    return redirect('hospital_dashboard')



def Add_Bed(request):
    bed=request.GET['Bed']
    num=request.GET['num']
    hospital_id = request.session['hospital_id']
    hospital = get_object_or_404(Hospital, id=hospital_id)
    for _ in range(int(num)):
        Bed.objects.create(hospital=hospital,bed_type=bed)
    
    return redirect('hospital_dashboard')
def Add_Update(request,hospital):
    print(hospital)
    context={'hospital':hospital}
    return render(request,'hospital_app/add_update.html',context)