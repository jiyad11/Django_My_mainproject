from django.shortcuts import render

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect

from myapp.forms import work_form, WorkerForm, customer_form, schedule_form, bill_form, complaint_form, \
    reply_complaintform
from myapp.models import work_types, schedule, customuser, Bill, card, appointment, complaints


# Create your views here.
def index(request):
    return render(request,'index.html')

def admin_dashboard(request):
    return render(request,'admin_dashboard.html')

#we redirecting using views function name, not htmlname
def add_works(request):
    form = work_form()
    if request.method == 'POST':
        form = work_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_works')
    return render(request,'add_works.html',{'form' : form})

def view_works(request):
    data = work_types.objects.all()
    return render(request,'view_works.html',{'data' : data})

def update_works(request,id):
    data = work_types.objects.get(id=id)
    form = work_form(instance=data)
    if request.method == 'POST':
        form = work_form(request.POST or None , instance=data or None)
        if form.is_valid():
            form.save()
            return redirect('view_works')
    return render(request,'edit_works.html',{'form' : form})

def delete_works(request,id):
    data = work_types.objects.get(id=id)
    form = work_form(instance=data)
    data.delete()
    return redirect('view_works')

def add_worker(request):
    form = WorkerForm()
    if request.method == 'POST':
        form = WorkerForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_worker = True
            user.save()
            messages.info(request,'worker added successful')
            return redirect('view_worker')
    return render(request,'add_worker.html',{'form' : form})

def view_worker(request):
    data = customuser.objects.filter(is_worker=True)
    return render(request,'view_worker.html',{'data' : data})

def update_worker(request,id):
    data = customuser.objects.get(id=id)
    form = WorkerForm(instance=data)
    if request.method == 'POST':
        form = WorkerForm(request.POST or None,request.FILES or None,instance=data)
        if form.is_valid():
            form.save()
            return redirect('view_worker')
    return render(request,'edit_worker.html',{'form' : form})



def delete_worker(request,id):
    # data = CustomUser.objects.get(id=id)
    # form = WorkerForm(instance=data)
    # data.delete()
    # return redirect('worker_view')
    customuser.objects.get(id=id).delete()
    return redirect('view_worker')

