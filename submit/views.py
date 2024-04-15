from django.shortcuts import render
from .forms import (JmSubmitForm, PersonForm)
import requests

send_url = 'https://apis.aligo.in/send/'

def jm_submit(request):
    if request.method == "POST":
        submitForm = JmSubmitForm(request.POST)
        personForm = PersonForm(request.POST)
        if all([submitForm.is_valid(), personForm.is_valid()]):
            obj = submitForm.save(commit=False)
            obj.category = "jm"
            if request.user.is_authenticated:
                obj.user = request.user
            obj.save()
            person = personForm.save(commit=False)
            person.submit = obj
            person.save()
            context = {'submit': obj, 'person': person}
            sms_data = {'key': 'mbam9e8v586xu9vugol89i2wxvihrv9l',
                        'userid': 'ocean3885',
                        'sender': '01022324548',
                        'receiver': '01022324548',
                        'msg': '작명신청이 접수되었습니다.'
                        }
            send_response = requests.post(send_url, data=sms_data)
            print(send_response.json())
            return render(request, 'submit/submit_complete.html', context)
        else:
            context = {'submit': submitForm, 'person': personForm}
            return render(request, 'submit/jm_submit.html', context)

    submitForm = JmSubmitForm()
    personForm = PersonForm()
    context = {'submit': submitForm, 'person': personForm}
    return render(request, 'submit/jm_submit.html', context)



def gm_submit(request):
    return render(request, 'submit/gm_submit.html')

def sj_submit(request):
    return render(request, 'submit/sj_submit.html')

def etc_submit(request):
    return render(request, 'submit/etc_submit.html')