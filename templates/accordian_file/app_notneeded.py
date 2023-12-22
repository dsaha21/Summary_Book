#import requests
import sys,datetime,re

from flask import Flask, render_template, url_for, request, jsonify, session, redirect
from flask import request as req
from pdfreader import pdfread
from transformers import pipeline
import json
import gdown
from db import DataBaseFunction
#from time import TimeFunction

#if lenght = 0 register page else login page
#check in login if normal user or admin

app = Flask(__name__)
app.secret_key = 'your_secret_key'
summarizer = pipeline("summarization", model="t5-base")
global data_count,inputuser
db = DataBaseFunction()
#timings = TimeFunction()
listnames=None
thenames=[]; page_summdic = None
usertype = ""
totalsummary_withlink = ""
nametime = {}
theUN=None
theMAIL=None
logintime = None
logouttime = None
usernamesforadmins = None
pw_alert=None

@app.route("/")
def Index():
    global db,listnames,mainusertype,usertype,thepage, theurl, totalsummary_withlink, page_summdic, thenames

    # Create a table
    db.create_table()
    db.time_table()
    db.create_blockedusers()
    rowsfromdb = db.rowsofcol(column_name="name")
    #print("the rows are-->", rowsfromdb,"=====",type(rowsfromdb))

    #rowlen = len(rowsfromdb)
    #print("ROW LENGTH------------",rowlen,"last value===========", rowsfromdb[rowlen-1])
    listnames = rowsfromdb

    return render_template('login.html')

    # db.close_connection()

#=================================================================

#summary of page dict
def page_dic_cal(txtlist, n1, n2):
    page_dic = {}
    pages = []
    if (n1 == None and n2 == None):
        k = 1

        for pageinfo in txtlist:
            page_dic[k] = txtlist[k-1]
            k+=1
    else:
        k=n1

        for k in range(n1,n2+1):
            page_dic[k] = txtlist[k-1]
            k+=1
            
    return page_dic

# return summary page_dic
def page_summdic_cal(txtlist, n1, n2):
    each_summary = {}

    if (n1 == None and n2 == None):
        k = 1
        for pageinfo in txtlist:
            # if k==10:
            #     break
            each_summary[k] = (summarizer(pageinfo, max_length=100, min_length=5, do_sample=False,
                                               truncation=True)[0]['summary_text'])
            print("**********page " + str(k) + " summerized *************")
            k += 1
    else:
        k=n1
        for k in range(n1,n2+1):
            # if k==10:
            #     break
            each_summary[k] = (summarizer(txtlist[k], max_length=100, min_length=5, do_sample=False,
                                               truncation=True)[0]['summary_text'])
            print("**********page " + str(k) + " summerized *************")
            k += 1


    return each_summary

def calculate_total_time(start_time, end_time):
    duration = end_time - start_time
    total_seconds = duration.total_seconds()
    total_minutes = total_seconds / 60.0
    return str(total_minutes)


def is_numeric_string(string):
    # Pattern to match only numerical values
    pattern = r'^\d+$'

    # Check if the string matches the pattern
    if re.match(pattern, string):
        return True
    else:
        return False

# #====================================================================================

#https://drive.google.com/file/d/1Wp6t-OIqWSfEulG8-JY2Nx50yMSEkn_j/view
#https://drive.google.com/file/d/1LOpw_xUcrT4y6jMmj73XA2yqFE68jKLP/view?usp=share_link
#https://drive.google.com/file/d/1kYbfLEFLYKlEWbO_RC2B0bz8oRM7mjz7/view
#https://drive.google.com/file/d/1-20T3_jvcXGD9BKDC-guxnosSAflpl-u/view?usp=sharing

#===========================================================
#======================================================================================
@app.template_filter('zip_lists')
def zip_lists(lst1, lst2, lst3, lst4):
    return zip(lst1, lst2, lst3, lst4)

