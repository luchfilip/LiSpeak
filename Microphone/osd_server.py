#!/usr/bin/env python

# This script is hacky, maybe it should work using sockets.
# Or dbus, or w/e
# -*- coding: cp1252 -*-
import pynotify, time, os, subprocess,lispeak,urllib2,appindicator,gtk

try:
    os.chdir("Microphone")
except:
    print "Currently in",os.getcwd()
PWD=str(os.getcwd()) # Our full path

def transaText(text):
    text = text.replace("\n",'')
    home = subprocess.Popen("echo $HOME", shell=True, stdout=subprocess.PIPE).communicate()[0].replace('\n','')
    with open(home+"/.lispeak/UserInfo") as f:
        for each in f:
            line = each.replace('\n','')
            if line.startswith("LANG="):
                language = line.replace("LANG=","").replace(" ","")
    try:
        if language == "en":
            return text
    except:
        return text
    else:
        f1 = open("Translations/"+language)
        f = f1.read().decode("utf-8")
        f1.close()
        f=f.split("\n")
        for l in f:
            l = l.replace('\n','')
            if l != "":
                o,n = l.split("=")
                if o == text:
                    return n
    return text


pynotify.init("Speech Recognition")

n = pynotify.Notification(lispeak.translate("LiSpeak Ready"),"")

try:
    os.system("rm pycmd_*")
except:
    pass
try:
    os.remove("result")
except:
    pass
try:
    os.remove("result_image")
except:
    pass

# This line allows palaver to work even if the computer is suspending
# screensavers. Such as when a fullscreen video is playing.
n.set_urgency(pynotify.URGENCY_CRITICAL)

n.show()

updateCount = 50

old = ""

while True:
    if updateCount > 10:
        #os.chdir("../")
        #os.system("./pm")
        #os.system("./update")
        #pid = subprocess.Popen("xprop -id `xdotool getwindowfocus` | grep '_NET_WM_PID' | grep -oE '[[:digit:]]*$'", shell=True, stdout=subprocess.PIPE).communicate()[0].replace('\n','')
        #currentWindow = subprocess.Popen("ps -p "+pid+" -o comm=", shell=True, stdout=subprocess.PIPE).communicate()[0].replace('\n','')
        #if old != currentWindow:
        #    n.update(currentWindow)
        #    n.show()
        #os.chdir("Microphone")
        f = urllib2.urlopen("http://lispeak.bmandesigns.com/functions.php?f=messageUpdate")
        nid,title,text = f.read().split("||")
        lastId = lispeak.getSingleInfo("lastid")
        if lastId == "":
            lastId = nid
        try:
            go = int(nid) > int(lastId)
        except:
            go = True
        if go:
            n.update("LiSpeak - "+title,text,"")
            n.show()
            lispeak.writeSingleInfo("lastid",str(int(lastId)+1))
        updateCount = 0
        #old = currentWindow
    while os.path.exists("silence"):
        sleep(.1)
    i = 0
    while os.path.exists("pycmd_record"):
        os.system("touch in_green")
        if i >=64:
            i = 0
            continue
        if i < 32:
            n.update(lispeak.translate("Listening"),"",PWD+"/Recording/thumbs/rec"+ str((i+1))+".gif")
        if i >= 32:
            n.update(lispeak.translate("Listening"),"",PWD+"/Recording/thumbs/rec"+ str(64-i)+".gif")
        n.show()
        i += 8
        time.sleep(.05)
    i = 0
    while os.path.exists("pycmd_wait"):
        n.update(lispeak.translate("Performing recognition"),"",PWD+"/Waiting/wait-"+str(i)+".png")
        n.show()
        time.sleep(.1)
        i += 1;
        if i > 17:
            i = 0
    i = 0
    while os.path.exists("pycmd_done"):
        os.system("touch in_grey")
        n.update(lispeak.translate("Done"),"","")
        n.show()
        try:
            os.rename("pycmd_done","pycmd_nocmd")
        except:
            pass
    i = 0
    while os.path.exists("pycmd_result"):
        os.system("touch in_grey")
        try:
            f = open("result")
       
            title = lispeak.translate(f.readline())
            image = f.readline()
            
            tmp = f.readline()
            
            body = ""
            while tmp != '':
                body += image
                image = tmp
                tmp = f.readline()
                
            if title == '\n' or title == '':
                title = " "
            if body == '\n' or body == '':
                body = " "
            else:
                if body[-1:] == '\n':
                    body = body[:-1]
            if image == '\n' or image == '':
                image = " "
            else:
                if image[-1:] == '\n':
                    image = image[:-1]
                    
            if os.path.exists("result_image"):
                imf = open("result_image")
                image = imf.read()
                print "IMAGE: ",image.replace("\n","").replace("file://","")
                imf.close()
            
            n.update(title,body,image.replace("\n","").replace("file://",""))
            n.show()
            try:
                os.rename("pycmd_result","pycmd_nocmd")
            except:
                pass
            try:
                os.remove("result")
            except:
                pass
            try:
                os.remove("result_image")
            except:
                print "Can't Delete!"
            if lispeak.getSingleInfo("ESPEAK") == "True":
                os.system("espeak -a 200 \""+title+"\"")
                os.system("espeak -a 200 \""+body+"\"")
        except:
            print "Error Displaying Notification"
    while os.path.exists("pycmd_stop"):
    
        n.update(lispeak.translate("Please wait"),"",PWD+"/Not_Ready/stop.png")
        n.show()
        try:
            os.rename("pycmd_stop","pycmd_nocmd")
        except:
            pass
    time.sleep(.1)
    updateCount = updateCount + 1
