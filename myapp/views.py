from django.shortcuts import render

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.template.loader import get_template

from myapp.forms import work_form, WorkerForm, customer_form, schedule_form, bill_form, complaint_form, \
    reply_complaintform
from myapp.models import work_types, schedule, customuser, Bill, card, appointment, complaints
from myapp.utils import render_to_pdf
from django.http import HttpResponse
from django.db.models import Q


#we redirecting using views function name, not htmlname


# Create your views here.

########################################################################################
def is_admin(user):
    return user.is_authenticated and user.is_superuser  ## The is_authenticated attribute checks if a user is authenticated,
                      ## meaning they have logged in and their session is active.

##########################################################################################

def index(request):
    return render(request,'index.html')

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request,'admin/admin_dashboard.html')


@login_required
@user_passes_test(is_admin)
def add_works(request):
    form = work_form()
    if request.method == 'POST':
        form = work_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_works')
    return render(request,'admin/add_works.html',{'form' : form})

@login_required
@user_passes_test(is_admin)
def view_works(request):
    data = work_types.objects.all()
    return render(request,'admin/view_works.html',{'data' : data})


@login_required
@user_passes_test(is_admin)
def update_works(request,id):
    data = work_types.objects.get(id=id)
    form = work_form(instance=data)
    if request.method == 'POST':
        form = work_form(request.POST or None , instance=data or None)
        if form.is_valid():
            form.save()
            return redirect('view_works')
    return render(request,'admin/edit_works.html',{'form' : form})


@login_required
@user_passes_test(is_admin)
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
            return redirect('waiting_for_approval')
    return render(request,'worker/add_worker.html',{'form' : form})


def approve_worker(request, worker_id):
    worker = customuser.objects.get(id=worker_id)
    worker.is_active = True
    worker.save()
    messages.info(request, 'worker approved')
    return redirect('view_worker')

def reject_worker(request, worker_id):
    worker = customuser.objects.get(id=worker_id)
    worker.delete()
    messages.info(request, 'worker rejected')
    return redirect('view_worker')

def view_worker_needsApproval(request):
    data = customuser.objects.filter(is_worker=True,is_active=False)
    return render(request,'admin/view_worker_needsApproval.html',{'data' : data})



def view_worker(request):
    data = customuser.objects.filter(is_worker=True, is_active=True)
    return render(request,'admin/view_worker.html',{'data' : data})


def view_painter(request):
    data = customuser.objects.filter(is_worker=True, type_of_work__works='painting')
    schedules = schedule.objects.filter(type_of_work__works='painting',Customuser__in=data)
    return render(request,'view_painter.html',{'data':data, 'schedules' : schedules})

def view_carpenter(request):
    data = customuser.objects.filter(is_worker=True, type_of_work__works='carpentery')
    schedules = schedule.objects.filter(type_of_work__works='carpentery',Customuser__in=data)
    return render(request, 'view_carpenter.html', {'data': data, 'schedules': schedules})

def update_worker(request,id):
    data = customuser.objects.get(id=id)
    form = WorkerForm(instance=data)
    if request.method == 'POST':
        form = WorkerForm(request.POST or None,request.FILES or None,instance=data)
        if form.is_valid():
            form.save()
            return redirect('view_worker')
    return render(request,'worker/edit_worker.html',{'form' : form})


@login_required
@user_passes_test(is_admin)
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
            user.is_active = False
            user.save()
            messages.info(request,'waiting for admin approval')
            return redirect('waiting_for_approval')
    return render(request,'customer/add_customer.html',{'form' : form})

def waiting_for_approval(request):
    return render(request,'waiting_for_approval.html')

def approve_customer(request, customer_id):
    customer = customuser.objects.get(id=customer_id)
    customer.is_active = True
    customer.save()
    messages.info(request, 'Customer approved')
    return redirect('view_customer')

def reject_customer(request, customer_id):
    customer = customuser.objects.get(id=customer_id)
    customer.delete()
    messages.info(request, 'Customer rejected')
    return redirect('view_customer')