@app.route("/tohome", methods=["POST","GET"])
def tohome():
    global theUN,theMAIL,usertype,listnames
    print("calling the tohome")

    rowsfromdb = db.rowsofcol(column_name="name")
    listnames = rowsfromdb

    #read and check the name inputed in the last database -->along with radio button user check
    inputuser = request.form.get('USER')
    inputpass = request.form.get('PASS')

    # if inputuser in listnames:
    #     if db.passcheck(uname=inputuser) != inputpass:
    #         return render_template('login.html', error_message="Please enter valid Pass")
    if is_numeric_string(inputpass):
        return render_template('login.html', error_message = "Please enter valid Pass")

    #usertypefromdb = db.rowsofusertype(row_name=inputuser)

    # if inputuser == None:
    if not (inputuser and inputpass):
        return render_template('login.html', error_message = "Please enter valid credentials")

    ifblocked = db.whether_blocked(uname=inputuser)
    if ifblocked:
        return render_template('login.html', error_message=f"THE USER {inputuser} is blocked. PLEASE LOGIN WITH OTHERS")

    file =""
    selected_option = request.form.get('option')
    print("selected user ....-->", selected_option)

    #please check in the admin table

    for name in listnames:
        thenames.append(name[0])
    print("listnames -------", thenames)

    theUN = inputuser
    alertmsg =""
    if selected_option == 'admin':

        usertype = db.get_the_usertype(uname=theUN)
        if (inputuser in thenames) and (usertype=="A"):
            file = "adminhome.html"
            usertype = "A"
        else:
            file = "showforadmin.html"

    elif (selected_option == 'user') and (inputuser in thenames): #return redirect(url_for('admin_page'))
        usertype = db.get_the_usertype(uname=theUN)
        if (usertype =="U"):
            file = "home.html"
            theMAIL = db.get_mail_tabledata(uname=theUN)
            #print("Messi cannot enter ...wrong block")
        else:
            file = "login.html"
            alertmsg = "YOU ARE AN ADMIN CANT LOGIN AS USER"
            #print("Correct block")
    else:
        file = "register.html"
        usertype = "U"


    return render_template(file, error_message=alertmsg, dbnames = db.get_users_timetable(), dbmails=db.get_mails_timetable(), dbtimes=db.get_times_timetable(), dbstats= db.get_statuses_timetable())
#===============================================================================
@app.route("/foradmin", methods = ["POST"])
def foradmin():

    return render_template('showforadmin.html', error_message = "YOU CANNOT REGISTER AS AN ADMIN")

# @app.route("/adminpage", methods = ["POST"])
# def adminpage():
#
#     return render_template('adminhome.html', error_message = "YOU CANNOT REGISTER AS AN ADMIN")


@app.route("/toregister", methods=["POST"])
def toregister():
    #checking user/ admin
    global theMAIL
    regname = str(request.form.get('NAME'))
    regmail = str(request.form.get('MAIL'))
    regpass = str(request.form.get('PASS'))

    if regname and regmail and regpass:
        db.insert_data(regname, regmail, regpass, "U")
        theMAIL=regmail

    else:
        return render_template('login.html', error_message = "Please enter valid credentials")





    return render_template("login.html")
#====================================================================================

def extract_value_from_json(json_data, key):
    print('\n\n\n\n\n\n\n\n------------------------>',type(json_data))
    print("\n\n\n\n\n\n\n\n------------------------>THE JASON DICT ---->", json_data,"===",key)

    val = json.dumps(json_data[0][0])
    json_object = val.replace("'", "\"")
    #print("############ ", json_object,"#########")
    #json_final = json.loads(json_object)
    #value = json.loads(json_data[0][0])


    # print('\n\n\n\n\n\n\n\n------------------------>')
    # print('------------>',json_object,"---->", type(json_object))
    # Access value by key
    # val2 = json_object
    # print('------------>', (val2))

    return json_object



