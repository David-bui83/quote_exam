from django.shortcuts import render, HttpResponse, redirect
from apps.quote.models import User, Quote
from django.contrib import messages
import bcrypt

# Method to render index.html
def index(request):
  return render(request, 'quote/index.html')

# Method to process registration
def registor(request):
  
  # Registration fields validation
  errors = User.objects.registor_validation(request.POST)
  print(errors)
  if len(errors) > 0:
    for key, val in errors.items():
      messages.error(request, val)
    return redirect('/')
  else:
    hashed_pw = bcrypt.hashpw(request.POST['pw'].encode(),bcrypt.gensalt())
    new_user = User.objects.create(name=request.POST['name'],alias=request.POST['alias'],email=request.POST['email'],password=hashed_pw,dob=request.POST['dob'])

    success = User.objects.last()
    request.session['user_id'] = success.id
    return redirect('/quotes')

# Login check for email and password
def login(request):

  try:
    User.objects.get(email=request.POST['l_email'])
  except:
    messages.error(request, 'Invalid user')
    return redirect('/')
  user_pw = User.objects.get(email=request.POST['l_email'])
  if bcrypt.checkpw(request.POST['l_pw'].encode(), user_pw.password.encode()):
    request.session['user_id'] = user_pw.id 
    return redirect('/quotes')
  else:
    messages.error(request, 'Incorrect password')
    return redirect('/')

def quotes(request):

  if not 'user_id' in request.session:
    return redirect('/')

  else:
    user = User.objects.get(id=request.session['user_id'])
    fav_quotes= Quote.objects.filter(fav=request.session['user_id'])
    not_favs= Quote.objects.exclude(fav=request.session['user_id'])
    
    context = {
      'user': user,
      'favs': fav_quotes,
      'not_favs': not_favs
    }
    return render(request, 'quote/quotes.html', context)

def create_quote(request):
  if not 'user_id' in request.session:
    return redirect('/')
  
  errors = Quote.objects.quote_validator(request.POST)
  print(errors)
  if len(errors) > 0:
    for key, val in errors.items():
      messages.error(request, val)
    return redirect('/quotes')
  else:
    user = User.objects.get(id=request.session['user_id'])
    new_quote = Quote.objects.create(quote=request.POST['quote'],message=request.POST['message'],creator=user)
    
    new_quote.fav.add(user)
    print(new_quote)
  return redirect('/quotes')

def users_view(request, id):
  if not 'user_id' in request.session:
    return redirect('/')

  creator = User.objects.get(id=id)

  quotes = Quote.objects.filter(creator=creator.id)
  context = {
    'quotes': quotes,
    'count': quotes.count(),
    'creator': creator
  }
  return render(request, 'quote/view.html', context)

def add(request, id):
  if not 'user_id' in request.session:
    return redirect('/')
    
  user = User.objects.get(id=request.session['user_id'])
  quote = Quote.objects.get(id=id)
  quote.fav.add(user)
  return redirect('/quotes')

def remove(request, id):
  if not 'user_id' in request.session:
    return redirect('/')
  quote = Quote.objects.get(id=id)
  quote.fav.remove(User.objects.get(id=request.session['user_id']))
  return redirect('/quotes')

def logout(request):
  del request.session['user_id']
  return redirect('/')

