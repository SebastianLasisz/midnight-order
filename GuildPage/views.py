from django.db import IntegrityError
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from Members.models import Member
from News.models import News
from Register.models import Register, UserProfile
from Register.form import *
from GuildPage.form import *
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
import json
import urllib2
import operator


def index(request):
    news = News.objects.all()[:10]
    news2 = list(reversed(news))
    return render_to_response('index.html', locals(), RequestContext(request))


def policies(request):
    return render(request, 'policies.html')


def forum(request):
    return render(request, 'forum.html')


def login(request):
    return render(request, 'login.html')


def log_out(request):
    logout(request)
    logged_out = True
    news = News.objects.all()[:10]
    news2 = list(reversed(news))
    return render_to_response('index.html', locals(), RequestContext(request))


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']
            recipients = ['sedi1ster@gmail.com']
            if cc_myself:
                recipients.append(sender)
        else:
            return render_to_response('contact.html', locals(), RequestContext(request))
        from django.core.mail import send_mail
        send_mail(subject, message, sender, recipients)
        return HttpResponseRedirect('/thanks/')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {
        'form': form,
    })


def register(request):
    if request.method == 'POST':
        form = RegisterNewUserForm(request.POST)
        try:
            if form.is_valid():
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                repeat_password = form.cleaned_data['repeat_password']
                captcha = form.cleaned_data['captcha']
                r = User(username=username,
                                email=email,
                                password=password)
                try:
                    r.save()
                    subject = "Your Midnight Order account confirmation"
                    message = "Hello,"+username+", and thanks for signing up for a Midnight Order account."
                    from django.core.mail import send_mail
                    send_mail(subject, message, 'accounts@midnightorder.com', [email])
                except IntegrityError:
                    error = "That name is already taken"
                    return render_to_response('register.html', locals(), RequestContext(request))
                g = Group.objects.get(name='Member')
                g.user_set.add(r)
            else:
                return render_to_response('register.html', locals(), RequestContext(request))
            return HttpResponseRedirect('/register_complete/')
        except:
            error = "Captcha input doesn't match. Please reenter it."
            return render_to_response('register.html', locals(), RequestContext(request))
    else:
        form = RegisterNewUserForm()

    return render(request, 'register.html', {
        'form': form,
    })


def thanks(request):
    return render(request, 'thanks.html')


def terms(request):
    return render(request, "terms_of_service.html")


def cookies(request):
    return render(request, "cookies.html")


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
    memb = Register.objects.all()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            irl_name = form.cleaned_data['irl_name']
            age = form.cleaned_data['age']
            country = form.cleaned_data['country']
            about_yourself = form.cleaned_data['about_yourself']
            username = form.cleaned_data['username']
            class_1 = form.cleaned_data['class_1']
            spec = form.cleaned_data['spec']
            wol_logs = form.cleaned_data['wol_logs']
            professions = form.cleaned_data['professions']
            previous_guilds = form.cleaned_data['previous_guilds']
            contacs = form.cleaned_data['contacs']
            reason = form.cleaned_data['reason']
            questions = form.cleaned_data['questions']
            rules = form.cleaned_data['rules']
            experience = form.cleaned_data['experience']

            r = Register(name=irl_name,
                         age=age,
                         country=country,
                         about_yourself=about_yourself,
                         username=username,
                         class_1=class_1,
                         spec=spec,
                         wol_logs=wol_logs,
                         professions=professions,
                         previous_guilds=previous_guilds,
                         contacs=contacs,
                         reason=reason,
                         questions=questions,
                         experience=experience,
                         slug=username)
            r.save()
        else:
            return render_to_response('recruitment.html', locals(), RequestContext(request))
        return HttpResponseRedirect('/thanks/')
    else:
        form = RegisterForm()

    return render(request, 'recruitment.html', {
        'form': form, 'memb':memb
    })


def register_complete(request):
    return render(request, 'register_complete.html')


def upload_pic(request):
    username = None
    if request.user.is_authenticated():
        username = request.user.username
        picture = UserProfile.objects.get(user=User.objects.get(username=username))
        avatar = picture.avatar

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            up = UserProfile.objects.filter(user=User.objects.get(username=username))
            if up.exists():
                r = UserProfile.objects.get(user=User.objects.get(username=username))
                r.avatar = form.cleaned_data['avatar']
                r.save()
            else:
                r = UserProfile(user=User.objects.get(username=username),
                                avatar=form.cleaned_data['avatar'])
                r.save()
            return render_to_response('thanks.html', locals(), RequestContext(request))
        else:
            return render_to_response('upload_avatar.html', locals(), RequestContext(request))
    else:
        form = UserProfileForm()

    return render(request, 'upload_avatar.html', {
        'form': form, 'avatar':avatar
    })