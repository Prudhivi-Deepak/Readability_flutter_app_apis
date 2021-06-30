
try:
    from flask import Flask, redirect, url_for, session,render_template,request
    from datetime import timedelta
    import textstat
    from authlib.integrations.flask_client import OAuth
    import json
    from werkzeug.utils import secure_filename
    from werkzeug import secure_filename
    import time
    import os
    from flask_mysqldb import MySQL
    import random
    from datetime import date,datetime
    import urllib
    import hashlib
except Exception as e:
    print("Some Modules are Missing : {} ".format(e))


# App config
app = Flask(__name__)

# ====================Change me  =======================================
global client_id
global client_secret

client_id = "778520672114-0nnem7bqng6l8u0o1vs08onno2k8hngd.apps.googleusercontent.com"
client_secret = "v8kyQb4VhO5ZqMFAfsctwjF4"

# Session config
app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)
app.secret_key = os.urandom(24)
app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = 'iQnG3ACqz9'
app.config['MYSQL_PASSWORD'] = 'OQbU3JbFVB'
app.config['MYSQL_DB'] = 'iQnG3ACqz9'
mysql = MySQL(app)
# ======================================================================


# oAuth Setup
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=client_id,
    client_secret=client_secret,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'},
)


def isLoggedIN():
    try:
        user = dict(session).get('profile', None)
        if user:
            return True, user.get("name"),user.get("email")
        else:
            return False,{},{}
    except Exception as e:
        return False,{},{}

@app.route('/login')
def login():
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
    user_info = resp.json()
    user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
    print(user_info)
    session['profile'] = user_info
    session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
    return redirect('/')


@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')


@app.route('/')
def hello_world():
    flag,user,email = isLoggedIN()
    print(flag,user,email)
    return render_template("Index1.html", flag=flag, user=user,msg1=0)


#================================History==========================================================================================================

@app.route('/history2/<dateurl>',methods=["POST","GET"])
def histroy2(dateurl):
    msg=""
    cursor1 = mysql.connection.cursor()
    res11 = cursor1.execute("SELECT * FROM predict1 WHERE time2 = %s",[dateurl])
    alldata = cursor1.fetchall()
    if(len(alldata)==0):
        return  render_template("admin1.html",flag=0,msg=str(date)+" Date Haven't used Our website")
    list1=[]

    print("---------------------------------------------------------------------------------------------------------")
    print(alldata[0][5:])
    return render_template("history3.html",flag=1,alldata=alldata[0][5:],input=alldata[0][4])




@app.route('/history1/<email11>',methods=["POST","GET"])
def histroy1(email11):
    msg=""
    cursor1 = mysql.connection.cursor()
    res11 = cursor1.execute("SELECT * FROM predict1 WHERE email = %s",[email11])
    alldata = cursor1.fetchall()
    print(alldata)
    if(len(alldata)==0):
        return  render_template("admin1.html",flag=0,msg=str(session["email"])+" Email Address Haven't used Our website for  image")
    dates=[]
    dupdate=[]
    list1=[]
    for i in alldata:
        if(i[1] not in dates):
            dates.append(i[1])
            dupdate.append(i[2])
        print(i)
    print(dates)
    # print(alldata[0][0],alldata[0][1],alldata[0][2],alldata[0][3],alldata[0][4])#id , email , input , output1 , output2 , info.
    return render_template("history1.html",flag=1,dates=dates,dupdate=dupdate,length1=range(len(dates)))




@app.route('/history',methods=["POST","GET"])
def histroy():
    flag,user,email = isLoggedIN()
    print(email)
    msg=""
    cursor1 = mysql.connection.cursor()
    res1 = cursor1.execute('SELECT * FROM predict1 WHERE email = %s',[email])
    print(res1)
    alldata = cursor1.fetchall()
    print(alldata)
    if(len(alldata)==0):
        return  render_template("admin1.html",flag=0,msg=str(email)+" Email Address Haven't used Our website for  image")
    emails=[]
    mysql.connection.commit()
    for i in alldata:
        if i[3] not in emails:
            emails.append(i[3])
    print(emails)
    return render_template("history.html",flag=1,emails=emails)

