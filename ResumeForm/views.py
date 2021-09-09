from os import name
from django.shortcuts import render
from .models import Profile
from django.conf import settings
from django.core.mail import EmailMessage
import smtplib
from email.message import EmailMessage
import imghdr
from PIL import Image, ImageDraw, ImageFont
import textwrap
import re

# Create your views here.
def accept(request):
    if request.method=="POST":
        first_name = request.POST.get("fname", "")
        last_name = request.POST.get("lname", "")
        dob = request.POST.get("dob", "")
        phone = request.POST.get("phone", "")
        email = request.POST.get("email", "")
        address = request.POST.get("address", "")
        linkedin = request.POST.get("linkedin", "")
        objective = request.POST.get("objective", "")
        ssc = request.POST.get("ssc", "")
        ssc_univ = request.POST.get("sscu", "")
        hsc = request.POST.get("hsc", "")
        hsc_univ = request.POST.get("hscu", "")
        grad = request.POST.get("grad", "")
        gradp = request.POST.get("gradp", "")
        grad_univ = request.POST.get("gradu", "")
        #postgrad = request.POST.get("postgrad", "")
        #postgrad_univ = request.POST.get("postgrad_univ", "")
        exp = request.POST.get("expr", "")
        skills = request.POST.get("skills", "")
        projects = request.POST.get("proj", "")

        profile = Profile(first_name=first_name, last_name=last_name, dob=dob, phone=phone, email=email, address=address, linkedin=linkedin, objective=objective, ssc=ssc, ssc_univ=ssc_univ, hsc=hsc, hsc_univ=hsc_univ, grad=grad, gradp=gradp, grad_univ=grad_univ, exp=exp, skills=skills, projects=projects)
        profile.save()

        #Resume Building
        global template_loc, tmp, img_h, name, emailID
        name = first_name
        emailID = email

        template_loc = "images/ResumeSite.jpg"
        tmp = Image.open(template_loc)  # Cft = Certificate
        linedrw = ImageDraw.Draw(tmp)
        s_size = 15
        m_size = 22

         # Drawing Name 
        xCrnt, yCrnt = drawtext(first_name + " " + last_name, 50, 35, 41, 30, (255, 255, 255), path="fonts/Righteous-Regular.ttf")

         # Drawing Contacts 478 176 ----------------------------------------------
        font = ImageFont.truetype('arial.ttf', s_size)
        img_h = font.getsize('I')[1]
        xCrnt = 478
        yCrnt = 180
        drawimg('images/email1.png',480,yCrnt)
        xCrnt, yCrnt = drawtext(email, s_size, 25, 510, yCrnt+2, (0, 0, 0))

        drawimg('images/phone1.png', 480, yCrnt+10)
        xCrnt, yCrnt = drawtext(phone, s_size, 25, 510, yCrnt+12, (0, 0, 0))

        drawimg('images/maps1.png', 480, yCrnt + 17)
        xCrnt, yCrnt = drawtext(address, s_size, 25, 510, yCrnt+12, (0, 0, 0)) #(53, 63, 88)

        drawimg('images/linkedin1.png', 480, yCrnt + 13)
        xCrnt, yCrnt = drawtext(linkedin, s_size, 25, 510, yCrnt+12, (0, 0, 0))

        # Drawing skills
        xCrnt, yCrnt = drawtext("SKILLS", m_size, 20, 490, yCrnt + 20, (0, 0, 0))
        linedrw.line([(xCrnt, yCrnt+10), (xCrnt+50, yCrnt+10)], fill=(97, 115, 159))
        yCrnt += 5
        temp = re.split(",",skills)
        for i in temp:
            xCrnt, yCrnt = drawtext(i, s_size, 25, 490, yCrnt + 8, (0, 0, 0))

         # Drawing Education
        xCrnt, yCrnt = drawtext("EDUCATION", m_size, 20, 490, yCrnt + 20, (0, 0, 0))
        linedrw.line([(xCrnt, yCrnt + 10), (xCrnt + 50, yCrnt + 10)], fill=(97, 115, 159))
        yCrnt += 8
        xCrnt, yCrnt = drawtext("SSC", s_size + 3, 20, 490, yCrnt + 18, (0, 0, 0))
        xCrnt, yCrnt = drawtext(ssc + " / " + ssc_univ, s_size, 25, 490, yCrnt + 5, (0, 0, 0))
        xCrnt, yCrnt = drawtext("HSC", s_size + 3, 20, 490, yCrnt + 18, (0, 0, 0))
        xCrnt, yCrnt = drawtext(hsc + " / " + hsc_univ, s_size, 25, 490, yCrnt + 5, (0, 0, 0))

        # Drawing Projects
        yCrnt += 5
        xCrnt, yCrnt = drawtext("PROJECTS", m_size, 25, xCrnt, yCrnt + 20, (0, 0, 0))
        linedrw.line([(xCrnt, yCrnt + 10), (xCrnt + 50, yCrnt + 10)], fill=(97, 115, 159))
        awards = re.split("\*", projects)
        for i in range(0, len(awards)):
            xCrnt, yCrnt = drawtext(awards[i], s_size, 30, xCrnt, yCrnt + 8, (0, 0, 0))

        # Drawing Objective
        xCrnt = 41
        yCrnt = 180
        xCrnt, yCrnt = drawtext("OBJECTIVE", m_size, 25, xCrnt, yCrnt, (0, 0, 0))
        linedrw.line([(xCrnt, yCrnt + 10), (xCrnt + 50, yCrnt + 10)], fill=(97, 115, 159))
        xCrnt, yCrnt = drawtext(objective, s_size, 60, xCrnt, yCrnt + 20, (0, 0, 0))

        # Drawing Experience
        xCrnt, yCrnt = drawtext("EXPERIENCE", m_size, 25, xCrnt, yCrnt + 20, (0, 0, 0))
        linedrw.line([(xCrnt, yCrnt + 10), (xCrnt + 50, yCrnt + 10)], fill=(97, 115, 159))
        experience = re.split("\#|\*", exp)

        for i in range(0, len(experience)):
            xCrnt = 41
            t = 15
            if i == 0:
                t = 25
            if (i % 2) != 0:  # Even
                if i == len(experience)-1:
                    xCrnt, yCrnt = drawtext(experience[i], s_size + 4, 50, xCrnt, yCrnt + t, (0, 0, 0), 1)
                else:
                    xCrnt, yCrnt = drawtext(experience[i], s_size + 4, 50, xCrnt, yCrnt + t, (0, 0, 0))
            else:
                if i == len(experience)-1:
                    xCrnt, yCrnt = drawtext(experience[i], s_size, 50, xCrnt, yCrnt + 6, (0, 0, 0), 1)
                else:
                    xCrnt, yCrnt = drawtext(experience[i], s_size, 50, xCrnt, yCrnt + 6, (0, 0, 0))

        return render(request, "./file_sent.html")

    return render(request, "accept_details.html")

