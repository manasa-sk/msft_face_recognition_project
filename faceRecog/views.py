from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from .models import *
from .recognizer import *
from django.contrib.auth.decorators import login_required

#GLOBAL VARIABLES
base_dir = os.path.dirname(os.path.dirname(__file__))
dataset = os.path.join(os.path.dirname(__file__), 'dataset')
post_people = []
user_posts = []
posts = []
notifications = []

#LOGIN/REGISTER PAGES
def login(request):
    return render(request, 'login.html', {'action': 'loginU', 'msg': ''})

def register(request):
    return render(request, 'register.html', {'action': 'registerU', 'msg': ''})


@login_required(login_url='login')
def loginU(request):
    users = User.objects.filter(is_active=True)
    for u in users:
        u.is_active = False
        u.save()
    if request.method=='POST':
        form = request.POST
        
        username = form.get('c_uname')
        password = form.get('pass')
        
        try:
            user = User.objects.get(username=username)
            if password == user.password:
                user.is_active = True
                user.save()
                login(request)
                return HttpResponseRedirect('/scanL/')
            else:
                msg = 'Password invalid.'
        except User.DoesNotExist:
            msg = 'User does not exist. Try registering.'
        return render(request, 'login.html', {'action': 'loginU', 'msg': msg})

@login_required(login_url='login')
def logout(request):
    user = getUser()
    if user is None:
        return render(request, 'login.html', {'action': 'loginU', 'msg': ''})
    user.is_active = False
    user.save()
    logout(request)
    return render(request, 'login.html', {'action': 'loginU', 'msg': ''})


def registerU(request):
    users = User.objects.filter(is_active=True)
    for u in users:
        u.is_active = False
        u.save()
    if request.method=='POST':
        form = request.POST

        name = form.get('c_name')
        username = form.get('c_uname')
        password = form.get('pass')
        cpassword = form.get('cpass')
        phone = form.get('phone')
        email = form.get('email')

        
        try:
            user = User.objects.get(username=username)
            if user.email == email:
                msg = 'User already exists. Try logging in.'
            else:
                msg = 'Username already taken.'
        except User.DoesNotExist:
            if len(password) < 6:
                msg = 'Password must contain at least 6 characters'
            elif password != cpassword and len(password)>=6:
                msg = 'Password does not match.'
            else:
                user = User(username=username, name=name, email=email, phone=phone, password=password)
                user.is_active = True
                user.save()
                login(request)
                return HttpResponseRedirect('/scanR/')
        return render(request, 'register.html', {'action': 'registerU', 'msg': msg})


def getUser():
    try:
        user = User.objects.get(is_active=True)
        return user
    except User.DoesNotExist:
        return None

def scanR(request):
    return render(request, 'scan.html', {'scan_url': 'cam_feed_R', 'action': 'register'})

def scanL(request):
    return render(request, 'scan.html', {'scan_url': 'cam_feed_L', 'action': 'login'})


#FACIAL RECOGNITION FOR LOGIN/REGISTER - FUNCTIONS
@login_required(login_url='login')
def cam_feed(request):
    global base_dir
    user = getUser()
    if user is None:
        return render(request, 'login.html', {'msg': ''})

    result, image = captureFace(user.username)
    if image is not None:
        pass
    else:
        msg = 'Failed due to Camera restrictions'
        user.is_active = False
        user.save()
        return render(request, 'register.html', {'msg': msg})
    saveimg = os.path.join(base_dir,"{}\{}\{}".format('media', 'temp_storage', '{}.jpg'.format(user.username)))
    if result == 1:
        User.objects.get(username=user.username).delete()
        msg = 'Face is already registered. Try logging in or use forgot password'
        os.remove(saveimg)
        logout(request)
        return render(request, 'register.html', {'msg': msg})
    else:
        login(request)
        return redirect('dash')
        
@login_required(login_url='login')
def check_face(request):
    global base_dir
    user = getUser()
    if user is None:
        return render(request, 'login.html', {'msg': ''})

    result = compareFace(username=user.username)
    if result is not None:
        pass
    else:
        msg = 'Failed due to Camera restrictions'
        return render(request, 'login.html', {'msg': msg})

    if result:
        login(request)
        return redirect('dash')
    logout(request)
    user.is_active = False
    msg = 'Face does not match, try registering'
    return render(request, 'login.html', {'msg': msg})


def identifyUsers(post):
    global post_people
    usernames = getUsers(post.image.url)
    post_people = [post, [User.objects.get(username=un) for un in usernames]]
    


#PLATFORM VIEWS
def get_notifications():
    user = getUser()
    if user is None:
        return HttpResponseRedirect('')
    notifications = []
    notifs = PostPeople.objects.filter(username=user)
    if not notifs:
        pass
    else:
        for notif in notifs:
            if notif.post_id.username != user:
                notifications.append(notif)
    return notifications

notifications = get_notifications() #GLOBAL VARIABLE

def get_notif_num():
    global notifications
    num = 0
    if notifications != []:
        for notif in notifications:
            if notif.is_checked:
                pass
            else:
                num+=1
    return num


