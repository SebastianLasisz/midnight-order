import json
import urllib2
import string

from django.conf import settings
from django.http import HttpResponse

from Progress.models import Boss, Raid, Stage


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


def character_progress(name, realm):
    try:
        character_json = urllib2.urlopen(
            'https://eu.api.battle.net/wow/character/' + replace_name(realm) + '/' + replace_name(
                name) + '?fields=progression&locale=en_GB&apikey=' + settings.API_KEY)
        character = json.load(character_json)
        raids = character['progression']['raids']
        index_of_last_raid = raids.__len__() - 1
        bosses = raids[index_of_last_raid]['bosses']
        normal_kills = []
        heroic_kills = []
        mythic_kills = []
        for b in bosses:
            normal_kills.append(b['normalKills'])
            heroic_kills.append(b['heroicKills'])
            mythic_kills.append(b['mythicKills'])
        result = [normal_kills, heroic_kills, mythic_kills]
        return result
    except:
        latest_expansion = Raid.objects.all().order_by('-id')[0]
        bosses = list(Boss.objects.filter(raid=latest_expansion))
        kills = []
        for b in bosses:
            kills.append([0])
        return [kills, kills, kills]


def replace_name(realm_name):
    return realm_name.replace(" ", "%20")


def get_raiders(realm, name):
    try:
        members_json = urllib2.urlopen(
            'https://eu.api.battle.net/wow/guild/' + replace_name(realm) + '/' + replace_name(
                name) + '?fields=members&locale=en_GB&apikey=' + settings.API_KEY)
        members = json.load(members_json)
        members = members['members']
        raiders = []
        for m in members:
            if m['rank'] <= 5:
                raider = [m['character']['name'], replace_name(m['character']['realm'].encode('ascii', 'ignore'))]
                raiders.append(raider)
        return raiders
    except:
        return []


def boss_kills():
    raiders = get_raiders('Defias Brotherhood', 'Midnight Order')
    latest_expansion = Raid.objects.all().order_by('-id')[0]
    bosses = list(Boss.objects.filter(raid=latest_expansion))
    new_bosses = []
    for b in bosses:
        new_bosses.append([str(b.name), 0, 0, 0])
    for r in raiders:
        character = character_progress(r[0], r[1])
        for x, sp in enumerate(character):
            for idx, s in enumerate(character[x]):
                if s >= 1:
                    new_bosses[idx][x + 1] += 1
    return new_bosses


def get_guild_progress():
    boss_spreadsheet = boss_kills()
    guild_progress = []
    for b in boss_spreadsheet:
        boss = b[0]
        if b[3] >= 7:
            progress = "Mythic"
        elif b[2] >= 7:
            progress = "Heroic"
        elif b[1] >= 7:
            progress = "Normal"
        else:
            progress = "Undefeated"
        guild_progress.append([boss, progress])
    return guild_progress


def update_guild_progress(request):
    guild_progress = get_guild_progress()
    for g in guild_progress:
        stage_of_progress = Stage.objects.get(progress=g[1])
        boss = Boss.objects.get(name=g[0])
        boss.progress = stage_of_progress
        boss.save()
    return HttpResponse(guild_progress)
