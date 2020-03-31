from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

import os
import multiprocessing
from multiprocessing import Process
# mport time
import random
import string
import docker
import json


def decodeJSONtoArray(str):
    arr = []
    tmp = ""
    start = False
    for c in str:
        if c == '\"' and not start:
            start = True
            continue
        if start:
            if c == '\"':
                start = False
                arr.append(tmp)
                tmp = ""
                continue
            else:
                tmp += c
        if c == ']':
            break
    return arr


def ranstr(num):
    salt = ''.join(random.sample(string.ascii_letters + string.digits, num))
    return salt


def Debug(debugstr):
    with open('debug', 'a+') as f:
        f.write(debugstr+'\n')


def SaveCode(codeList):
    global randomStr, folder_host
    CreateFile = False
    while not CreateFile:
        randomStr = ranstr(7)
        folder_host = '/home/dock/docker/src/' + 'c' + randomStr + '/'
        CreateFile = not os.path.exists(folder_host)
    os.makedirs(folder_host)
    for item in codeList:
        with open(folder_host+item["file"], 'w') as f:
            f.write(item["code"])


def SaveStdin(stdin):
    global filename_stdin
    filename_stdin = folder_host+"stdin"
    with open(filename_stdin, 'w') as f:
        f.write(stdin)


def CreateContainer(language, fileList, exportEXE):
    global client
    client = docker.from_env()
    global container
    folder_docker = '/usr/src/'
    image_name = "ubuntu_" + language
    if exportEXE :
        image_name = 'ubuntu_'+language+'_hi'
    volumes = {}
    for filename in fileList:
        volumes[folder_host +
                filename] = {'bind': folder_docker+filename, 'mode': 'rw'}
    volumes[filename_stdin] = {'bind': folder_docker+"stdin", 'mode': 'rw'}
    container = client.containers.run(
        image_name, init=True, detach=True, tty=True, mem_limit='128m', volumes=volumes)


def Compile(language, fileList):
    global filename_exe
    filename_exe = '/usr/src/c' + randomStr
    if language == "py":
        filename_exe = '/usr/src/'+fileList[0]
        return True
    if language == "java":
        filename_exe = 'Main'
    compile_cmd = 'bash /usr/src/compile ' + filename_exe
    exec_compile = client.api.exec_create(
        container=container.id, cmd=compile_cmd, tty=True)
    result_compile = client.api.exec_start(
        exec_compile, tty=True).decode('UTF-8')
    if result_compile == "":
        return True
    else:
        result['message'] = result_compile
        result['result'] = "Compile failed"
        return False


def RunProcess(q, exec_run):
    result_run = client.api.exec_start(exec_run, tty=True).decode('UTF-8')
    try:
        q.put(result_run, block=False)
    except:
        pass


def Run():
    run_cmd = 'bash /usr/src/run ' + filename_exe
    exec_run = client.api.exec_create(
        container=container.id, cmd=run_cmd, tty=True)
    q = multiprocessing.Queue()
    p = Process(target=RunProcess, args=(q, exec_run,))
    p.start()
    try:
        result_run = q.get(block=True, timeout=60)
    except:
        result['message'] = "Program run timeout"
        result['result'] = "Run timeout"
        p.terminate()
    else:
        result['message'] = result_run
        result['result'] = "success"
    p.join()


def Finish():
    container.kill()
    container.remove()
    os.system("rm -rf "+folder_host)


def readFile(fn, buf_size=262144):
    f = open(fn, "rb")
    while True:  # 循环读取
        c = f.read(buf_size)
        if c:
            yield c
        else:
            break
    f.close()


def Download():
    host_exe = folder_host+'c'+randomStr+'.exe'
    cpcmd = 'docker cp '+container.id+':'+filename_exe+' '+host_exe
    Debug("cpcmd:   "+cpcmd)
    os.system(cpcmd)
    Debug("cp")
    response = HttpResponse(
        readFile(host_exe), content_type='APPLICATION/OCTET-STREAM')
    response['Content-Disposition'] = 'attachment; filename='+'c'+randomStr+'.exe'
    response['Content-Length'] = os.path.getsize(host_exe)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST,GET,OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    Finish()
    return response


def index(request):
    if os.path.exists('debug'):
        os.remove('debug')
    request.encoding = 'utf-8'

    Debug("start encode")
    codeList = []
    fileList = request.POST['fileList']
    Debug("fileList:  " + fileList)
    fileList = json.loads(fileList)
    Debug("fileList:  " + str(fileList))
    for item in fileList:
        codeList.append(dict(file=item, code=request.POST[item]))
    Debug("codeList:  " + str(codeList))
    stdin = request.POST['stdin']
    global language
    language = request.POST['language']
    global result
    result = {'result': '', 'message': ''}
    exportEXE = json.loads(request.POST['exportEXE'])

    SaveCode(codeList)
    SaveStdin(stdin)
    CreateContainer(language, fileList, exportEXE)
    compileResult = Compile(language, fileList)
    if compileResult:
        if not exportEXE:
            Run()
        else:
            return Download()
    Finish()

    response = JsonResponse(result, safe=False)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST,GET,OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response