def view_customer(request):
    data = customuser.objects.filter(is_customer=True,is_active=True)
    return render(request,'admin/view_customer.html',{'data' : data})

def view_loggedIn_customer_only(request):
    data = customuser.objects.filter(username=request.user.username)
    return render(request,'view_loggedIn_customer.html',{'data':data})

def view_customer_needsApproval(request):
    data = customuser.objects.filter(is_customer=True,is_active=False)
    return render(request,'admin/view_customer_needsApproval.html',{'data' : data})


@login_required(login_url='login_user')
def update_customer(request,id):
    user = request.user
    data = customuser.objects.get(id=id)
    form = customer_form(instance=data)
    if request.method == 'POST':
        form = customer_form(request.POST or None,request.FILES or None,instance=data or None)
        if form.is_valid():
            form.save()
            return redirect('view_customer')
    return render(request,'customer/edit_customer.html',{'form' : form, 'user':user})

@login_required
@user_passes_test(is_admin)
def delete_customer(request,id):
    customuser.objects.get(id=id).delete()
    return redirect('view_customer')


@login_required(login_url='login_user')
@user_passes_test(lambda u : u.is_customer)
def customer_dashboard(request):
    welcome = f'welcome,{request.user.username}'
    data = customuser.objects.filter(is_customer=True)
    return render(request,'customer/customer_dashboard.html',{'data' : data, 'welcome' : welcome})

def customer_profilecard(request):
    username = request.user
    data = customuser.objects.filter(is_customer=True,username=request.user)
    return render(request,'customer/customer_profilecard.html',{'data' : data,'username' : username})

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
                messages.info(request,'schedule created successfully')
                return redirect('view_schedulework')
        return render(request, 'worker/schedule_work.html', {'form': form, 'username' : username})
    else:
        messages.error(request,'no access other-than worker')
        return redirect('view_customerschedule')


def view_schedulework(request):
    user = request.user
    data = schedule.objects.filter(Customuser=user)
    return render(request,'view_schedulework.html',{'data' : data})


def view_customerschedule(request):
    data = schedule.objects.all()
    return render(request,'customer/view_customerschedule.html',{'data' : data})

def view_adminschedule(request):
    data = schedule.objects.all()
    return render(request,'admin/view_adminschedule.html',{'data' : data})



########## seperate section to view workers schedules to take appointments #########
@login_required(login_url='login_user')
def painter_schedule(request):
    data = schedule.objects.filter(type_of_work__works='painting')
    return render(request,'customer/view_customerschedule.html',{'data':data})


@login_required(login_url='login_user')
def carpenter_schedule(request):
    data = schedule.objects.filter(type_of_work__works='carpentry')
    if data.exists():
        return render(request,'customer/view_customerschedule.html',{'data' : data})
    else:
        HttpResponse('<h1>sorry no schedules available right now<h1>')

@login_required(login_url='login_user')
def welder_schedule(request):
    data = schedule.objects.filter(type_of_work__works='welding')
    return render(request,'customer/view_customerschedule.html',{'data' : data})

@login_required(login_url='login_user')
def electrician_schedule(request):
    data = schedule.objects.filter(type_of_work__works='electrical')
    return render(request,'customer/view_customerschedule.html',{'data' : data})



@login_required(login_url='login_user')
def plumber_schedule(request):
    data = schedule.objects.filter(type_of_work__works='plumbing')
    return render(request,'customer/view_customerschedule.html',{'data' : data})

@login_required(login_url='login_user')
def tilesWorker_schedule(request):
    data = schedule.objects.filter(type_of_work__works='tiles and floorwork')
    if data.exists():
        return render(request, 'customer/view_customerschedule.html', {'data': data})
    else:
        return render(request, 'no_schedules.html')



######################################################################



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


@login_required(login_url='login_user')
@user_passes_test(lambda u : u.is_worker)
def worker_dashboard(request):
    welcome = f'welcome,{request.user.username}'
    data = customuser.objects.filter(is_worker=True)
    return render(request,'worker/worker_dashboard.html',{'data' : data, 'welcome' : welcome})