@login_required(login_url='login')
def dashboard(request):
    user = getUser()
    getDash()
    if user is None or getDash() is False:
        return render(request, 'login.html', {'msg': ''})
    
    global posts
    global notifications
    return render(request, 'dashboard.html', {'user': user, 'posts': posts, 'notifications': get_notifications(), 'notif_num': get_notif_num()})

@login_required(login_url='login')
def profile(request):
    user = getUser()
    if user is None:
        return render(request, 'login.html', {'msg': ''})
    edit_opt = True
    global notifications
    getPosts(user)
    global user_posts
    return render(request, 'profile.html', {'user': user, 'p_user': user, 'edit_opt': edit_opt, 'userPosts': user_posts, 'notifications': get_notifications(), 'notif_num': get_notif_num()})

@login_required(login_url='login')
def showProfile(request):
    if request.method=='GET':
        uid = request.GET.get('uid')
        a_user = getUser()
        if a_user is None:
            return render(request, 'login.html', {'msg': ''})
        p_user = User.objects.get(username=uid)

        if a_user != p_user:
            edit_opt = False
        else:
            edit_opt = True
        global notifications
        getPosts(p_user)
        global user_posts
        return render(request, 'profile.html', {'user': a_user, 'p_user': p_user, 'edit_opt': edit_opt, 'userPosts': user_posts, 'notifications': get_notifications(), 'notif_num': get_notif_num()})


@login_required(login_url='login')
def showPost(request):
    if request.method=='GET':
        global post_people
        pid = request.GET.get('pid')
        post = Posts.objects.get(post_id=pid)
        people = PostPeople.objects.filter(post_id=post)
        user = getUser()
        if user is None:
            return render(request, 'login.html', {'action': 'loginU', 'msg': ''})
        global notifications

        try:
            check = request.GET.get('check')
            for notif in notifications:
                if notif.post_id == post:
                    notif.is_checked = True
                    notif.save()
        except AttributeError:
            pass

        if user in people:
            you = True
        else:
            you = False
        if user != post.username:
            delete_opt = False
        else:
            delete_opt = True
        return render(request, 'post.html', {'user': user, 'post': post, 'people': people, 'delete_opt': delete_opt, 'notifications': get_notifications(), 'notif_num': get_notif_num()})

@login_required(login_url='login')
def report(request):
    if request.method=='GET':
        pid = request.GET.get('pid')
        post = Posts.objects.get(post_id=pid)
        post.delete()
        return redirect('dash')


def getPosts(user):
    global user_posts
    user_posts = Posts.objects.filter(username=user)

@login_required(login_url='login')
def editForm(request):
    user = getUser()
    if user is None:
        return render(request, 'login.html', {'action': 'loginU', 'msg': ''})
    global notifications
    return render(request, 'edit_profile.html', {'user': user, 'notifications': get_notifications(), 'notif_num': get_notif_num()})

@login_required(login_url='login')
def edit(request):
    user = getUser()
    if user is None:
        return render(request, 'login.html', {'action': 'loginU', 'msg': ''})
    if request.method=='POST':
        about = request.POST.get('about')
        try:
            dp = request.FILES.get('pp')
            user.profile_pic = dp
        except AttributeError:
            pass
        user.about = about
        user.save()
        return redirect('profile')

@login_required(login_url='login')
def create(request):
    global notifications
    user = getUser()
    if user is None:
        return render(request, 'login.html', {'action': 'loginU', 'msg': ''})
    return render(request, 'create_post.html', {'notifications': get_notifications(), 'notif_num': get_notif_num(), 'user': user})

@login_required(login_url='login')
def create_post(request):
    if request.method=='POST':
        image = request.FILES.get('image')
        user = getUser()
        if user is None:
            return render(request, 'login.html', {'action': 'loginU', 'msg': ''})

        post = Posts(username=user, image=image)
        post.save()
        identifyUsers(post)

        #usernames = getUsers(post.image.url)
        #post_people = [post, [User.objects.get(username=un) for un in usernames]]

        if post_people != []:
            for person in post_people[1]:
                PostPeople(post_id=post_people[0], username=person).save()
        return redirect('profile')


@login_required(login_url='login')
def likePost(request):
    user = getUser()
    if user is None:
        return render(request, 'login.html', {'action': 'loginU', 'msg': ''})
    if request.method=='GET':
        pid = request.GET.get('pid')
        post = Posts.objects.get(post_id=pid)

        try:
            obj = LikedBy.objects.get(post_id=post, user=user)
            post.likes-=1
            post.save()
            obj.delete()
        except LikedBy.DoesNotExist:
            post.likes += 1
            post.save()
            like = LikedBy(post_id=post, user=user)
            like.save()
        return redirect('dash')

@login_required(login_url='login')
def delete_post(request):
    if request.method == 'GET':
        pid = request.GET.get('pid')
        post = Posts.objects.get(post_id=pid)
        post.delete()

        return redirect('dash')

def getDash():
    global posts
    user = getUser()
    if user is None:
        return False
    posts = [post for post in Posts.objects.exclude(username=user).order_by('-date_posted')]

@login_required(login_url='login')
def delete_acct(request):
    user = getUser()
    if user is None:
        return render(request, 'login.html', {'action': 'loginU', 'msg': ''})
    logout(request)
    user.is_active = False
    user.delete()
    return render(request, 'login.html', {'action': 'loginU', 'msg': ''})
