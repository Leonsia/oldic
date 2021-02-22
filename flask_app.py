# First we imported the Flask class. An instance of this class will be our WSGI application.
from flask import Flask
from flask import request, jsonify, render_template
import dict_functions
import pickle
import jellyfish
import re
import os
import datetime as dt
from random import shuffle

# Store recent queries
recent_words = ["garðr", "ormr", "bók", "maðr", "galdr", "gestr", "leita", "barn", "áss"]
shuffle(recent_words)

# Next we create an instance of this class.
# The first argument is the name of the application’s module or package.
# If you are using a single module (as in this example), you should use __name__ because depending on
# if it’s started as application or imported as module the name will be different ('__main__' versus the actual import name).
# This is needed so that Flask knows where to look for templates, static files, and so on.
app = Flask(__name__)

#with open(os.path.join(os.getcwd(), "dicts/demo.txt"), 'r') as f:   # load test file
#    demo = f.read()

# We use the route() decorator to tell Flask what URL should trigger our function.
@app.route('/')
def home():
    html_page = render_template('isl_front.html', recent_results = recent_words[::-1])
    #with open("index.html", "w", encoding='utf-8') as file:
    #    file.write(html_page)
    return html_page
    #return render_template('isl_front.html', recent_results = recent_words[::-1])


@app.route('/lookup', methods=['POST'])
def lookup():

    search_word = list(request.form.values())[0].lower().strip()

    if len(search_word) > 0:

        zoega_text, zoega_respond_main, flag_success_zoega_1 = dict_functions.find_word(search_word.replace("ǫ", "ö"),  dict_zoega, "Zoega")
        zoega_respond_alt, zoega_respond_found, flag_success_zoega_2 =  dict_functions.zoega_alt_find(search_word.replace("ǫ", "ö"),  dict_zoega, verb_forms = verb_forms)
        flag_success_zoega = flag_success_zoega_1 or flag_success_zoega_2

        try:
            zoega_page_check = "http://norroen.info/dct/zoega/" + dict_link_zoega[search_word.replace("ǫ", "ö")[0]] + ".html"
        except:
            zoega_page_check = "http://norroen.info/dct/zoega/"

        cleasby_text, cleasby_respond_main, flag_success_cleasby_1 = dict_functions.find_word(search_word.replace("ǫ", "ö"), dict_cleasby, "Cleasby")
        cleasby_respond_alt, cleasby_respond_found, flag_success_cleasby_2 = dict_functions.cleasby_alt_find(search_word.replace("ǫ", "ö"), dict_cleasby, verb_forms = verb_forms)
        flag_success_cleasby = flag_success_cleasby_1 or flag_success_cleasby_2

        try:
            cleasby_page_check = "http://norroen.info/dct/cleasby/" + dict_link_cleasby[search_word.replace("ǫ", "ö")[0]] + ".html"
        except:
            cleasby_page_check = "http://norroen.info/dct/cleasby/"

        new_text, new_respond_main, flag_success_rus_1 = dict_functions.find_word(search_word.replace("ö", "ǫ"), dict_new, "New")
        new_respond_alt, new_respond_found, flag_success_rus_2 = dict_functions.new_alt_find(search_word.replace("ö", "ǫ"), dict_new, verb_forms = verb_forms)
        flag_success_rus = flag_success_rus_1 or flag_success_rus_2

        flag_success = flag_success_zoega or flag_success_cleasby or flag_success_rus

        try:
            new_page_check = "http://norroen.info/dct/new/" + dict_link_new[search_word[0]] + ".html"
        except:
            new_page_check = "http://norroen.info/dct/new/"

        with open(os.path.join(os.getcwd(), "stats/history.txt"), 'a', encoding='utf-8') as file:
            (file.write(str(dt.datetime.now()) + '    |    ' + search_word.ljust(12) +  '    | ' + str(flag_success_zoega) + ' | '
             + str(flag_success_cleasby) +  ' | ' + str(flag_success_rus) + '\n'))

        if flag_success:
            recent_words.append(search_word)
            recent_words.pop(0)

        html_page = render_template('results.html',
        zoega_text = zoega_text, zoega_respond_1 = zoega_respond_main, zoega_respond_2 = zoega_respond_alt,
        zoega_alt_results = zoega_respond_found, zoega_check_link  = zoega_page_check,
        cleasby_text = cleasby_text, cleasby_respond_1 = cleasby_respond_main, cleasby_respond_2 = cleasby_respond_alt,
        cleasby_alt_results = cleasby_respond_found, cleasby_check_link  =  cleasby_page_check,
        new_text = new_text, new_respond_1 = new_respond_main, new_respond_2 = new_respond_alt,
        new_alt_results = new_respond_found, new_check_link  =  new_page_check,
        recent_results = recent_words[::-1])

        if flag_success:
            with open("results/" + search_word + ".html", "w", encoding='utf-8') as file:
                file.write(html_page)

        return html_page

    else:
        html_page = render_template('results.html',
        zoega_text = "Sorry, you didn't enter anything!", zoega_respond_1 = "Please try again or: ",
        zoega_respond_2 = "", zoega_alt_results ="", zoega_check_link  =  "http://norroen.info/dct/zoega/",
        cleasby_text = "", cleasby_respond_1 = "", cleasby_respond_2 = "",
        cleasby_alt_results ="", cleasby_check_link  =  "http://norroen.info/dct/cleasby/",
        new_text = "", new_respond_1 = "", new_respond_2 = "",
        new_alt_results ="", new_check_link  =  "http://norroen.info/dct/new/",
        recent_results = recent_words[::-1])

        return html_page


@app.errorhandler(404)
def page_not_found(e):
    return render_template('page_404.html'), 404
    

if __name__ == "__main__":

    with open('dicts/dict_zoega.pickle', 'rb') as f:   # load Zoega dicitonary
        dict_zoega = pickle.load(f)

    with open('dicts/dict_link_zoega.pickle', 'rb') as f:   # load links to Zoega dicitonary pages
        dict_link_zoega = pickle.load(f)

    with open('dicts/dict_cleasby.pickle', 'rb') as f:   # load Cleasby dicitonary
        dict_cleasby = pickle.load(f)

    with open('dicts/dict_link_cleasby.pickle', 'rb') as f:   # load links to Cleasby dicitonary pages
        dict_link_cleasby = pickle.load(f)

    with open('dicts/dict_new.pickle', 'rb') as f:   # load New OldIcelandic-Russian dictionary
        dict_new = pickle.load(f)

    with open('dicts/dict_link_new.pickle', 'rb') as f:   # load links to New OldIcelandic-Russian dicitonary pages
        dict_link_new = pickle.load(f)

    with open('dicts/verb_forms_all.pickle', 'rb') as f:   # load dumped dictionary with strong verb forms
        verb_forms = pickle.load(f)


    app.run(debug=True)


# To run application use python command shell:
# $ python -m flask run
# * Running on http://127.0.0.1:5000/

# Now head over to http://127.0.0.1:5000/, and you should see your hello world greeting.
# Source: https://flask.palletsprojects.com/en/1.1.x/quickstart/
