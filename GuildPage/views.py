import json
import urllib2
import operator
import datetime

from django.db import IntegrityError
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail

from django_messages.models import inbox_count_for
from Members.models import Member
from News.models import News
from News.form import *
from Register.models import Register, UserProfile
from Register.form import *
from GuildPage.form import *
from Progress.models import *
from forums.models import Post, PostRating, View


def index(request):
    all_news = list(reversed(News.objects.all()))
    count = len(all_news)
    news = all_news[:10]
    raids = Raid.objects.all()
    number_of_pages = range(1, int(1 + (count - ((count - 1) % 10) + 10) / 10))
    progress = []
    for r in raids:
        bosses = Boss.objects.filter(raid=Raid.objects.filter(name=r.name))
        progress.append(bosses)
    return render_to_response('index.html', locals(), RequestContext(request))


def paged_index(request, **kwargs):
    raids = Raid.objects.all()
    progress = []
    for r in raids:
        bosses = Boss.objects.filter(raid=Raid.objects.filter(name=r.name))
        progress.append(bosses)

    pk = int(kwargs.get('pk', None))
    all_news = list(reversed(News.objects.all()))
    count = len(all_news)
    number_of_pages = range(1, int(1 + (count - ((count - 1) % 10) + 10) / 10))
    if pk * 10 - count < 10 and pk > 1:
        news = all_news[((pk - 1) * 10):(pk * 10)]
        return render_to_response('index.html', locals(), RequestContext(request))
    else:
        return HttpResponseRedirect('/')


def policies(request):
    return render_to_response('policies.html', locals(), RequestContext(request))


def login(request):
    return render_to_response('login.html', locals(), RequestContext(request))


def log_out(request):
    logout(request)
    return index(request)


