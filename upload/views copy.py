from django.shortcuts import render, HttpResponse
from .forms import LogForm
import os
from DjangoLogReader.settings import MEDIA_ROOT
from datetime import datetime
from apachelogs import LogParser
from .models import Log
from django.core.paginator import Paginator
from django.http import StreamingHttpResponse
from django.http import JsonResponse



parser = LogParser("%h - - %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"")
def met_http(log_line):
    http = ['GET', 'POST', 'UPDATE', 'DELETE']
    for m in http:
        if m in str(log_line):
            return m

def _count_generator(reader):
    b = reader(1024 * 1024)
    while b:
        yield b
        b = reader(1024 * 1024)

def line_counter(file):
    with open(file, 'rb') as fp:
        c_generator = _count_generator(fp.raw.read)
        # count each \n
        count = sum(buffer.count(b'\n') for buffer in c_generator)
        print('Total lines:', count + 1)
    return count




def Home(request):
    if request.method == 'POST':
        form = LogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = LogForm()
    context = {
        'form' : form,
    }
    return render(request, 'home.html', context)


def listLogsView(request):
    logfilelist = os.listdir("media/logs/")
    context = {
        "filelist" : logfilelist,
    }
    return render(request, 'list.html', context)

def filterInputView(request, name):
    context = {
        "filename" : name,
    }
    return render(request, 'filterInput.html', context)


def get_log_data(file_path, start):
    with open(file_path, "r") as file:
        for i in range(start):
            next(file)
        while True:
            yield file.readline()

def stream_log_file(request, name):
    log = Log.objects.get(file="logs/"+name)
    log_path = log.file.path

    data_chunk = get_log_data(log_path, request.session['start'])
    counter = request.session['counter']
    criterias = request.session['criterias']

    filtered_data = ""

    while counter:
        line = next(data_chunk)
        try:
            log_entry = parser.parse(line)
        except: pass
        row = [
            getattr(log_entry, 'remote_host', '-'), 
            str(datetime.date(getattr(log_entry, 'request_time', '-'))),
            met_http(getattr(log_entry, 'request_line', '-')),
            getattr(log_entry, 'final_status', '-')
        ]
        if request.session['date']:
            my_date = datetime.strptime(request.session['date'], '%Y-%m-%d')
            log_date = datetime.strptime(row[1], '%Y-%m-%d')
            if my_date < log_date:
                print("Koniec")
                request.session['start'] = line_counter(log_path)
                break
        if all(criteria in row for criteria in criterias):
            filtered_data += line
            counter -= 1
        request.session['start'] += 1

    return StreamingHttpResponse(filtered_data, content_type='text/html')

def dynamic_loading_page(request, name):
    request.session.clear()
    criterias = []
    if request.POST.get('ip'):
        criterias.append(request.POST.get('ip'))
    if request.POST.get('date'):
        criterias.append(request.POST.get('date'))
    if request.POST.get('method'):
        criterias.append(request.POST.get('method'))
    if request.POST.get('code'):
        criterias.append(int(request.POST.get('code')))

    request.session['criterias'] = criterias
    request.session['counter'] = 100
    request.session['start'] = 0
    request.session['date'] = request.POST.get('date')
    
    context = {
        "name" : name,
    }
    return render(request, 'filtered.html', context)


def deleteLog(request, name):
    log = Log.objects.get(file="logs/"+name)
    log.file.delete()
    log.delete()

    logfilelist = os.listdir("media/logs/")
    context = {
        "filelist" : logfilelist,
    }

    return render(request, 'list.html', context)
