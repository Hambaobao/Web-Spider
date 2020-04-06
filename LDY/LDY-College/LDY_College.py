'''
/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * *
 * Copyright (C) 
 *              Author : Hambaobao (Email : jameszhang2880@gmal.com)
 *              Time : 2020 - 04 - 05 Sunday                 
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * *
 *                       LDY College Corparation Sign Up File
 *                       
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * *
*           This File Can Only Be Used For Study and Discussion
*           Prohibited For Commercial Use        
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * */
'''

from selenium import webdriver
from PIL import Image
import urllib.request
import tesserocr
import time
import re

Max_Cycle = 20
UpBound = 1

Login_url    = "http://api.zhijing888.com/Login/?"
GetPhone_url = "http://api.zhijing888.com/GetPhone/?"
GetMsg_url   = "http://api.zhijing888.com/GetMsg/?"
ItemID = "50211"

global Usrname
global Password
global Med_code

global Driver
global Phone_Number
global Token
global Graphic_Code
global Text_Graphic_Code
global Sms_Code


def Login():
    global Token
    global Usrname
    global Password

#    url = "http://api.zhijing888.com/Login/?username=" \
#          + Usrname + "&password=" + Password 

    url = Login_url + "username=" + Usrname + \
        "&password=" + Password 

    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req)
    web_content = resp.read().decode('utf-8')

    content_s = web_content.split('|')

    Token = content_s[1]
    balance = content_s[2]

    if content_s[0] != '1':
        print("Response Error\n")
        return

    print("Balance = " + balance + " ¥")

def Get_Phone_number():
    global Token
    global Phone_Number
    global GetPhone_url

#    url = "http://api.zhijing888.com/GetPhone/?id=" + ItemID \
#          + "&token=" + Token + "&loop=1"

    url = GetPhone_url + "id=" + ItemID + "&token=" \
        + Token + "&loop=1"

    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req)
    web_content = resp.read().decode('utf-8')
    content_s = web_content.split('|')
    
    if(content_s[0] != '1'):
        print("Get Phone Number Error")
        return -1

    Phone_Number = content_s[1]   
    print("Phone NUmber = " + str(Phone_Number))

def Get_Verification_Code():
    global Phone_Number
    global Token
    global Sms_Code

    url = "http://api.zhijing888.com/GetMsg/?id=" + ItemID \
          + "&phone=" + Phone_Number + "&token=" + Token \
          + "&dev=ldycollege"

    url = GetMsg_url + "id=" + ItemID + "&phone=" + Phone_Number \
          + "&token=" + Token + "&dev=ldycollege"

    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req)
    web_content = resp.read().decode('utf-8')
    content_s = web_content.split('|')

    if(content_s[0] != '1'):
        print("Get Verification Code Error")
        print("Sms_Code = " + content_s[1])
        Sms_Code = "-1"
        return

    print(content_s[1])
    Sms_Code = ""
    index = 15
    while(content_s[1][index] != ':'):
        index = index + 1;
    index = index + 1
    while(content_s[1][index] != ','):
        Sms_Code  = Sms_Code + content_s[1][index]
        index = index + 1
    print("Sms_Code = " + Sms_Code + '\n')


def Web_commit():
    global Driver
    global Phone_Number
    global Text_Graphic_Code

    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    Driver = webdriver.Chrome(options=option)

#    Driver = webdriver.Chrome()

    Driver.get('http://m.ldygo.com/app/newUser/phoneVoucher.html?\
               pageFor=extension&source=market-287&medCode=med-6322')

    Driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[3]\
                    /div[2]/div[1]/input').send_keys(Phone_Number)

    gcode_url = Driver.find_element_by_xpath('//*[@id="app"]/div[1]\
                    /div[3]/div[2]/div[2]/span/img').get_attribute('src')

    Graphic_Code = urllib.request.urlopen(gcode_url).read()
    with open('Graphic_Code.png', 'wb') as f:
        f.write(Graphic_Code)

    image = Image.open("Graphic_Code.png")

    img2tex = tesserocr.image_to_text(image)
    if(len(img2tex) != 5):
        print("Image to Text Error")
        return -1
    
    Text_Graphic_Code = img2tex[0:4]
    print("Text_Graphic_Code = " + Text_Graphic_Code)


def Web_Sign_Up():
    global Driver
    global Text_Graphic_Code
    global Sms_Code

    Driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[3]\
                    /div[2]/div[2]/input').send_keys(Text_Graphic_Code)

    Driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[3]\
                    /div[2]/div[3]/span[1]').click()

    time.sleep(20)

    Get_Verification_Code();
    if(len(Sms_Code) != 6):
        return -1

    Driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[3]\
                    /div[2]/div[3]/input').send_keys(Sms_Code)

    Driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[3]\
                    /div[2]/div[4]/a').click()
    
    Driver.quit()
    
    return 0


def Get_Usr_Info():
    global Usrname
    global Password
    global UpBound
    global Max_Cycle
    global Med_code

    Usrname = str(input("Please Input Your Account: "))
    Password = str(input("Please Input Your Password: "))
    Med_code = str(input("Please Input Your Med_code (Example: med-6322): "))
    bound = int(input("Please Input Amount You Need (Max %d per time): " %(Max_Cycle)))

    if(bound > Max_Cycle):
        UpBound = Max_Cycle
    else:
        UpBound = bound

    print("Start Automatically Sign Up (Total %d times)" %(UpBound))
    print("----------------------------------------------------------\n")

if __name__ == "__main__":
    global Driver
    global Phone_Number
    global Token

    Get_Usr_Info()

    # Login
    Login()

    Success_Count = 0
    Cycle_Count = 0
    while(Success_Count < UpBound):
        Cycle_Count = Cycle_Count + 1       
        print("Now Successed %d Times, Trying %dth Times" %(Success_Count, Cycle_Count))

        # Get Phone Number
        if(Get_Phone_number() == -1):
            Driver.quit()
            time.sleep(5)
            continue

        # Commit to Get SMS Verification Code
        if(Web_commit() == -1):
            Driver.quit()
            continue
            
        # Using SMS Verification Code & Phone Number to Sign Up
        if(Web_Sign_Up() == 0):
            Success_Count = Success_Count + 1
    
    print("Now Successed %d Times, Totally Tried %d Times" %(Success_Count, Cycle_Count))
    print("Thanks for Using")