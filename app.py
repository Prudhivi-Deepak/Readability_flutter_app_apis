import textstat
import json
from flask.json import jsonify
from flask import Flask, redirect, url_for, session,render_template,request
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

app.secret_key = os.urandom(24)
app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = 'iQnG3ACqz9'
app.config['MYSQL_PASSWORD'] = 'OQbU3JbFVB'
app.config['MYSQL_DB'] = 'iQnG3ACqz9'
mysql = MySQL(app)

@app.route('/<id>')
def login(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM upload WHERE id = %s", (str(id),))
    response = cursor.fetchall()
    try:
        if(len(response[-1][-1].split(" "))<5):
            pass
    except:
        return jsonify({"output":000})
       
    test_data = response[-1][-1]
                       
    print(textstat.flesch_reading_ease(test_data),"\n",
    textstat.smog_index(test_data),"\n",
    textstat.flesch_kincaid_grade(test_data),"\n",
    textstat.coleman_liau_index(test_data),"\n",
    textstat.automated_readability_index(test_data),"\n",
    textstat.dale_chall_readability_score(test_data),"\n",
    textstat.difficult_words(test_data),"\n",
    textstat.linsear_write_formula(test_data),"\n",
    textstat.gunning_fog(test_data),"\n",
    textstat.text_standard(test_data),"\n",
    textstat.fernandez_huerta(test_data),"\n",
    textstat.szigriszt_pazos(test_data),"\n",
    textstat.gutierrez_polini(test_data),"\n",
    textstat.crawford(test_data))

    return jsonify({"output":
        {
            "id":response[-1][0],
            "email":response[-1][1],
            "time":response[-1][2],
            "text_input":response[-1][3],
            "flesch_reading_ease":textstat.flesch_reading_ease(test_data),
            "smog_index":textstat.smog_index(test_data),
            "flesch_kincaid_grade":textstat.flesch_kincaid_grade(test_data),
            "coleman_liau_index":textstat.coleman_liau_index(test_data),
            "automated_readability_index":textstat.automated_readability_index(test_data),
            "dale_chall_readability_score":textstat.dale_chall_readability_score(test_data),
            "difficult_words":textstat.difficult_words(test_data),
            "linsear_write_formula":textstat.linsear_write_formula(test_data),
            "gunning_fog":textstat.gunning_fog(test_data),
            "text_standard":textstat.text_standard(test_data),
            "fernandez_huerta":textstat.fernandez_huerta(test_data),
            "szigriszt_pazos":textstat.szigriszt_pazos(test_data),
            "gutierrez_polini":textstat.gutierrez_polini(test_data),
            "crawford":textstat.crawford(test_data)
    }})

@app.route('/')
def alldata():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM predict")
    response = cursor.fetchall()
    dict1 = {}
    headings=["automated_readability_index", "coleman_liau_index","crawford", 
                        "dale_chall_readability_score", "difficult_words", "fernandez_huerta", 
                        "flesch_kincaid_grade", "flesch_reading_ease", "gunning_fog", 
                        "gutierrez_polini", "linsear_write_formula", "smog_index", 
                        "szigriszt_pazos"]
    for j,i in enumerate(response):
        dict1[j]={
                    "id":i[0],
                    "time":i[1],
                    "email":i[2],
                    "text_input":i[3],
                    "text_standard":i[4],
                    "automated_readability_index":i[5],
                    "coleman_liau_index":i[6],
                    "crawford":i[7],
                    "dale_chall_readability_score":i[8],
                    "difficult_words":i[9],
                    "fernandez_huerta":i[10],
                    "flesch_kincaid_grade":i[11],
                    "flesch_reading_ease":i[12],
                    "gunning_fog":i[13],
                    "gutierrez_polini":i[14],
                    "linsear_write_formula":i[15],
                    "smog_index":i[16],
                    "szigriszt_pazos":i[17]
                }        
            
    print(dict1)

    return jsonify({"output":dict1})

@app.route('/user/<emailvalue>')
def userdata(emailvalue):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM predict where email = %s", (str(emailvalue),))
    response = cursor.fetchall()
    dict1 = {}
    headings=["automated_readability_index", "coleman_liau_index","crawford", 
                        "dale_chall_readability_score", "difficult_words", "fernandez_huerta", 
                        "flesch_kincaid_grade", "flesch_reading_ease", "gunning_fog", 
                        "gutierrez_polini", "linsear_write_formula", "smog_index", 
                        "szigriszt_pazos"]
    for j,i in enumerate(response):
        dict1[j]={
                    "id":i[0],
                    "time":i[1],
                    "email":i[2],
                    "text_input":i[3],
                    "text_standard":i[4],
                    "automated_readability_index":i[5],
                    "coleman_liau_index":i[6],
                    "crawford":i[7],
                    "dale_chall_readability_score":i[8],
                    "difficult_words":i[9],
                    "fernandez_huerta":i[10],
                    "flesch_kincaid_grade":i[11],
                    "flesch_reading_ease":i[12],
                    "gunning_fog":i[13],
                    "gutierrez_polini":i[14],
                    "linsear_write_formula":i[15],
                    "smog_index":i[16],
                    "szigriszt_pazos":i[17]
                }        
            
    print(dict1)

    return jsonify({"output":dict1})

if __name__ == "__main__":
    app.run(debug=True)