def add_customer(request):
    form = customer_form()
    if request.method == 'POST':
        form = customer_form(request.POST,request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_customer = True
            user.save()
            return redirect('view_customer')
    return render(request,'add_customer.html',{'form' : form})

def view_customer(request):
    data = customuser.objects.filter(is_customer=True)
    return render(request,'view_customer.html',{'data' : data})

def update_customer(request,id):
    data = customuser.objects.get(id=id)
    form = customer_form(instance=data)
    if request.method == 'POST':
        form = customer_form(request.POST or None,request.FILES or None,instance=data or None)
        if form.is_valid():
            form.save()
            return redirect('view_customer')
    return render(request,'edit_customer.html',{'form' : form})


def delete_customer(request,id):
    customuser.objects.get(id=id).delete()
    return redirect('view_customer')

def customer_dashboard(request):
    welcome = f'welcome,{request.user.username}'
    data = customuser.objects.filter(is_customer=True)
    return render(request,'customer_dashboard.html',{'data' : data, 'welcome' : welcome})

def customer_profilecard(request):
    username = request.user
    data = customuser.objects.filter(is_customer=True,username=request.user)
    return render(request,'customer_profilecard.html',{'data' : data,'username' : username})

@login_required
def schedule_work(request):
    username = request.user.username
    if request.user.is_worker:
        form = schedule_form(initial={'Customuser' : request.user})
        form.fields['Customuser'].queryset = customuser.objects.filter(is_worker=True,username=request.user.username)
        if request.method == 'POST':
            form = schedule_form(request.POST)
            if form.is_valid():
                form.save()
                return redirect('view_schedulework')
        return render(request, 'schedule_work.html', {'form': form, 'username' : username})
    else:
        messages.error(request,'no access other-than worker')
        return redirect('view_customerschedule')



def view_schedulework(request):
    user = request.user
    data = schedule.objects.filter(Customuser=user)
    return render(request,'view_schedulework.html',{'data' : data})
# def view_schedulework(request):
#     data = appointment.objects.all()
#     return render(request, 'view_schedulework.html', {'data': data})

def view_customerschedule(request):
    data = schedule.objects.all()
    return render(request,'view_customerschedule.html',{'data' : data})


def update_schedulework(request,id):
    username = request.user.username
    if request.user.is_worker:
        data = schedule.objects.get(id=id)
        form = schedule_form(initial={'Customuser' : request.user})
        form.fields['Customuser'].queryset = customuser.objects.filter(is_worker=True,username=request.user.username)
        if request.method == 'POST':
            form = schedule_form(request.POST or None, instance=data or None)
            if form.is_valid():
                form.save()
                return redirect('view_schedulework')
    return render(request,'edit_schedulework.html',{'form' : form,'username' : username})

def delete_schedulework(request,id):
    schedule.objects.get(id=id).delete()
    return redirect('view_schedulework')

def worker_dashboard(request):
    data = customuser.objects.filter(is_worker=True)
    return render(request,'worker_dashboard.html',{'data' : data})


# def available_schedules(request):
#     data = appointment.objects.all()
#     return render(request,'available_schedules.html',{'data' : data})

def take_appointment(request,id):
    s = schedule.objects.get(id=id)
    c = customuser.objects.get(username=request.user)
    appo = appointment.objects.filter(Customuser=c, Schedule=s)
    if appo.exists():
        messages.info(request,'you have already requested for this schedule')
        return redirect('view_customerschedule')
    else:
        if request.method == 'POST':
            obj = appointment()
            obj.Customuser = c
            obj.Schedule = s
            obj.save()
            messages.info(request,'appointment requested successfully')
            return redirect('view_appointment')
    return render(request,'appointment.html', {'Schedule' : s})



def view_appointment(request):
    c = customuser.objects.get(username=request.user)
    a = appointment.objects.filter(Customuser=c)
    return render(request,'view_appointment.html',{'appointment' : a})

@login_required
@user_passes_test(lambda u : u.is_worker)
def view_worker_appointment(request):
    c = customuser.objects.get(username=request.user)
    a = appointment.objects.filter(Schedule__Customuser=c)
    return render(request,'view_worker_appointment.html',{'appointment' : a})
        # u can also add is_worker=True inside get() to narrow the search down to only workers,but its not
        #needed right now, cos while adding schedule only workers can add it, so no probs.
# def view_worker_appointment(request):
#     worker = customuser.objects.get(username=request.user, is_worker=True)
#     appointments = appointment.objects.filter(Schedule__Customuser=worker)
#     return render(request, 'view_worker_appointment.html', {'appointments': appointments})

def approve_appointment(request,id):
    a = appointment.objects.get(id=id)
    a.status = 1
    a.save()
    messages.info(request,'appointment approved')
    return redirect('view_worker_appointment')

def reject_appointment(request,id):
    a = appointment.objects.get(id=id)
    a.status = 2
    a.save()
    messages.info(request,'appointment rejected')
    return redirect('view_worker_appointment')


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            if user.is_superuser:
                return redirect('admin_dashboard')
            elif user.is_customer:
                return redirect('customer_dashboard')
            elif user.is_worker:
                return redirect('worker_dashboard')
        else:
             messages.info(request,'invalid credentials')
    return render(request,'login.html')


def welcome(request):
    username = request.user.username
    return render(request,'welcome.html',{'username' : username})

def logout_user(request):
    logout(request)
    return redirect('login_user')


def payment(request):
    form = bill_form()
    if request.method == 'POST':
        form = bill_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_payment')
    return render(request,'payment.html',{'form' : form})


def view_payment(request):
    data = Bill.objects.all()
    return render(request,'view_payment.html',{'data' : data})


# @login_required -this is a decorator for security but now i commented this


def view_userpayment(request):
    user = request.user
    data = Bill.objects.filter(Customuser=user)
    return render(request,'view_userpayment.html',{'data' : data})


def bill_payment(request,id):
    bi = Bill.objects.get(id=id)
    if request.method == 'POST':
        c = request.POST.get('card')
        cv = request.POST.get('cvv')
        exp_d = request.POST.get('exp_date')
        card(bill=bi,card_no=c,card_cvv=cv,expiry_date=exp_d).save()
        bi.status = 1
        bi.save()
        messages.info(request,'bill paid successfully')
        return redirect('bill_history')
    return render(request,'bill_payment.html')

def bill_directpayment(request,id):
    bi = Bill.objects.get(id=id)
    bi.status = 2
    bi.save()
    messages.info(request,'bill paid directly as cash')
    return redirect('bill_history')

def bill_history(request):
    u = customuser.objects.get(username=request.user)
    bill = Bill.objects.filter(Customuser=u,status__in=[0,1,2])
    return render(request,'view_bill_history.html',{'bills' : bill})


def complaint(request):
    username = request.user.username
    form = complaint_form(initial={'Customuser': request.user})
    form.fields['Customuser'].queryset = customuser.objects.filter(username=request.user.username)
    if request.method == 'POST':
        form = complaint_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_complaint')
    return render(request, 'complaint.html', {'form': form, 'username': username})

def view_complaint(request):
    user = request.user
    comp = complaints.objects.filter(Customuser=user)
    return render(request,'view_complaint.html',{'comp' : comp})

# def view_complaint_admin(request):
#     if request.user.is_superuser:
#         comp = complaints.objects.all()
#     else:
#         messages.info(request,'no access other than admin')
#         return redirect('customer_dashboard')
#     return render(request,'view_complaint_admin.html',{'comps' : comp})
def view_complaint_admin(request):
    if request.user.is_superuser:
        comps = complaints.objects.all().select_related('Customuser')
    else:
        messages.info(request, 'No access other than admin')
        return redirect('customer_dashboard')
    return render(request, 'view_complaint_admin.html', {'comps': comps})


# def reply_complaint(request,id):
#     if request.user.is_superuser:
#         comp = complaints.objects.get(id=id)
#         form = reply_complaintform()
#         if request.method == 'POST':
#             form = reply_complaintform(request.POST)
#             if form.is_valid():
#                 reply = form.cleaned_data.get('reply')
#                 comp.reply = reply
#                 comp.save()
#                 return redirect('view_complaint_admin')
#     return render(request,'reply_complaint.html',{'form' : form})
def reply_complaint(request, id):
    if request.user.is_superuser:
        comp = complaints.objects.get(id=id)
        form = reply_complaintform()
        if request.method == 'POST':
            form = reply_complaintform(request.POST)
            if form.is_valid():
                reply_complaint = form.cleaned_data.get('reply_complaint')
                comp.reply_complaint = reply_complaint
                comp.save()
                return redirect('view_complaint_admin')
    else:
        messages.info(request, 'No access other than admin')
        return redirect('customer_dashboard')
    return render(request, 'reply_complaint.html', {'form': form, 'comp': comp})
