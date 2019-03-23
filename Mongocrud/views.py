from django.shortcuts import render , redirect,render_to_response
from pymongo import MongoClient, TEXT
from django.http import HttpResponse
from djongo import cursor
import hashlib
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

def getTable():
    client = MongoClient()
    db = client.schooldb
    tbl = db.stddetails
    return tbl




def home(request):
    #return HttpResponse(request.session['username'])
    if 'username' in request.session:
        client = MongoClient()
        db = client.schooldb
        col = db.stddetails
        #results = ('firstname','lastname')
        searchText=request.POST.get('searchText')
        if (request.method =="POST" and searchText!=''):
            # a = db.stddetails.list_indexes()
            # return HttpResponse(a)
            
            # a= col.find({
            #          'firstname':{
            #                         '$regex' : '/^'+searchText+'/'    #search in single field
            #                     }
            #             })
           # --------------------------------------------------------------------------------------------
            #db.stddetails.create_index([ ('firstname',TEXT),('lastname',TEXT)],name='text')
            
            # a= col.find({
            #          '$text':{
            #                         '$search' : searchText    #search in index created for multiple fields
            #                     }
            #             })
            a = col.find({'$or':[{'firstname':{'$regex':searchText}},{'lastname':{'$regex':searchText}}]}) # search in multiple fields
            #return HttpResponse(a)
            return render(request,'home.html',context={'records' : a})
        client = MongoClient()
        db = client.schooldb
        col = db.stddetails
        records = col.find()
        # paginator = Paginator(records, 2)
        # page = request.GET.get('page')
        context ={
            'records' : records #paginator.get_page(page)         
        }
        return render(request,'home.html',context)
    return redirect('login')

def djex(request):
    sql = cursor()
    print(sql)

def login(request):
    context = {'emsg':''}
    if request.method =='POST':
        uname = request.POST.get('username')
        passwd = request.POST.get('password')
        if (uname=="" or passwd==""):
            context = {
            'emsg' : 'Username or Password is empty'
            }
        else:
            tbl = getTable()
            res = tbl.find_one(
                {
                'username':uname
                },
                {
                'password':1
                })
            #return HttpResponse(uname +' ' + passwd)
            if(res ==None or res==""):
                context = {
                'emsg' : 'User with ' + uname + ' username not found'
                }
                #request.session['username'] = uname
            else:
                if hashlib.md5(passwd.encode()).digest() == res['password']:
                    request.session['username'] = uname
                    return redirect('home')
                else:
                    context = {
                    'emsg' : 'Invalid credentials! Please login with correct details'
                    }

        return render(request,'login.html',context)
    if 'username' in request.session:
         return redirect('home')
    return render(request,'login.html',context)

def logout(request):
    request.session.flush()
    return redirect('login')

def logo(request):
    return HttpResponse('hi')