def take_appointment(request,id):
    s = schedule.objects.get(id=id)
    c = customuser.objects.get(username=request.user)
    appo = appointment.objects.filter(Customuser=c, Schedule=s)
    if appo.exists():
        messages.info(request,'you have already requested for this schedule')
        return redirect('view_customerschedule') # here use the message.info using loop or add a html page or js as a message to show if a user already submit an appointment
    else:
        if request.method == 'POST':
            obj = appointment()
            obj.Customuser = c
            obj.Schedule = s
            obj.save()
            messages.info(request,'appointment requested successfully')
            return redirect('view_appointment')
    return render(request,'appointment.html', {'Schedule' : s})


@login_required(login_url='login_user')
@user_passes_test(lambda u : u.is_customer or u.is_superuser)
def view_appointment(request):
    c = customuser.objects.get(username=request.user)
    a = appointment.objects.filter(Customuser=c)
    return render(request,'view_appointment.html',{'appointment' : a})

def view_admin_appointment(request):
    appo = appointment.objects.all()
    return render(request,'view_all_appointment.html',{'appo' : appo})

def view_admin_workerAppointment(request):
    appo = appointment.objects.all()
    return render(request,'view_all_worker_appointment.html',{'appo' : appo})


@login_required(login_url='login_user')
@user_passes_test(lambda u : u.is_worker)
def view_worker_appointment(request):
    c = customuser.objects.get(username=request.user)
    a = appointment.objects.filter(Schedule__Customuser=c)
    return render(request,'worker/view_worker_appointment.html',{'appointment' : a})
        # u can also add is_worker=True inside get() to narrow the search down to only workers,but its not
        #needed right now, cos while adding schedule only workers can add it, so no probs.





def view_approved_appointments(request):
    c = customuser.objects.get(username=request.user)

    # Filter appointments to only include those with status=1 (approved)
    a = appointment.objects.filter(Q(Schedule__Customuser=c) & Q(status=1))

    return render(request, 'worker/view_worker_appointment.html', {'appointment': a})


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
                return redirect('index')
            elif user.is_worker:
                return redirect('worker_dashboard')
        else:
             messages.info(request,'invalid credentials')
    return render(request,'login.html')



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
    return render(request,'admin/payment.html',{'form' : form})

@login_required(login_url='login_user')
@user_passes_test(is_admin)
def view_payment(request):
    data = Bill.objects.all()
    return render(request,'admin/view_payment.html',{'data' : data})


@login_required(login_url='login_user')
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


@login_required(login_url='login_user')
@user_passes_test(is_admin)
def bill_history_admin(request):
    u = customuser.objects.all()
    bill = Bill.objects.filter(status__in=[0,1,2])
    return render(request,'view_bill_history_admin.html',{'bills' : bill, 'u':u})

def get_invoice(request,id):
    data = customuser.objects.get(username=request.user)
    bill = Bill.objects.get(id=id)
    template = get_template('invoice.html')
    html = template.render({'data' : bill})
    pdf = render_to_pdf('invoice.html',{'data' : bill})
    return HttpResponse(pdf, content_type='application/pdf')

def view_invoice(request,id):
    u = customuser.objects.get(username=request.user)
    bill = Bill.objects.filter(id=id)
    return render(request,'invoice.html',{'data' : bill})


@login_required
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

@login_required
def view_complaint(request):
    user = request.user
    comp = complaints.objects.filter(Customuser=user)
    return render(request,'view_complaint.html',{'comp' : comp})



@login_required
@user_passes_test(is_admin)
def view_complaint_admin(request):
    if request.user.is_superuser:
        comps = complaints.objects.all().select_related('Customuser')
    else:
        messages.info(request, 'No access other than admin')
        return redirect('customer_dashboard')
    return render(request, 'admin/view_complaint_admin.html', {'comps': comps})


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
    return render(request, 'admin/reply_complaint.html', {'form': form, 'comp': comp})


def about_us(request):
    return  render(request,'about_us.html')

def contact_us(request):
    return render(request,'admin/contact_us.html')


def view_available_schedulePage(request):
    return render(request,'view_available_schedulePage.html')


