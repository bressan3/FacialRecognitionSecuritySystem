import datetime

import os
import subprocess
import sys

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

""" Mailing part """
def send_email(files):

    # Returns the email's password within a file
    def get_password():
        file = open('emailinfo/pswd', 'r')
        password = file.read()
        
        return password

    # Reads a file containing the email address that are gonna be used for both sending and
    # receiving the messages
    def get_emails():
        emails_array = []

        with open('emailinfo/emails', 'r') as file:
            for line in file:
                emails_array.append(line)

        return emails_array

    FROM = get_emails()[0]
    TO = get_emails()[1]

    msg = MIMEMultipart()
    msg['From'] = FROM
    msg['To'] = TO
    msg['Subject'] = "PYTHON EMAIL TEST"

    # filename = "/Users/Lucas/Desktop/ben.jpg"
    for filename in files:
        attachment = open(filename, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(FROM, get_password())
    text = msg.as_string()
    server.sendmail(FROM, TO, text)
    server.quit()

""" Uses face detection to determine if it should or not report via email """
def with_facerec():
    # Infinite loop that keeps checking if there are images in the snapshots folder and recognizing the faces in them
    while True:
        # Number of files in the snapshots directory (check facedetector.py for more info)
        number_of_files = len([name for name in os.listdir('snapshots') if os.path.isfile(name)])
        
        if number_of_files == 0:
            continue

        files_list = []
        match_count = 0

        for i in xrange(1, number_of_files + 1):
            if os.path.exists("snapshots/snapshot"+str(i)+".jpg"):
                p = subprocess.Popen(['python', 'facerec.py', 'identify', 'snapshots/snapshot'+str(i)+'.jpg'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = p.communicate()
               
                files_list.append("snapshots/snapshot"+str(i)+".jpg")
                # print(out)
                # Face recognized
                if out.find('recognized with confidence') > 0:
                    # Finds the subject's name
                    subject_pos = out.find("'") + 1
                    subject_val = str(out[subject_pos: out.find("' ")])
                    # print(out)
                    # Finds the % confidence. Confidence is a distance so, the higher the
                    # confidence, the higher is the probability that the person in the picture
                    # is not a subject
                    confidence_pos = out.find('confidence') + 11
                    confidence_val = float(out[confidence_pos: ])
                    # Only counts as a match is confidence_val is lesser than 45 %
                    if confidence_val <= 45.0:
                        match_count += 1

        all_files_exist = False
        if len(files_list) == number_of_files:
            all_files_exist = True

        # No matches
        if match_count == 0 and all_files_exist:
            print("SENDING EMAIL...")
            send_email(files_list)
            for i in xrange(1, number_of_files + 1):
                # Creates a directory in dmp for the current date if it does not exit
                if not os.path.exists("dmp/"+datetime.datetime.today().strftime("%m-%d-%Y")):
                    os.system("mkdir -p dmp/"+datetime.datetime.today().strftime("%m-%d-%Y"))
                if os.path.exists("snapshots/snapshot"+str(i)+".jpg"):
                    # Changes the snapshots names to the current time and date and move them to the proper folder in dmp
                    new_filename = datetime.datetime.now().strftime('%b %d %Y %H'+"h"+'%M'+"m"+'%S'+"s")+" "+str(i)+".jpg"
                    new_filename = new_filename.replace(" ", "_")
                    os.rename("snapshots/snapshot"+str(i)+".jpg", new_filename)
                    os.system("mv "+new_filename+" dmp/"+datetime.datetime.today().strftime("%m-%d-%Y"))
        # If there are matches, the snapshots will be deleted
        elif match_count > 0 and all_files_exist:
            print("DELETING...")
            for i in xrange(1, number_of_files + 1):
                if os.path.exists("snapshots/snapshot"+str(i)+".jpg"):
                    os.remove("snapshots/snapshot"+str(i)+".jpg")


""" This is is used in case you know no one will be at home (It doesn't use face recognition) """
def without_facerec():
    
    while True:
        # Number of files in the snapshots directory (check facedetector.py for more info)
        number_of_files = len([name for name in os.listdir('snapshots') if os.path.isfile(name)])

        files_list = []

        for i in xrange(1, number_of_files + 1):
            if os.path.exists("snapshots/snapshot"+str(i)+".jpg"):
                files_list.append("snapshots/snapshot"+str(i)+".jpg")
        
        email_sent = False
        all_files_exist = False
        # If all files are in the list, then we can send the email
        if len(files_list) == number_of_files:
            all_files_exist = True
        
        try:
            if all_files_exist:
                print("SENDING EMAIL...")
                send_email(files_list)
                email_sent = True
        except:
            pass

        for i in xrange(1, number_of_files + 1):
            # After sending the email we can safely move all the pictures to the dmp folder
            if os.path.exists("snapshots/snapshot"+str(i)+".jpg") and email_sent:
                os.system("mv snapshots/snapshot"+str(i)+".jpg dmp")

def main(argv):
    # Makes sure that all the needed folders exist
    if not os.path.isdir("dmp"):
        os.makedirs("snapshots")

    if not os.path.isdir("snapshots"):
        os.makedirs("snapshots")

    if not os.path.isdir("emailinfo"):
        os.makedirs("emailinfo")
    if not os.path.isfile("emailinfo/pswd"):
        open("emailinfo/pswd", "r")
    if not os.path.isfile("emailinfo/emails"):
        open("emailinfo/emails", "r")
    
    if os.stat("emailinfo/pswd").st_size == 0 or os.stat("emailinfo/emails").st_size == 0:
        print("ERROR: Please insert the sender's email password on 'emailinfo/pswd' and on 'emailinfo/emails' the sender's email on its first line and the receiver's email on the second.")
        exit(-1)

    # Analyses the parameter and decides which mode should it run on
    if argv[0] == "with_facerec":
        print("FACE RECOGNITION IS ON")
        with_facerec()
    elif argv[0] == "without_facerec":
        print("FACE RECOGNITION IS OFF")
        without_facerec()
    else:
        print("Usage: faceanalyzer [with_facerec | without_facerec]")

if __name__ == "__main__":
    main(sys.argv[1:])
    