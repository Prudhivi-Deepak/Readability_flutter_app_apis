import textstat
import json
from flask.json import jsonify
from flask import Flask, redirect, url_for, session,render_template,request

app = Flask(__name__)
@app.route('/')
def login():
    test_data = (
        "Playing games has always been thought to be important to "
        "the development of well-balanced and creative children; "
        "however, what part, if any, they should play in the lives "
        "of adults has never been researched that deeply. I believe "
        "that playing games is every bit as important for adults "
        "as for children. Not only is taking time out to play games "
        "with our children and other adults valuable to building "
        "interpersonal relationships but is also a wonderful way "
        "to release built up tension."
    )

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

    return jsonify({
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
    })

if __name__ == "__main__":
    app.run(debug=True)