#========================main================================================================================================================
@app.route('/main1',methods=['POST','GET'])
def index():
    flag,user,email = isLoggedIN()
    list1=[]
    if request.method=='POST' and flag:
        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        d2 = datetime.now().strftime("%H:%M:%S")

        d11 = today.strftime("%d_%m_%Y")
        d22 = datetime.now().strftime("%H_%M_%S")


        test_data = request.form["text_value"]
        list1=[
        textstat.text_standard(test_data),
        textstat.automated_readability_index(test_data),
        textstat.coleman_liau_index(test_data),

        textstat.crawford(test_data),
        textstat.dale_chall_readability_score(test_data),
        textstat.difficult_words(test_data),

        textstat.fernandez_huerta(test_data),
        textstat.flesch_kincaid_grade(test_data),
        textstat.flesch_reading_ease(test_data),

        textstat.gunning_fog(test_data),
        textstat.gutierrez_polini(test_data),
        textstat.linsear_write_formula(test_data),

        textstat.smog_index(test_data),
        textstat.szigriszt_pazos(test_data)     
        ]

        print(test_data,list1,d1+" "+d2,d11+d22)    
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO predict1 VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',[d1+" "+d2,d11+d22,email,test_data,list1[0],list1[1],list1[2],list1[3],list1[4],list1[5],list1[6],list1[7],list1[8],list1[9]
        ,list1[10],list1[11],list1[12],list1[13]])
        mysql.connection.commit()
    return render_template("Index1.html",msg1=list1,flag=flag, user=user)

@app.route('/towards/<name>',methods=['POST','GET'])
def main1(name):
    list2 = []
    print(name)
    flag,user,email = isLoggedIN()
    names = ["id", "time","email","text_input","text_standard","automated_readability_index", "coleman_liau_index","crawford", 
                        "dale_chall_readability_score", "difficult_words", "fernandez_huerta", 
                        "flesch_kincaid_grade", "flesch_reading_ease", "gunning_fog", 
                        "gutierrez_polini", "linsear_write_formula", "smog_index", 
                        "szigriszt_pazos"]
    print(names.index(name))   
    index1 = names.index(name) 
    textinfo = ["This is the id of the input","This is the todays date","","","Based upon all the Other tests, returns the estimated school grade level required to understand the text"
                          ,"The automated readability index is a readability test designed to measure the how easy your text is to understand."
                            ,"Coleman and Liau developed the formula to automatically calculate writing samples instead of manually coding the text."
                            ,"Returns an estimate of the years of schooling required to understand the text. The text is only valid for elementary school level texts."
                            ,"Different from other tests, since it uses a lookup table of the most commonly used 3000 English words. Thus it returns the grade level using the New Dale-Chall Formula."
                            ,"Difficult words are found by using all other metrics calculated."
                            ,"The Huerta score* was an adaptation of the Flesch Reading Ease score intoSpanish. The Flesch formula for English text, first published in 1948, is : Flesch = 206.835 - 84.6 * syllables/words - 1.015 * words/sentences"
                            ,"Returns the Flesch-Kincaid Grade of the given text. This is a grade formula in that a score of 9.3 means that a ninth grader would be able to read the document."
                            ,"The Flesch Reading Ease Formula is a simple approach to assess the grade-level of the reader."
                            ,"The index estimates the years of formal education a person needs to understand the text on the first reading."
                            ,"","The result is a grade level measure, reflecting the estimated years of education needed to read the text fluently."
                            ,"The SMOG grade is a measure of readability that estimates the years of education needed to understand a piece of writing. "
                            ];
  
    formulas =  ["","","","",""
                          ,"Automated Readability Index formula: 4.71 x (characters/words) + 0.5 x (words/sentences) - 21.43."
                            ,"Coleman Liau Index formula: 5.89 x (characters/words) - 0.3 x (sentences/words) – 15.8."
                            ,"A = -0.205OP+0.049SP - 3.407. A is the number of years of schooling; OP , the number of sentences per hundred words; SP , the number of syllables per hundred words. The result is rounded to the nearest tenth."
                            ,"The formula for calculating the raw score of the Dale–Chall readability score (1948) is =0.1579((difficultwords/words)100)+0.0496(words/sentences)"
                            ,"It may check in the library of commomly used words it Has . "
                            ,"The Huerta formula is usually presented as 206.84 - (0.60 * P) - (1.02 *F), where P = number of syllables and F = number of sentences, as countedin a sample containing 100 words"
                            ,"Flesch-Kincaid grade level formula: 0.39 x (words/sentences) + 11.8 x (syllables/words) - 15.59."
                            ," RE = 206.835 – (1.015 x ASL) – (84.6 x ASW) RE = Readability Ease ASL = Average Sentence Length (i.e., the number of words divided by the number of sentences)ASW = Average number of syllables per word (i.e., the number of syllables divided by the number of words)"
                            ,"Gunning fog index = 0.4[(words/sentences)+100(complex words/eords)]"
                            ,"","For each easy word, defined as words with 2 syllables or less, add 1 point.For each hard word, defined as words with 3 syllables or more, add 3 points.Divide the points by the number of sentences in the 100-word sample.Adjust the provisional result r : If r > 20, Lw = r / 2.If r ≤ 20, Lw = r / 2 - 1"
                            ,"Grade=1.0430[sqrt((number of polysyllables)(30/number of sentences))]+3.1291"
                            ]
    ref =  ["","","","",""
                          ,"https://www.webfx.com/tools/read-able/automated-readability-index.html"
                            ,"https://www.webfx.com/tools/read-able/coleman-liau-index.html"
                            ,"https://legible.es/blog/formula-de-crawford/"
                            ,"https://en.wikipedia.org/wiki/Dale%E2%80%93Chall_readability_formula"
                            ,""
                            ,"https://linguistlist.org/issues/22/22-2332/"
                            ,"https://www.webfx.com/tools/read-able/flesch-kincaid.html"
                            ,"https://readabilityformulas.com/flesch-reading-ease-readability-formula.php"
                            ,"https://en.wikipedia.org/wiki/Gunning_fog_index"
                            ,"","https://en.wikipedia.org/wiki/Linsear_Write"
                            ,"https://en.wikipedia.org/wiki/SMOG"
                            ]

    images =  ["","","","",""
                          ,"ARI.png"
                            ,"CLI.png"
                            ,"cra.png"
                            ,"dale.png"
                            ,""
                            ,"hue.png"
                            ,"fleasch.png"
                            ,"fleash.png"
                            ,"gun.png"
                            ,"","linear.png"
                            ,"smog.png"
                            ]; 
    print(str([names[names.index(name)],textinfo[index1],formulas[index1],ref[index1],images[index1]]))
    cursor = mysql.connection.cursor()
    cursor.execute('insert into upload (email , time , text_input) values (?,?,?)',[user,datetime,text1])
    response = cursor.fetchall()

    return redirect(url_for(ref[index1]))

