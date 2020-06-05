from django.http import HttpResponse
from django.shortcuts import render
import requests
from datetime import datetime, timedelta


def index(request):
    return render(request, 'index.html')




def info(request):
    # str(request.POST.get('handle','nizam'))
    handle = request.POST.get('handle', 'tonystark1234')
    if handle is '':
        handle='tonystark1234'
    
    r = requests.get('https://codeforces.com/api/user.info',
                     params={'handles': handle})
    user = r.json()
    if user['status'] == 'FAILED':
        return HttpResponse("No such user exits");
    data = {}
    data["handle"] = handle
    data["Contest_Rating"] = user['result'][0]['rating']
    data["src"] = "https:"+str(user['result'][0]['titlePhoto'])
    data["Max_Rating"] = user['result'][0]['maxRating']
    data["Friend_of"] = user['result'][0]['friendOfCount']
    if('Email' in user['result'][0]):
        data["Email"] = user['result'][0]['Email']
    else:
        data["Email"] = "Not Visible"
    data["Last_Visit"] = datetime.fromtimestamp(
        (user['result'][0]['lastOnlineTimeSeconds'])).strftime("%A, %B %d, %Y %I:%M:%S")
    data["Registered"] = datetime.fromtimestamp(
        (user['result'][0]['registrationTimeSeconds'])).strftime("%A, %B %d, %Y %I:%M:%S")
    return render(request, 'info.html', data)