def drawimg(loc1, x, y):
    img = Image.open(loc1).resize((img_h + 8, img_h + 8)).convert("L")
    tmp.paste(img, (x, y))

def drawtext(text,size,nwords,x,y, fontcolor, print=0,path='arial.ttf'):

    # --------------------- Making the Resume ---------------------
    # Wrapping the text
    draw = ImageDraw.Draw(tmp)
    font = ImageFont.truetype(path, size)
    lines = textwrap.wrap(text, nwords)

    for line in lines:
        w, h = font.getsize(line)
        draw.text(xy=(x, y), text=line, fill=fontcolor, font=font)
        y = y + h + 6

    if print:
        tmp.show()
        tmp.save('user_resume/Resume_' + str(name.replace(" ", "")) + '.pdf')

        #  Variable Initialization
        filename = 'user_resume/Resume_' + str(name.replace(" ", "")) + '.pdf'
        gmail_id = settings.EMAIL_HOST_USER
        gmail_subject = 'Resume: By Karan Chavan'
        gmail_content = """
Hello <name>, 

It's wonderful that you chose this service to make your resume. 
Good luck for your interview.
        
Regards,
Karan K. Chavan
"""

        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()  # Traffic encryption
        s.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

        msg = EmailMessage()
        msg['Subject'] = gmail_subject
        msg['From'] = gmail_id
        msg['To'] = emailID
        gmail_content = gmail_content.replace("<name>", name)
        msg.set_content(gmail_content)

        # Attaching the Poster
        f = open(filename, 'rb')
        fdata = f.read()
        # fname = 'images/' + CertificateFileName
        fname = 'Resume_' + str(name.replace(" ", "")) + '.pdf'

        file_type = imghdr.what(f.name)
        msg.add_attachment(fdata, maintype='application', subtype='octet-stream', filename=fname)
        s.send_message(msg)
        s.quit()

    return x, y