@app.route('/home')
def home():
    return redirect('/')

#=============================canvas=========================================================================================================

@app.route('/admin')
def admin():
    return render_template("admin.html")


@app.route('/adminh3/<dateurl>',methods=["POST","GET"])
def adminh3(dateurl):
    msg=""
    cursor1 = mysql.connection.cursor()
    res1 = cursor1.execute('SELECT * FROM predict1 WHERE time2 = %s',[dateurl])
    alldata = cursor1.fetchall()
    if(len(alldata)==0):
        return  render_template("admin1.html",flag=0,msg=str(date)+" Date Haven't used Our website")
    newlist=[]
    dates=[]
    list1=[]
    return render_template("admin1.html",flag=1,alldata=alldata[0][5:],input=alldata[0][4])



@app.route('/adminh2/<email11>',methods=["POST","GET"])
def adminh2(email11):
    msg=""
    cursor1 = mysql.connection.cursor()
    res1 = cursor1.execute('SELECT * FROM predict1 WHERE email = %s',[email11])
    alldata = cursor1.fetchall()
    if(len(alldata)==0):
        return  render_template("admin1.html",flag=0,msg=str(session["email"])+" Email Address Haven't used Our website for  image")
    dates=[]
    dupdate=[]
    list1=[]
    for i in alldata:
        if(i[1] not in dates):
            dates.append(i[1])
            dupdate.append(i[2])
        print(i)
    print(dates)
    # print(alldata[0][0],alldata[0][1],alldata[0][2],alldata[0][3],alldata[0][4])#id , email , input , output1 , output2 , info.
    return render_template("adminh2.html",flag=1,dates=dates,dupdate=dupdate,length1=range(len(dates)))


@app.route('/admin11',methods=["POST","GET"])
def admin11():
    msg=""
    try:
        cursor1 = mysql.connection.cursor()
        res1 = cursor1.execute('SELECT * FROM predict1')
        alldata = cursor1.fetchall()
        list1=[]
        emails=[]
        print("---------------------------------------------------------------------------------------------------------")
    except:
        # print("exception")
        msgs = "An Exception Occured"
        return render_template("admin.html",msgs=msgs)
    emails=[]
    mysql.connection.commit()
    for i in alldata:
        if i[3] not in emails:
            emails.append(i[3])
    print(emails)
    return render_template("adminh.html",flag=1,emails=emails)





