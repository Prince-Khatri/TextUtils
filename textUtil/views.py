# I have created this file - Prince
from django.http import HttpResponse ,HttpResponseRedirect
from django.shortcuts import render , redirect
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.conf import settings
import re

#---------------------------------------------------------------------------------
# Function for analysis
#---------------------------------------------------------------------------------
def removePuncFun(content):
    punctutation = '''!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~'''

    analyzedText = ''

    for letter in content:
        if letter not in punctutation:
                analyzedText += letter
    params = {'purpose':'Remove Punctutation','analyzedText' : analyzedText, 'counter' : len(content)}

    return params

def capitalizeFun(content):
    analyzedText = ''

    for letter in content:
            analyzedText = analyzedText + letter.upper()


    params = {'purpose':'Capitalizing every Element' , 'analyzedText' : analyzedText, 'counter' : len(content)}

    return params

def newLineRemoverFun(content):
    analyzedText = re.sub('\n|\r|\n\r','',content)

    params = {'purpose':'New Line remover' , 'analyzedText' : analyzedText, 'counter' : len(content)}

    return params

def spaceRemoverFun(content):
    analyzedText = re.sub(' +',' ',content)

    params = {'purpose':'Extra Space remover' , 'analyzedText' : analyzedText, 'counter' : len(content)}

    return params

def inputChecker(listOfCheckBox,content):
    moreThanOne = [var == 'on' for var in listOfCheckBox]
    params= dict()

    if content == '':
        # error due to no content
        params = {'message':'Kindly Enter Some Text to be Analyzed!!!!','error':1}

        return params

    elif moreThanOne.count(True)>1:
        # error due to more than one selection
        params = {'message':'Kindly Select only one of the Features to be implemented!!!!','error':2}

        return params
    
    elif moreThanOne.count(True) == 0:
        # error due to no selection
        params = {'message':'Kindly Select what do you want to do with the TEXT!!!!','error':3}

        return params
    
    else:
        return False

def choiceToParameter(removePunc,capitalize,newLineRemover,spaceRemover,djText):
    # This function selects the cohoice made by the user and then pass the content and choice to respective functions and create the parameters

    if removePunc == 'on':
        params = removePuncFun(djText)
        return params
    
    elif capitalize == 'on':
        params = capitalizeFun(djText)
        return params
        
    elif newLineRemover == 'on':
        params = newLineRemoverFun(djText)
        return params

    elif spaceRemover == 'on':
        params = spaceRemoverFun(djText)
        return params

    else:
        # None type to be sent for html parameters
        return 


#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------




#---------------------------------------------------------------------------------
# Function for Handling Http request

def index(request):

    params = {'message':'Text Utils is ready to go! Enter your text below and let Text Utils do the magic!!!', 'error':0}
    
    return render(request,'index.html',params)

# Main Brain Of this backend
def analyze(request):

    # Text Taken from web
    djText = request.GET.get('text','default')

    # The Button which is turned on
    removePunc = request.GET.get('removePunc','off')
    capitalize = request.GET.get('capitalize','off')
    newLineRemover = request.GET.get('newLineRemover','off')
    spaceRemover = request.GET.get('spaceRemover','off')


    # ---------
    # Createing funciton for more than one checkBox Turned on

    parameters = inputChecker([removePunc,capitalize,newLineRemover,spaceRemover],djText)

    if parameters:
        return render(request,'index.html',parameters)
    
    # ---------

    # parameters returned by the Above Function choiceToParameters
    parameters = choiceToParameter(removePunc,capitalize,newLineRemover,spaceRemover,djText)


    if parameters:
        return render(request,'analyze.html',parameters)


    else:
        return render(request,'analyze.html')

def contactUs(request):
    return render(request,'contactUs.html')

def contactUsData(request):
    # Name Taken from User
    userEmail = request.GET.get('userEmail','default')
    flag = False
    # print(userName,userEmail,userComment,userEmailSubject,'\nSentCopy:',sentMeCopy) all values are coming

    try:
        validate_email(userEmail)
    except ValidationError:
        flag = 1
        params = {'messageSent':flag}
        return render(request,'contactUs.html',params)
    

    
    
    # Rest Data taken from the form
    userName = request.GET.get('userName','default')
    userEmailSubject = request.GET.get('userEmailSubject','default')
    userComment = request.GET.get('userComment','default')
    sentMeCopy = request.GET.get('sentMeCopy','off')

    # Creating the email to be sent

    emailSubject = f'Contact Us: {userEmailSubject} '
    emailContent = f'Name: {userName}\nEmail: {userEmail}\n\nMessage:\n{userComment}'

    send_mail(
        emailSubject,
        emailContent,
        settings.DEFAULT_FROM_EMAIL,
        [settings.DEFAULT_FROM_EMAIL],
        fail_silently = False
    )
    # send_mail(subject,content,from,to,fail_sailently=False)

    if sentMeCopy == 'on' :
        send_mail(
            f'Copy of your Message: {userEmailSubject}',
            emailContent,
            settings.DEFAULT_FROM_EMAIL,
            [userEmail],
            fail_silently = False
        )

    flag = 2
    params = {'messageSent':flag}
    return render(request,'contactUs.html',params)



def aboutUs(request):
     return render(request,'aboutUs.html')


#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------
# For Links to the Contact Us page

def github(request):
    return redirect('https://github.com/Prince-Khatri')

def mail(request):
    return HttpResponse('<script type="text/javascript">'
        'window.location.href="mailto:textutilsbyprince@gmail.com";'
        '</script>')

def linkedin(request):
    return redirect('https://www.linkedin.com/in/princekhatri1013')

def telegram(request):
    return redirect('https://t.me/PrinceKhatri_0_0')

#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------








