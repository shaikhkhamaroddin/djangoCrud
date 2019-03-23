from pymongo import MongoClient
from django.http import HttpResponse
from django.shortcuts import render, render_to_response,redirect
from pymongo.collection import ReturnDocument
import hashlib
from django.core.files.storage import FileSystemStorage



def getTable():
    client = MongoClient()
    db = client.schooldb
    tbl = db.stddetails
    return tbl

def addPage(request):
    context={
        'flag' : 'add',
        'heading' : 'Add New record',
        'posturl':'save',
        'dis':'disabled',
        'spc':None
    }
    return render(request,'mongocrudView.html',context)

def saveRecord(request):
    file = request.FILES.get('fileupload')
    if(file):
        fs = FileSystemStorage(location="images/")
        filename = fs.save(file.name, file)
        uploaded_file_url = fs.url(filename)
  #  return HttpResponse(uploaded_file_url)
    db = getTable()
    cid = db.counters.find_one_and_update({'_id': 'product_id' },{'$inc':{'sequence_value':1}},
      upsert=True,
      #new=True,
      return_document=ReturnDocument.AFTER
    )
    db.save({
        'empid': cid['sequence_value'],
        'firstname' : request.POST.get('firstname'),
        'lastname' :  request.POST.get('lastname'),
        'gender' : request.POST.get('gender'),
        'username' : request.POST.get('username'),
        'password' : hashlib.md5(request.POST.get('password').encode()).digest()
    })

    # context = {
    #     'firstname' : request.POST.get('firstname'),
    # 'lastname' :  request.POST.get('lastname'),
    # 'gender' : request.POST.get('gender')

    # }
    return redirect('home')
    #return render(request,'Record_view.html',context)
    #return render_to_response('Record_view.html')
def updateRecord(request,id=0):
    tbl = getTable()
    if request.method =="POST":
        id=request.POST.get('id')
        a= tbl.find_one_and_update({
            'empid':int(id)},{'$set':{
            'firstname' : request.POST.get('firstname'),
            'lastname' :  request.POST.get('lastname'),
            'username' :  request.POST.get('username'),
            'password' :  hashlib.md5(request.POST.get('password').encode()).digest(),
            'gender' : request.POST.get('gender')}
            })
        #return HttpResponse(a)
        return redirect('home')
    
    a = tbl.find_one({'empid':int(id)})
    context={
        'id':id,
        'flag' : 'update',
        'heading' : 'Update Page',
        'firstname': a['firstname'],
        'lastname' : a['lastname'],
        #'username' : a['username'],
        #'password' : a['password'],
        'gender': a['gender'],
        'posturl' : 'update',
        'spc':None,
        'dis':'disabled'
    }
    return render(request,'mongocrudView.html',context)
def deleteRecord(request,id):
    tbl = getTable()
    tbl.find_one_and_delete({'empid':int(id)})
    return redirect('home')
def viewRecord(request):
    return render_to_response('mongocrudView.html')