@app.route('/admin1',methods=["POST","GET"])
def admin1():
    msg=""
    newlist=[]
    if request.method == 'POST':
        email1=request.form['email']
        pass1=request.form['password']
        if(str(email1)=="root@gmail.com" and str(pass1)=="root"):
            try:
                cursor1 = mysql.connection.cursor()
                res1 = cursor1.execute('SELECT * FROM predict1')
                alldata = cursor1.fetchall()
                list1=[]
                emails=[]
            except:
                # print("exception")
                msgs = "An Exception Occured"
                return render_template("admin.html",msgs=msgs)
        else:
            msgs="Wrong Credentials"
            print(msgs)
            return render_template("admin.html",msgs=msgs)
        emails=[]
    mysql.connection.commit()
    for i in alldata:
        if i[3] not in emails:
            emails.append(i[3])
    print(emails)
    return render_template("adminh.html",flag=1,emails=emails)

@app.route('/admin2',methods=["POST","GET"])
def admin2():
    return render_template("admin1.html",flag=0)


@app.route('/admin22',methods=["POST","GET"])
def admin22():
    msg=""
    if request.method == 'POST':
        email1=request.form['email']
        engine = create_engine('sqlite:///database2.db',echo=True)
        conn  =engine.connect()
        res11 = conn.execute("SELECT * FROM data WHERE email =?",(str(email1)))
        alldata = res11.fetchall()
        if(len(alldata)==0):
            return  render_template("admin1.html",flag=0,msg=str(email1)+" Email Address Haven't used Our website for  image")
        newlist=[]
        list1=[]
        for data1 in range(len(alldata)):
            print(list(alldata[data1][5].split(",")))
            list1.append( list(alldata[data1][5].split(",")) )
        for i1,i2 in zip(alldata,list1):
            print("---------------------------------------------",i2[0][3:-3])
            print("---------------------------------------------",i2[1][3:-3])
            print("---------------------------------------------",i2[2][3:-3])
            print("---------------------------------------------",i2[3][3:-3])
            print("---------------------------------------------",i2[4][3:-3])
            print("---------------------------------------------",i2[5][3:-3])
            i2[0]=i2[0][3:-3]
            i2[1]=i2[1][3:-3]
            i2[2]=i2[2][3:-3]
            i2[3]=i2[3][3:-3]
            i2[4]=i2[4][3:-3]
            i2[5]=i2[5][3:-3]

            newlist.append([i1,i2])
        print("---------------------------------------------------------------------------------------------------------")
        for i in newlist:
            print(i)
        # print(alldata[0][0],alldata[0][1],alldata[0][2],alldata[0][3],alldata[0][4])#id , email , input , output1 , output2 , info.
    return render_template("admin1.html",flag=1,alldata=newlist,length1=range(len(newlist[0][1])))


@app.route('/admin3',methods=["POST","GET"])
def admin3():
    msg=""
    engine = create_engine('sqlite:///database2.db',echo=True)
    conn  =engine.connect()
    res11 = conn.execute("SELECT * FROM data")
    alldata = res11.fetchall()
    if(len(alldata)==0):
        return  render_template("admin1.html",flag=0,msg=" Email Address Haven't used Our website for  image")
    newlist=[]
    list1=[]
    for data1 in range(len(alldata)):
        print(list(alldata[data1][5].split(",")))
        list1.append( list(alldata[data1][5].split(",")) )
    for i1,i2 in zip(alldata,list1):
        print("---------------------------------------------",i2[0][3:-3])
        print("---------------------------------------------",i2[1][3:-3])
        print("---------------------------------------------",i2[2][3:-3])
        print("---------------------------------------------",i2[3][3:-3])
        print("---------------------------------------------",i2[4][3:-3])
        print("---------------------------------------------",i2[5][3:-3])
        i2[0]=i2[0][3:-3]
        i2[1]=i2[1][3:-3]
        i2[2]=i2[2][3:-3]
        i2[3]=i2[3][3:-3]
        i2[4]=i2[4][3:-3]
        i2[5]=i2[5][3:-3]

        newlist.append([i1,i2])
    # print("---------------------------------------------------------------------------------------------------------")

    # print(alldata[0][0],alldata[0][1],alldata[0][2],alldata[0][3],alldata[0][4])#id , email , input , output1 , output2 , info.
    return render_template("admin1.html",flag=1,alldata=newlist,length1=range(len(newlist[0][1])))

port = int(os.getenv('PORT', 8080))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)

# if __name__ == "__main__":
#     app.run(debug=True)