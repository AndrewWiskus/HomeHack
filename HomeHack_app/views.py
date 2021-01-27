from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
import bcrypt
from .models import User, ProjectPost, Comment

#ROUTING
def index(request):
    return render(request, "login.html")

def register(request):
    return render(request, "register.html")

def about(request):
    return render(request, "about.html")

def dash(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context={
        'all_projects':ProjectPost.objects.all()
    }
    return render(request, "dash.html", context)

def edit_account(request, user_id):
    context={
        'user':User.objects.get(id=user_id)
    }
    return render(request, 'edit_account.html', context)

def edit_project(request, project_id):
    context={
        'project':ProjectPost.objects.get(id=project_id)
    }
    return render(request, 'edit_project.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')

def project_page(request, project_id):
    context={
        'project':ProjectPost.objects.get(id=project_id)
    }
    return render(request, 'project_page.html', context)

def user_projects(request, user_id):
    context={
        'user':User.objects.get(id=user_id)
    }
    return render(request, 'user_projects.html', context)

def search_projects(request):
    q = request.GET.get('q')
    context={
        'filtered':ProjectPost.objects.filter(
            Q(title=q) |
            Q(content=q)
        ).distinct()
    }
   
    return render(request, "search_projects.html", context)

# CREATE A USER
def register_user(request):
    if request.method=='POST':
        # VALIDATE
        errors=User.objects.validator(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/register')
        # ENCRYPTING PASSWORD
        user_pw=request.POST['pw']
        # HASH PASSWORD
        hash_pw=bcrypt.hashpw(user_pw.encode(), bcrypt.gensalt()).decode()
        new_user=User.objects.create(first_name=request.POST['f_n'], last_name=request.POST['l_n'], email=request.POST['email'], city=request.POST['city'], state=request.POST['state'], password=hash_pw)
        print(new_user)
        request.session['user_id']=new_user.id
        request.session['user_name']=f"{new_user.first_name} {new_user.last_name}"

        return redirect('/dash')
    return redirect('/register')

# LOG IN
def login(request): 
    if request.method=='POST':
        # QUERY
        logged_user=User.objects.filter(email=request.POST['email'])
        if logged_user:
            logged_user=logged_user[0]
            # COMPARE PASSWORDS
            if bcrypt.checkpw(request.POST['pw'].encode(), logged_user.password.encode()):
                request.session['user_id']=logged_user.id
                request.session['user_name']=f"{logged_user.first_name} {logged_user.last_name}"
                return redirect('/dash')
    return redirect('/')

# DASH FUNCTIONALITY
def create_project(request):
    if request.method=='POST':
        errors=ProjectPost.objects.project_validator(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/dash')
            #to do add img
        ProjectPost.objects.create(title=request.POST['title'], content=request.POST['content'], tools=request.POST['tools'], post_image=request.FILES['post_image'], poster=User.objects.get(id=request.session['user_id']))
        return redirect('/dash')
    return redirect('/')

# DESTROY
def delete_project(request, project_id):
    ProjectPost.objects.get(id=project_id).delete()
    return redirect('/dash')

# LIKE
def like(request, user_id, project_id):
    user_account=User.objects.get(id=user_id)
    project=ProjectPost.objects.get(id=project_id)
    context={
        'project':ProjectPost.objects.get(id=project_id)
    }
    project.likes.add(user_account)
    return render(request, "project_page.html", context)

#COMMENTS
def create_comm(request, project_id):
    if request.method=='POST':
        # create comment
        this_user = User.objects.get(id=request.session["user_id"])
        this_project = ProjectPost.objects.get(id=project_id)
        Comment.objects.create(content=request.POST['content'], comment_poster=this_user, message = this_project)
        context={
        'project':ProjectPost.objects.get(id=project_id)
    }
    return render(request, 'project_page.html', context)

def delete_comm(request, comm_id, project_id):
    Comment.objects.get(id=comm_id).delete()
    context={
        'project':ProjectPost.objects.get(id=project_id)
    }
    return render(request, 'project_page.html', context)

# UPDATE USER
def update(request, user_id):
    user_account=User.objects.get(id=user_id)

    # VALIDATE
    errors=User.objects.validator(request.POST)
    if errors:
        for error in errors:
            if user_account.email != request.POST['email'] or (user_account.email == request.POST['email'] and errors[error] != 'duplicate_email'):
                messages.error(request, errors[error])

                context={
                    'user':User.objects.get(id=user_id)
                }
                return render(request, "edit_account.html", context)
            
    user_account.first_name=request.POST['f_n']
    user_account.last_name=request.POST['l_n']
    user_account.email=request.POST['email']
    user_account.city=request.POST['city']
    user_account.state=request.POST['state']
    user_account.save()
    user_account=User.objects.get(id=user_id)
    request.session['user_name']=f"{user_account.first_name} {user_account.last_name}"
    context={
        'user':User.objects.get(id=user_id)
    }
    return render(request, "edit_account.html", context)

# UPDATE PROJECT
def update_project(request, project_id):
    project_account=ProjectPost.objects.get(id=project_id)
    errors=ProjectPost.objects.project_validator(request.POST)
    
    errors=ProjectPost.objects.project_validator(request.POST)
    if errors:
        for error in errors:
            messages.error(request, errors[error])
        return render(request, "edit_project.html")
            
    project_account.title=request.POST['title']
    project_account.content=request.POST['content']
    project_account.tools=request.POST['tools']
    project_account.post_image=request.FILES['post_image']
    project_account.save()
    project_account=ProjectPost.objects.get(id=project_id)
    context={
        'project':ProjectPost.objects.get(id=project_id)
    }
    return render(request, "project_page.html", context)

# SEARCH
def get_project_queryset(request, query=None):
    q = request.GET.get('q')

    context={
        'filtered':ProjectPost.objects.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q) |
            Q(tools__icontains=q)
        ).distinct()
    }
    return render(request, "search_projects.html", context)



