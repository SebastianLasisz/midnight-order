import json
import urllib2
from django.conf import settings
from django.http import HttpResponse
import string


def get_zones():
    json_file = urllib2.urlopen('https://www.warcraftlogs.com:443/v1/zones?api_key=' + settings.WL_API_KEY)
    js = json.load(json_file)
    zone = []
    for j in js:
        zone.insert(0, [j['id'], j['name']])
    return HttpResponse(zone)


def get_active_zones():
    json_file = urllib2.urlopen('https://www.warcraftlogs.com:443/v1/zones?api_key=' + settings.WL_API_KEY)
    js = json.load(json_file)
    zone = []
    for j in js:
        if not j['frozen']:
            zone.insert(0, [j['id'], j['name']])
    return HttpResponse(zone)


def get_bosses():
    json_file = urllib2.urlopen('https://www.warcraftlogs.com:443/v1/zones?api_key=' + settings.WL_API_KEY)
    js = json.load(json_file)
    encounters = []
    for j in js:
        encounters2 = j['encounters']
        for e in encounters2:
            encounters.insert(0, [e['id'], e['name']])
    return HttpResponse(encounters)


def get_boss_name(id_of_boss):
    json_file = urllib2.urlopen('https://www.warcraftlogs.com:443/v1/zones?api_key=' + settings.WL_API_KEY)
    js = json.load(json_file)
    encounters = 0
    for j in js:
        encounters2 = j['encounters']
        for e in encounters2:
            if e['id'] == id_of_boss:
                encounters = e['name']
    if not encounters:
        encounters = "Wrong id of boss"
    return HttpResponse(encounters)


def get_boss_id(name_of_boss):
    json_file = urllib2.urlopen('https://www.warcraftlogs.com:443/v1/zones?api_key=' + settings.WL_API_KEY)
    js = json.load(json_file)
    encounters = ""
    for j in js:
        encounters2 = j['encounters']
        for e in encounters2:
            if e['name'].upper() == name_of_boss.upper():
                encounters = e['id']
    if not encounters:
        encounters = "Wrong name of boss"
    return HttpResponse(encounters)


def get_class_id(name_of_class):
    json_file = urllib2.urlopen('https://www.warcraftlogs.com/v1/classes?api_key=' + settings.WL_API_KEY)
    js = json.load(json_file)
    id_of_class = 0
    for j in js:
        if j['name'].upper() == name_of_class.upper():
            id_of_class = j['id']
    return HttpResponse(id_of_class)


def get_class_name(id_of_class):
    json_file = urllib2.urlopen('https://www.warcraftlogs.com/v1/classes?api_key=' + settings.WL_API_KEY)
    js = json.load(json_file)
    name_of_class = ""
    for j in js:
        if j['id'] == id_of_class:
            name_of_class = j['name']
    return HttpResponse(name_of_class)


def get_spec_name(name_or_id__of_class, id_of_spec):
    try:
        name_or_id__of_class = string.capwords(name_or_id__of_class)
    except:
        pass
    json_file = urllib2.urlopen('https://www.warcraftlogs.com/v1/classes?api_key=' + settings.WL_API_KEY)
    js = json.load(json_file)
    spec = 0
    for j in js:
        if j['name'] == name_or_id__of_class or j['id'] == name_or_id__of_class:
            for j_spec in j['specs']:
                if j_spec['id'] == id_of_spec:
                    spec = j_spec['name']
    return HttpResponse(spec)


def get_spec_id(name_or_id__of_class, name_of_spec):
    try:
        name_or_id__of_class = string.capwords(name_or_id__of_class)
        name_of_spec = string.capwords(name_of_spec)
    except:
        name_of_spec = string.capwords(name_of_spec)
    json_file = urllib2.urlopen('https://www.warcraftlogs.com/v1/classes?api_key=' + settings.WL_API_KEY)
    js = json.load(json_file)
    spec = ""
    for j in js:
        if j['name'] == name_or_id__of_class or j['id'] == name_or_id__of_class:
            for j_spec in j['specs']:
                if j_spec['name'] == name_of_spec:
                    spec = j_spec['id']
    return HttpResponse(spec)


def zone_test(request):
    return HttpResponse(get_spec_id('druid', 'balance'))