from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext, loader, context
from django.shortcuts import render_to_response, redirect
import os;
import battlenet
from battlenet import *
from wowapi.api import WoWApi
import json
import urllib2


def hello(request):
    PUBLIC_KEY = os.environ.get('BNET_PUBLIC_KEY')
    PRIVATE_KEY = os.environ.get('BNET_PRIVATE_KEY')
    Connection.setup(public_key=PUBLIC_KEY, private_key=PRIVATE_KEY, locale='fr')
    realm = Realm(battlenet.UNITED_STATES, 'Nazjatar')
    guild = Guild(battlenet.EUROPE, 'Defias Brotherhood', 'Midnight Order')
    wowapi = WoWApi()
    asd = wowapi.get_guild('eu', 'Defias Brotherhood', 'Midnight Order')
    character = wowapi.get_character('eu','Doomhammer','Thetotemlord')
    j = urllib2.urlopen('http://eu.battle.net/api/wow/guild/defias-brotherhood/Midnight%20Order?fields=members')
    js = json.load(j)
    ourResult = js['members'][0]['character']['name']
    return HttpResponse(ourResult)


def index(request):
    return render(request, 'index.html')

def policies(request):
    return render(request, 'policies.html')

def awards(request):
    return render(request, 'awards.html')

def calendar(request):
    return render(request, 'calendar.html')

def contact(request):
    return render(request, 'contact.html')

def forum(request):
    return render(request, 'forum.html')

def gallery(request):
    return render(request, 'gallery.html')

def login(request):
    return render(request, 'login.html')


def members(request):
    j = urllib2.urlopen('http://eu.battle.net/api/wow/guild/defias-brotherhood/Midnight%20Order?fields=members')
    js = json.load(j)
    arr = js['members']
    yarr = []
    for rs in arr:
        yarr.append(rs['character']['name'])
    return render_to_response('members.html', locals(), RequestContext(request))


def recruitment(request):
    return render(request, 'recruitment.html')

def roster(request):
    return render(request, 'roster.html')

def talents(request):
    return render(request, 'talents.html')

def video(request):
    return render(request, 'video.html')