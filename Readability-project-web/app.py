
try:
    from flask import Flask, redirect, url_for, session,render_template,request
    from cloudant.client import Cloudant
    from cloudant.error import CloudantException
    from cloudant.result import Result, ResultByKey
    from datetime import timedelta
    import textstat
    from authlib.integrations.flask_client import OAuth
    import json
    import re
    from werkzeug.utils import secure_filename
    from werkzeug import secure_filename
    import time
    from flask_mysqldb import MySQL
    import random
    from datetime import date,datetime
    import urllib
    import hashlib
    import os
except Exception as e:
    print("Some Modules are Missing : {} ".format(e))


# App config
app = Flask(__name__)

# ====================Change me  =======================================
global client_id
global client_secret
global client

client = Cloudant.iam("e9a1474d-2a68-4b11-b60c-a60c87c061a9-bluemix","oUFFwB9qB-SghbaQbaj7y7TSu7N4yS3mWrDdyYHxtjJn",connect=True)
client.connect()

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
    textarea1=""
    print(flag,user,email)
    if(flag==True):
        flag2=1
    else:
        flag2=0
    return render_template("index2.html", flag=flag, user=user,msg1=0,flag2=flag2,textarea1=textarea1)

@app.route('/test',methods=["POST","GET"])
def test():
    if request.method=="POST":
        flag,user,email = isLoggedIN()
        print(flag,user,email)
        return render_template("test.html", flag=flag, user=user,msg1=0)


#================================History==========================================================================================================

@app.route('/history2/<dateurl>',methods=["POST","GET"])
def histroy2(dateurl):
    msg=""
    if "datar" in client:
        db = client["datar"]
    else:
        db = client.create_database("datar")

    result = Result(db.all_docs, include_docs=True)
    # print(result,list(result))

    for i in list(result):
        if i['doc']['dateurl']==dateurl:
            i1=i['doc']
    print(i1)
    return render_template("history3.html",flag=1,alldata=i1['scores'],input=i1['text_iput_before'],input1=i1['text_iput_after'])





@app.route('/history1/<email11>',methods=["POST","GET"])
def histroy1(email11):
    msg=""

    if "datar" in client:
        db = client["datar"]
    else:
        db = client.create_database("datar")

    result = Result(db.all_docs, include_docs=True)
    # print(result,list(result))
    dates=[]
    dupdate=[]
    for i in list(result):
        if i['doc']['email']==email11 and  i['doc']['date'] not in dates:
            dates.append(i['doc']['date'])
            dupdate.append(i['doc']['dateurl'])
    
    print(dupdate)

   
    return render_template("history1.html",flag=1,dates=dates,dupdate=dupdate,length1=range(len(dates)))




@app.route('/history',methods=["POST","GET"])
def histroy():
    flag,user,email = isLoggedIN()
    msg=""
    if "datar" in client:
        db = client["datar"]
    else:
        db = client.create_database("datar")

    result = Result(db.all_docs, include_docs=True)
    emails=[]
    for i in list(result):
        if i['doc']['email'] not in emails:
            emails.append(i['doc']['email'])
    
    print(emails)

    return render_template("history.html",flag=1,emails=emails)

