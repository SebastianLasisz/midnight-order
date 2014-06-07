from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from Members.models import Member
from News.models import News
import json
import urllib2
import operator


def index(request):
    news = News.objects.all()[:10]
    news2 = list(reversed(news))
    return render_to_response('index.html', locals(), RequestContext(request))


def policies(request):
    return render(request, 'policies.html')


def calendar(request):
    return render(request, 'calendar.html')


def contact(request):
    return render(request, 'contact.html')


def forum(request):
    return render(request, 'forum.html')


def login(request):
    return render(request, 'login.html')


def members(request):
    a = []
    j = urllib2.urlopen('http://eu.battle.net/api/wow/guild/defias-brotherhood/Midnight%20Order?fields=members')
    js = json.load(j)
    arr = js['members']
    for rs in arr:
        try:
            m = Member(name=rs['character']['name'],
                       level=rs['character']['level'],
                       thumbnail="http://eu.battle.net/static-render/eu/" + rs['character']['thumbnail'],
                       class_number=rs['character']['class'],
                       class_name=char_number_to_string(rs['character']['class']),
                       spec=rs['character']['spec']['name'],
                       rank=rs['rank'],
                       rank_name=rank_to_string(rs['rank']),
                       armory="http://eu.battle.net/wow/en/character/defias-brotherhood/" + rs['character'][
                           'name'] + "/advanced")
            a.insert(0, m)
        except KeyError:
            m = Member(name=rs['character']['name'],
                       level=rs['character']['level'],
                       thumbnail="http://eu.battle.net/static-render/eu/" + rs['character']['thumbnail'],
                       class_number=rs['character']['class'],
                       class_name=char_number_to_string(rs['character']['class']),
                       spec="none",
                       rank=rs['rank'],
                       rank_name=rank_to_string(rs['rank']),
                       armory="http://eu.battle.net/wow/en/character/defias-brotherhood/" + rs['character'][
                           'name'] + "/advanced")
            a.insert(0, m)
    members2 = sorted(a, key=operator.attrgetter('rank'))
    return render_to_response('members.html', locals(), RequestContext(request))


def char_number_to_string(request):
    if request == 1:
        character = "Warrior"
    elif request == 2:
        character = "Paladin"
    elif request == 3:
        character = "Hunter"
    elif request == 4:
        character = "Rogue"
    elif request == 5:
        character = "Priest"
    elif request == 6:
        character = "Death Knight"
    elif request == 7:
        character = "Shaman"
    elif request == 8:
        character = "Mage"
    elif request == 9:
        character = "Warlock"
    elif request == 10:
        character = "Monk"
    elif request == 11:
        character = "Druid"
    else:
        character = "Unknown"

    return character


def rank_to_string(request):
    if request == 0:
        rank_s = "Guild Master"
    elif request == 1:
        rank_s = "Officer"
    elif request == 2:
        rank_s = "Leader"
    elif request == 3:
        rank_s = "Veteran"
    elif request == 4:
        rank_s = "Vanquisher"
    elif request == 5:
        rank_s = "Raider"
    elif request == 6:
        rank_s = "Cadet"
    elif request == 7:
        rank_s = "Member"
    else:
        rank_s = "Initiate"

    return rank_s


def recruitment(request):
    return render(request, 'recruitment.html')