@app.route('/api/retrive', methods=['GET','POST'])
def get_data():
    onlypvals =""
    if request.method == 'GET':
        # if (thepage and theurl) == None:
        pagenumber = request.args.get('pagenumber')  # Retrieve the value of the 'pagenumber' query parameter
        print("The page nos...----->#",pagenumber, "#---", type(pagenumber))
        bookID = request.args.get('bookID')
        expanData = db.fetchbook(page_no= pagenumber, book_url=bookID)
        expanData_wholecontent = db.fetchbook_wholedict(book_url=bookID)#<for the whole content dict>)

        thepage=pagenumber
        theurl=bookID


        finaldic_summ = json.loads(str(expanData))
        finaldic_whole = json.loads(str(expanData_wholecontent))
        # for i in finaldic:
        #     onlypvals=onlypvals + finaldic[i] + "\n"
        print("FIRST PLEASE SEEE ====================", finaldic_summ,"=======",type(finaldic_summ))
        output = finaldic_summ[pagenumber]
        print("THE OUTPUT TYPE.........", output, "------",type(output))
        #data = extract_value_from_json(expanData, pagenumber) #dictionarydata
        #print("\n\n\n\n\n\n\n\n============FIRST PLEASE SEEE ====================",data,"=====",type(data))


        # Example response
        response = {
            'pagenumber': pagenumber,
            'message': bookID,
            'data': output
        }
        # print(type(data))
        #thedict = json.loads(data)#newdict = {k: v.replace('\n', '') for k, v in thedict.items()}

        print('\n\n\n\n\n\n\n\n------------------------>','RENDER TO NEW')
        #print("THE OUTPUT", output[:10])
        #return render_template("fulltextdisplay.html", finaltext= output)
        return render_template("test.html", pn = finaldic_summ[pagenumber], popped= finaldic_whole[pagenumber])# finaltext= output)




@app.route('/blocked_users/<string:name>', methods=['GET'])
def blocked_users(name):
    print("blocked is clicked ...",name)
    status = db.fetch_status_timetable(uname=name)
    #set status
    print("The status...", status)
    if status == "UB":
        db.set_status_timetable(blocked=True,uname=name)
        return render_template("showforadmin.html", cs=f"THE user {name} is BLOCKED")
    else:
        return render_template("showforadmin.html", msg= "ALREADY BLOCKED")

@app.route('/unblocked_users/<string:name>', methods=['GET'])
def unblocked_users(name):
    print("Unblocked is clicked ")
    status = db.fetch_status_timetable(uname=name)
    # set status
    print("The status...", status)
    if status == "B":
        db.set_status_timetable(blocked=False, uname=name)
        return render_template("showforadmin.html", cs=f"THE user {name} is UNBLOCKED")
    else:
        return render_template("showforadmin.html", msg="ALREADY UNBLOCKED")

#for the logout button

@app.route("/adminlogout", methods=['POST'])
def adminlogout():
    session.clear()
    return redirect('/')

@app.route('/logout', methods=['POST'])
def logout():
    # if c==1:
    #     session.clear()
    #     return redirect('/')

    #print("To the back page...")
    logouttime = datetime.datetime.now()
    tt = calculate_total_time(logintime, logouttime)
    presentname = db.whether_name_timetable(uname=theUN)
    if presentname:
        db.update_time_timetable(uname=theUN,newtime=tt)
    else:
        db.time_input(theUN, theMAIL, tt, "UB")

    # Clear the session to log the user out
    session.clear()

    # Redirect the user to the first page
    return redirect('/')


@app.route("/Summarize_fold", methods=["GET","POST"])
def Summarize_fold():
    return render_template('summary_fold.html') 