#========================main================================================================================================================
@app.route('/main1',methods=['POST','GET'])
def index():
    flag,user,email = isLoggedIN()
    textarea1=""
    if flag==True:
        flag2=1
    else:
        flag2=0
    list11=[]
    if request.method=='POST' and flag:
        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        d2 = datetime.now().strftime("%H:%M:%S")

        d11 = today.strftime("%d_%m_%Y")
        d22 = datetime.now().strftime("%H_%M_%S")
        pattern = r">[\w_ ,-.:'\"&;]+<"

        test_data = request.form["text_value"]
        list3=re.findall(pattern,test_data)
        list4=[]
        for i in list3:
            list4.append(i.strip("><"))
        print(list3)
        string_data=" ".join(list4)


        list11=[
        textstat.text_standard(string_data),
        textstat.automated_readability_index(string_data),
        textstat.coleman_liau_index(string_data),

        textstat.crawford(string_data),
        textstat.dale_chall_readability_score(string_data),
        textstat.difficult_words(string_data),

        textstat.fernandez_huerta(string_data),
        textstat.flesch_kincaid_grade(string_data),
        textstat.flesch_reading_ease(string_data),

        textstat.gunning_fog(string_data),
        textstat.gutierrez_polini(string_data),
        textstat.linsear_write_formula(string_data),

        textstat.smog_index(string_data),
        textstat.szigriszt_pazos(string_data)     
        ]
        pattern = r">[\w_ ,-.:'\"&;]+<"
        h1 = r"<h1.*>[\w_ ,-.:'\"?].+</h1>"
        h2 = r"<h2.*>[\w_ ,-.:;'\"?</>]+[^</h2>.+]</h2>"
        h3 = r"<h3.*>[\w_ ,-.:'\"?].+[^</h3>.+]</h3>"
        h4 = r"<h4.*>[\w_ ,-.:'\"?].+[^</h4>.+]</h4>"
        h5 = r"<h5.*>[\w_ ,-.:'\"?].+[^</h5>.+]</h5>"
        h6 = r"<h6.*>[\w_ ,-.:'\"?].+[^</h6>.+]</h6>"
        h7 = r"<h7.*>[\w_ ,-.:'\"?].+[^</h7>.+]</h7>"
        p = r"<p.*>[\w_ ,-.:'\"?].+[^</p>.+]</p>"
        list1=test_data.split("<")
        list2=[]
        for i in list1:
            if(i !=""):
                if i[0:2] in ["h1","h2","h3","h4","h5","h6","h7"]:
                    i=i.replace(i[i.index('>'):],'><span style="background-color: rgb(77, 255, 0);"><font color="#cc3333"'+i[i.index('>'):]+'</span></font>')              
            list2.append(i)

        textarea1 = '<'.join(list2)
        print(textarea1)

        if "datar" in client:
            db = client["datar"]
        else:
            db = client.create_database("datar")

        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        d2 = datetime.now().strftime("%H:%M:%S")

        d11 = today.strftime("%d_%m_%Y")
        d22 = datetime.now().strftime("%H_%M_%S")
        
        input_data = {"email":email,
                "text_iput_before":str(test_data),
                "text_iput_after":str(textarea1),
                "scores":list11,
                "date":d1+" "+d2,
                "dateurl":d11+d22
            }
        print(input_data)
        db.create_document(input_data)
    return render_template("index2.html",msg1=list11,flag=flag, user=user,flag2=flag2,textarea1=textarea1)

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

    # cursor = mysql.connection.cursor()
    # cursor.execute('insert into upload (email , time , text_input) values (?,?,?)',[user,datetime,text1])
    # response = cursor.fetchall()

    return redirect(url_for(ref[index1]))

@app.route('/home')
def home():
    return redirect('/')

#=============================admin=========================================================================================================

@app.route('/admin')
def admin():
    return render_template("admin.html")


@app.route('/adminh3/<dateurl>',methods=["POST","GET"])
def adminh3(dateurl):
    msg=""
    if "datar" in client:
        db = client["datar"]
    else:
        db = client.create_database("datar")

    result = Result(db.all_docs, include_docs=True)
    for i in list(result):
        if i['doc']['dateurl']==dateurl:
            i1=i['doc']
    print(i1)
    
    return render_template("admin1.html",flag=1,alldata=i1['scores'],input=i1['text_iput_before'],input1=i1['text_iput_after'])


@app.route('/adminh2/<email11>',methods=["POST","GET"])
def adminh2(email11):
    msg=""

    if "datar" in client:
        db = client["datar"]
    else:
        db = client.create_database("datar")

    result = Result(db.all_docs, include_docs=True)
    # print(result,list(result))
    dates=[]
    dupdate=[]
    for i in list(result):
        if i['doc']['email']==email11 and  i['doc']['date'] not in dates:
            dates.append(i['doc']['date'])
            dupdate.append(i['doc']['dateurl'])

    return render_template("adminh2.html",flag=1,dates=dates,dupdate=dupdate,length1=range(len(dates)))


@app.route('/admin11',methods=["POST","GET"])
def admin11():
    msg=""
    emails=[]
    try:
        if "datar" in client:
            db = client["datar"]
        else:
            db = client.create_database("datar")
        result = Result(db.all_docs, include_docs=True)
        for i in list(result):
            if i['doc']['email'] not in emails:
                emails.append(i['doc']['email'])
    except:
        msgs = "An Exception Occured"
        return render_template("admin.html",msgs=msgs)
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
                if "data" in client:
                    db = client["datar"]
                else:
                    db = client.create_database("datar")
                result = Result(db.all_docs, include_docs=True)
                # print(result,list(result))
                emails=[]
                for i in list(result):
                    if i['doc']['email'] not in emails:
                        emails.append(i['doc']['email'])
            except:
                # print("exception")
                msgs = "An Exception Occured"
                return render_template("admin.html",msgs=msgs)
        else:
            msgs="Wrong Credentials"
            print(msgs)
            return render_template("admin.html",msgs=msgs)
    return render_template("adminh.html",flag=1,emails=emails)


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
    return render_template("admin1.html",flag=1,alldata=newlist,length1=range(len(newlist[0][1])))

port = int(os.getenv('PORT', 8080))

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=port, debug=True)

if __name__ == "__main__":
    app.run(debug=True)