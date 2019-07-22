from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt


################### HOME PAGE#######################################
def index(request):
    pass
    return render(request, 'app_1/index.html')

################### REGISTER NEW USER #######################################
def user_input(request):
    errors = Users.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect ('/')
    else:
        
        hash_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        print(hash_pw)
        new_user = Users.objects.create(first_name=request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = hash_pw)
        request.session['id'] = new_user.id
        return redirect ('/dashboard')

################### USER LOGGING IN #######################################
def user_login(request):
    errors = Users.objects.validate_login(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect ('/')
    else:
        user = Users.objects.filter(email = request.POST['email'])
        person = user[0]
        request.session['id'] = person.id
        return redirect ('/dashboard')

################### LOGGING OUT #######################################
def logout(request):
    request.session.clear()
    return redirect ('/')



######################## MY DASHBOARD #################################
def dashboard(request):
    errors = {}
    if 'id' not in request.session:
        messages.error(request, "you need to log in first!")
        return redirect ('/')
    else:
        this_user = Users.objects.get(id=request.session['id'])
        users_uploads = this_user.trips_uploaded.all()
        all_trips = Trips.objects.all()
        users_trips = this_user.users_trips.all()
        context = {
            "current_user": Users.objects.get(id=request.session['id']),
            "all_trips": all_trips,
            "users_trips": users_trips,
        }
        return render (request, 'app_1/dashboard.html', context)


############################# NEW TRIP PAGE ########################
def new_trip (request):
    context = {
            "current_user": Users.objects.get(id=request.session['id']),
        }
    return render (request, 'app_1/add_trip.html', context)

############################# SUBMITTING NEW TRIP ########################

def submit_new_trip (request):
    errors = Users.objects.validate_trip(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect ('/trips/new')
    else:
        uploader = Users.objects.get(id = request.session['id'])
        Trips.objects.create(destination=request.POST['destination'], start_date = request.POST['start_date'], end_date = request.POST['end_date'], plan = request.POST['plan'], uploaded_by = uploader)
        new_trip = Trips.objects.last()
        new_trip.trips_on.add(uploader)
        uploader.users_trips.add(new_trip)
   
    return redirect('/dashboard')


def delete_trips (request, my_val):
    trip_to_delete = Trips.objects.get(id=my_val)
    trip_to_delete.delete()
    return redirect('/dashboard')


#####################  EDITING TRIP DETAILS ##########################
def edit_trips(request, my_val):
    this_trip = Trips.objects.get(id=my_val)
    context = {
        "this_trip": this_trip,
        "current_user": Users.objects.get(id=request.session['id']),

    }
    return render(request, 'app_1/edit_trip_details.html', context)

############### SUBMITTING TRIP EDITS ####################
def edit_trip_submit (request, my_val):
    this_trip = Trips.objects.get(id=my_val)
    errors = Users.objects.basic_validator2(request.POST)
    #is it necessary to run this part of the if statement in the views.py instead of models so I can pull the 'my_val' data to compare?
    if this_trip.destination == request.POST['destination']:
        pass
    else:
        all_trips = Trips.objects.filter(destination=request.POST['destination'])
        if len(all_trips) >= 1:
            errors['destination_used'] = "This destination already exists!"
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect (f'/trips/edit/{my_val}')
    else:
        if request.method =="POST":
            edit_trip = Trips.objects.get(id=my_val)
            edit_trip.destination = request.POST['destination']
            edit_trip.start_date = request.POST['start_date']
            edit_trip.end_date = request.POST['end_date']
            edit_trip.plan = request.POST['plan']
            edit_trip.save()
            return redirect ('/dashboard')

#####################  LIST OF TRIP DETAILS ##########################
def trip_details (request, my_val):
    trip_details = Trips.objects.get(id = my_val)
  
    context = {
        "current_user": Users.objects.get(id=request.session['id']),
        "trip_details": trip_details,
        "poster": trip_details.uploaded_by.first_name,
        "trip_attendees": trip_details.trips_on.exclude(id = trip_details.uploaded_by.id)
        # "start_date": trip_details.dateReleased(),
        
    }
    return render (request, 'app_1/trip_details.html', context)

######### ADDING A TRIP TO YOUR LIST############
def add_trip (request, my_val):
    adding_trip = Trips.objects.get(id = my_val)
    current_user = Users.objects.get(id=request.session['id'])
    current_user.users_trips.add(adding_trip)
    return redirect ('/dashboard')

############# GIVING UP ON A TRIP ##################
def give_up (request, my_val):
    removing_trip = Trips.objects.get(id=my_val)
    this_user = Users.objects.get(id=request.session['id'])
    this_user.users_trips.remove(removing_trip)
    return redirect ('/dashboard')