@app.route("/Summarize", methods=["GET","POST"])
def Summarize():
    totalsummary = ""
    global logintime,logouttime
    # new_tab_url = "http://127.0.0.1:5010/Summarize_fold"
    
    db.booktable()
    ## test code # print(request.form)
    if request.method == 'POST':

        # result = request.values.get('name')
        # print('result is ', result)
        # #get 1st no. range -->
        # n1 = int(request.values.get("N1")) #(request.form["N1"])
        # print(f"1st no...{n1}")  #
        # n2 = int(request.values.get("N2"))
        # print(f"2nd no...{n2}")

        n1 = request.values.get("N1")
        if_n1 = is_numeric_string(n1)
        if(if_n1 == True):
            n1 = int(n1)
        else:
            n1 = None
        #print("The value of n1...", type(n1))


        n2 = request.values.get("N2")
        if_n2 = is_numeric_string(n2)
        if (if_n2 == True):
            n2 = int(n2)

        else:
            n2 = None
        #print("The value of n2...", type(n2))

        result = request.values.get('name')



        if (if_n1==True and if_n2==True):
            if(n1 <= 0 or n2 <= 0):
                return render_template('home.html', error_message="Please enter valid credentials")

        link = result.split("/")
        print(link[5])
        url = 'https://drive.google.com/uc?id={}'.format(link[5])
        output = 'book.pdf'
        print("----Starting download -----")
        gdown.download(url, output, quiet=False)
        txtlist = pdfread("book.pdf")
        print(f"Get no. of pages...{len(txtlist)}")
        print("len of txtlist",len(txtlist))
        # print("----- End of 1 part ..next each page summary----")

        # summarizer = pipeline("summarization", model="t5-base")
        article_summary = {}
        if (n1==None and n2==None):
            key = 1
        else:
            key = n1  # 0
        total_para = []
        article_summary_links={}


        if theUN in nametime:
            logintime = db.fetch_time(userid= theUN)#nametime[theUN]
        else:
            logintime = datetime.datetime.now()

        totalpages_book = len(txtlist)
        print("TOTAL PAGES ...",totalpages_book)
        page_dic = page_dic_cal(txtlist, n1, n2)
        # insert to db here, with respect to book name and page number
        db.booktable()
        page_summdic = page_summdic_cal(txtlist, n1, n2)


        # for page in range(n1, n2 + 1):  # range(len(txtlist))
        #     print(page, "------", page_dic[page], "-------", page_summdic[page])


        # converting to json object and to db
        json_data_summ = json.dumps(page_summdic)  # -->for the wholecontent of pages
        json_data_whole = json.dumps(page_dic)

        db.bookinput(url, json_data_summ, json_data_whole, theUN, None)
        for page in page_summdic.values():
            # hyperlink = '<a href="/processKey" onclick="processKey(\'' + str(key) + '\')">' + page + '</a>' target="_blank"
            #passing the json data whole to the 3d fold.html
            totalsummary = totalsummary + page + '<a target="_blank" href ="' + '/api/retrive?pagenumber=' + str(key) + '&&bookID=' + url + '">' + str(key) + '</a>\n'

            key += 1

        totalsummary_withlink = totalsummary

        response_data = {
            # 'totalsummary': totalsummary,
            'summary': page_summdic,
            'whole': page_dic,
            
            'thelength':len(page_summdic)
        }

        return jsonify(response_data)

        # else:
        #     #for the new name entry in the timetable database
        #     logintime = datetime.datetime.now()
        #     page_dic = page_dic_cal(txtlist, n1, n2)
        #     # insert to db here, with respect to book name and page number
        #
        #     page_summdic = page_summdic_cal(txtlist, n1, n2)
        #
        #     #for time
        #     #if(nametime == theUN):
        #         #<present so perform normal task >
        #     #else:
        #         #add to the dict for a new name
        #     for page in range(n1, n2+1):  # range(len(txtlist))
        #         print(page, "------", page_dic[page], "-------", page_summdic[page])
        #         # print_dict(page_dic, page_summdic, len(txtlist))
        #
        #
        #     #converting to json object and to db
        #     json_data_summ = json.dumps(page_summdic) #-->for the wholecontent of pages
        #     json_data_whole = json.dumps(page_dic)
        #
        #     db.bookinput(url, json_data_summ, json_data_whole, theUN, None) #-->content table
        #     for page in page_summdic.values() :
        #         #hyperlink = '<a href="/processKey" onclick="processKey(\'' + str(key) + '\')">' + page + '</a>' target="_blank"
        #         totalsummary = totalsummary + page + '<a target="_blank" href ="' +'/api/retrive?pagenumber='+str(key) +'&&bookID='+url+ '">' + str(key) + '</a>\n'
        #
        #         #totalsummary = totalsummary + page + '<div class="popup" onclick="myFunction()"> <b>'+str(key)+'</b><span class="popuptext" id="myPopup">'+page_dic[key]+'</span>''</div>'
        #         #totalsummary = totalsummary + page + '<button type="button" class="btn btn-primary" data-toggle="modal" data-target="#exampleModalLong">'+str(key)+'</button>\n'
        #
        #         key+=1
        #
        #     totalsummary_withlink = totalsummary
        #
        #     return jsonify(totalsummary)


if __name__ == '__main__':
    #db work
   app.run(debug = True,
           host='0.0.0.0',
           port=5010,
           threaded=True)