def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            n = News(title=title, description=description, name=request.user,
                     time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
            n.save()
        else:
            return render_to_response('add_news.html', locals(), RequestContext(request))
        return index(request)
    else:
        form = NewsForm()

    return render(request, 'add_news.html', {
        'form': form
    })


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
        send_mail("Midnight Order: Contact us - " + subject, message, sender, recipients)
        return thanks(request)
    else:
        form = ContactForm()

    return render(request, 'contact.html', {
        'form': form
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
                         password=make_password(password))
                try:
                    r.save()
                    us = UserProfile(user=r, avatar="/pic_folder/logo3.jpg", signature="")
                    us.save()
                    g = Group.objects.get(name='Initiate')
                    g.user_set.add(r)
                    subject = "Your Midnight Order account confirmation"
                    message = "Hello " + username + ". Thanks for signing up for a Midnight Order account. " \
                                                    "Your account will be given full access after confirmation."
                    send_mail(subject, message, 'noreply@midnightorder.com', [email], fail_silently=False)
                    send_mail("New user registration!", "New user has create an account. Check " + username + ".",
                              'noreply@midnightorder.com', ["sedi1ster@gmail.com"], fail_silently=False)
                except IntegrityError:
                    error = "That user name is already taken"
                    return render_to_response('register.html', locals(), RequestContext(request))
            else:
                return render_to_response('register.html', locals(), RequestContext(request))
            return register_complete(request)
        except:
            error = "Captcha input doesn't match. Please reenter it."
            return render_to_response('register.html', locals(), RequestContext(request))
    else:
        form = RegisterNewUserForm()

    return render(request, 'register.html', {
        'form': form
    })


def thanks(request):
    message = "Thanks for sending us request. We will look into it soon."
    return render_to_response('notifications.html', locals(), RequestContext(request))


def register_complete(request):
    message = "Your account is activated. You can log in <a href=\"/login\">here."
    return render_to_response('notifications.html', locals(), RequestContext(request))


def terms(request):
    return render_to_response('terms_of_service.html', locals(), RequestContext(request))


def cookies(request):
    return render_to_response('cookies.html', locals(), RequestContext(request))


def media(request):
    return HttpResponse(status=403)


def credit(request):
    return render_to_response('credits.html', locals(), RequestContext(request))


def members(request):
    a = []
    j = urllib2.urlopen(
        'https://eu.api.battle.net/wow/guild/Defias%20Brotherhood/Midnight%20Order?fields=members&locale=en_GB&apikey=a7w8cuncze9u7nqrnubfx3dzkmahdy55')
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
            import datetime

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
                         slug=username + datetime.datetime.now().strftime("%y-%m-%d-%H-%M"))
            r.save()
            from forums.models import Topic, Post, Forum

            user = UserProfile.objects.get(user=User.objects.get(username="Unregistered"))
            topic_forum = Forum.objects.get(name="Applications")
            topic_name = username + "'s Application"
            topic = Topic(forum=topic_forum, name=topic_name)
            topic.save()
            post_body = "Real name: 	" + irl_name + "\nAge: 	" + str(age) + "\nFrom: 	" + country +\
                        "\nAbout: 	" + about_yourself + "\nCharacter name: 	" + username + \
                        "\nClass: 	" + class_1 + "\nSpecialisation: 	" + spec + "\nWorld of Logs: 	" + \
                        wol_logs + "\nProfessions: 	" + professions + "\nReason of leaving previous guilds: 	" + \
                        previous_guilds + "\nKnowledge of other people in guild: 	" + contacs + \
                        "\nReason to join us: 	" + reason + "\nQuestions to us: 	" \
                        + questions + "\nRaiding experience: 	" + experience

            post = Post(topic=topic, body=post_body, user=user)
            post.save()
            topic.last_post = post
            topic.save()
        else:
            return render_to_response('recruitment.html', locals(), RequestContext(request))
        return HttpResponseRedirect('/thanks/')
    else:
        form = RegisterForm()

    return render(request, 'recruitment.html', {
        'form': form, 'memb': memb
    })


def profile(request):
    if request.user.is_authenticated():
        username = request.user.username
        picture = UserProfile.objects.get(user=User.objects.get(username=username))
        avatar = picture.avatar
        signature = picture.signature
        style = picture.style

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            up = UserProfile.objects.filter(user=User.objects.get(username=username))
            u = User.objects.get(username=username)
            if form.cleaned_data['password'] != '' and form.cleaned_data['repeat_password'] != '' \
                    and form.cleaned_data['old_password'] != '':
                if form.cleaned_data['password'] == form.cleaned_data['repeat_password'] and \
                        request.user.check_password(form.cleaned_data['old_password']):
                    u.password = make_password(form.cleaned_data['password'])
                    u.save()
                else:
                    error = "Current password is invalid or new passwords doesn't match."
                    return render_to_response('profile.html', locals(), RequestContext(request))
            if up.exists():
                r = UserProfile.objects.get(user=User.objects.get(username=username))
                if form.cleaned_data['avatar'] is not None:
                    r.avatar = form.cleaned_data['avatar']
                if form.cleaned_data['signature'] != "":
                    r.signature = form.cleaned_data['signature']
                r.style = form.cleaned_data['style']
                r.save()
            else:
                r = UserProfile(user=User.objects.get(username=username),
                                avatar=form.cleaned_data['avatar'],
                                signature=form.cleaned_data['signature'],
                                style=form.cleaned_data['style'])
                r.save()
            error1 = "Your settings have been saved."
            picture = UserProfile.objects.get(user=User.objects.get(username=username))
            avatar = picture.avatar
            style = picture.style
            return render_to_response('profile.html', locals(), RequestContext(request))
        else:
            return render_to_response('profile.html', locals(), RequestContext(request))
    else:
        form = UserProfileForm(initial={'signature': signature, 'style': style})

    return render(request, 'profile.html', {
        'form': form, 'avatar': avatar, 'username': username, 'signature': signature, 'style': style
    })


def ajax_test(request):
    if request.is_ajax():
        if request.user.is_authenticated():
            msg = inbox_count_for(request.user)
        else:
            msg = "Woops! Something went wrong."
    else:
        msg = "Woops! Something went wrong."
    return HttpResponse(msg)


def ajax_upvote(request):
    if request.is_ajax():
        if request.user.is_authenticated():
            user = UserProfile.objects.get(user=request.user)
            posts = Post.objects.filter(user=user)
            rated_posts = PostRating.objects.filter(post__in=posts).count()
            msg = rated_posts
        else:
            msg = "Woops! Something went wrong."
    else:
        msg = "Woops! Something went wrong."
    return HttpResponse(msg)


def new_content(request):
    unread_posts = collection_filter_view(request.user, View.objects.filter(visited=False, user=request.user))
    posts_day = collection_filter_post(request.user, get_topic(get_posts(1)))
    posts_week = collection_filter_post(request.user, get_topic(get_posts(7)))
    posts_month = collection_filter_post(request.user, get_topic(get_posts(31)))
    return render_to_response('new_content.html', locals(), RequestContext(request))


def get_posts(days):
    date = datetime.datetime.now() - datetime.timedelta(days=days)
    return Post.objects.filter(created__gte=date)


def collection_filter_view(user, collection):
    col = []
    for t in collection:
        if user.groups.all()[0].name != 'Initiate':
            if t.topic.forum.category.name != 'Forum: Restricted forums':
                col.append(t)
            else:
                if user.groups.all()[0].name == 'Leader' and t.topic.forum.name == 'Leader\'s Chat':
                    col.append(t)
                else:
                    if user.groups.all()[0].name == 'Officer':
                        col.append(t)
    return col


def get_topic(collection):
    topics_day = []
    for t in collection:
        topics_day.append(t.topic)
    return set(topics_day)


def collection_filter_post(user, collection):
    col = []
    for t in collection:
        if user.groups.all()[0].name != 'Initiate':
            if t.forum.category.name != 'Forum: Restricted forums':
                col.append(t)
            else:
                if user.groups.all()[0].name == 'Leader' and t.forum.name == 'Leader\'s Chat':
                    col.append(t)
                else:
                    if user.groups.all()[0].name == 'Officer':
                        col.append(t)
    return col