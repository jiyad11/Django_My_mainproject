from django import forms
from django.contrib.auth.forms import UserCreationForm

from myapp.models import work_types, customuser, schedule, Bill, card, appointment, complaints


class work_form(forms.ModelForm):
    class Meta:
        model = work_types
        fields = ('works',)


gender_choice = [
        ('male', 'MALE'),
        ('female', 'FEMALE'),
        ('others', 'OTHERS')
    ]

class WorkerForm(UserCreationForm):

    gender = forms.ChoiceField(choices=gender_choice,required=True,widget=forms.RadioSelect)
    class Meta:
        model = customuser
        fields = ('username','first_name','last_name','type_of_work','experience','password1','password2',
                  'date_of_birth','gender','email','address','photo')

        widgets = {
            'date_of_birth' : forms.widgets.DateInput(attrs={'type' : 'date'})
        }



    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            user = customuser.objects.exclude(pk=self.instance.pk).get(username=username)
            raise forms.ValidationError('Username already exists')
        except customuser.DoesNotExist:
            return username

class customer_form(UserCreationForm):
    gender = forms.ChoiceField(choices=gender_choice,required=True,widget=forms.RadioSelect)

    class Meta:
        model = customuser
        fields = ('username','first_name','last_name','password1','password2','date_of_birth','gender','email','address','photo','is_active')
        widgets = {
            'date_of_birth' : forms.widgets.DateInput(attrs={'type' : 'date'}),
            'is_active' : forms.HiddenInput(),
        }
    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            user = customuser.objects.exclude(pk=self.instance.pk).get(username=username)
            raise forms.ValidationError('username already exists')
        except customuser.DoesNotExist:
            return username


class schedule_form(forms.ModelForm):
    # Customuser = forms.ModelChoiceField(queryset=customuser.objects.filter(is_worker=True))
    class Meta:
        model = schedule
        fields = ('Customuser','type_of_work','date_available','start_time','end_time')
        widgets = {
            'date_available' : forms.widgets.DateInput(attrs={'type' : 'date'}),
            'start_time' : forms.widgets.TimeInput(attrs={'type':'time'}),
            'end_time' : forms.widgets.TimeInput(attrs={'type' : 'time'})
        }


class appointment_form(forms.ModelForm):
    class Meta:
        model = appointment
        fields = ('Customuser','Schedule')


class bill_form(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ('Customuser','bill_date','amount')


class payment_form(forms.ModelForm):
    class Meta:
        model = card
        fields = ('bill','card_no','card_cvv','expiry_date')

class complaint_form(forms.ModelForm):
    class Meta:
        model = complaints
        fields = ('Customuser','type_complaint')

class reply_complaintform(forms.Form):
    reply_complaint = forms.CharField(widget=forms.Textarea, required=True)

    def clean_reply(self):
        reply_complaint = self.cleaned_data['reply_complaint']
        if reply_complaint == '':
            raise forms.ValidationError('This Field is required')
        return reply_complaint