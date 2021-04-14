# Load Flask modules and standard python libraries
from flask import Flask, request, redirect, render_template
import datetime as dt
import os
import pickle
from random import shuffle

# Load custom python module to search words in dictionaries
import dict_functions

# Store default queries in random order to display recent queries further
recent_words = ["garðr", "ormr", "bók", "maðr", "galdr", "gestr", "leita", "barn", "áss"]
shuffle(recent_words)

# Instantiate Flask app
app = Flask(__name__)

# Get list of existing html-pages to show in priority
existing_pages = [name.strip(".html") for name in os.listdir("results")]

# The main website page - oldic.ru
@app.route('/')
def home():
    html_page = render_template('isl_front.html', recent_results = recent_words[::-1])
    #with open("index.html", "w", encoding='utf-8') as file:
    #    file.write(html_page)
    return html_page
    #return render_template('isl_front.html', recent_results = recent_words[::-1])

# Page to display search results - oldic.ru/lookup
@app.route('/lookup', methods=['POST'])
def lookup():

    search_word = list(request.form.values())[0].lower().replace("<", "").replace(">", "").replace("/", "").replace("&", "").strip()    # Get the searched word as website form input
    if len(search_word) > 0:      # Check the input is not empty

        #if search_word in existing_pages:  # Check if the searched word is already present in the names of generated html-pages

        #    with open(os.path.join(os.getcwd(), "stats/history.txt"), 'a', encoding='utf-8') as file:   # Store the searched word in log file
        #        file.write(str(dt.datetime.now()) + '    |    ' + search_word.ljust(12) +  '\n')

        #    recent_words.append(search_word)   #   Add the searched word to the recent queries with replacing the last word in the list.
        #    recent_words.pop(0)

        #    return redirect("/results/" + search_word + ".html")   # Redirect to the relevant html-page

        #else:   #   If the searched word is new, implement it's search in dictionaries

        # Implement search in Geir T. Zoega  dictionary
        zoega_text, zoega_respond_main, flag_success_zoega_1 = dict_functions.find_word(search_word.replace("ǫ", "ö"),  dict_zoega, "Zoega")
        zoega_respond_alt, zoega_respond_found, flag_success_zoega_2 =  dict_functions.zoega_alt_find(search_word.replace("ǫ", "ö"),  dict_zoega, verb_forms = verb_forms)
        flag_success_zoega = flag_success_zoega_1 or flag_success_zoega_2    # Check if direct (flag_success_zoega_1) or fuzzy (flag_success_zoega_2) searches have brought any result.

        # Add link to Geir T. Zoega web-page which correspond to the first letter of the searched word.
        try:
            zoega_page_check = "http://norroen.info/dct/zoega/" + dict_link_zoega[search_word.replace("ǫ", "ö")[0]] + ".html"
        except:
            zoega_page_check = "http://norroen.info/dct/zoega/"

        # Implement search in Richard Cleasby  dictionary
        cleasby_text, cleasby_respond_main, flag_success_cleasby_1 = dict_functions.find_word(search_word.replace("ǫ", "ö"), dict_cleasby, "Cleasby")
        cleasby_respond_alt, cleasby_respond_found, flag_success_cleasby_2 = dict_functions.cleasby_alt_find(search_word.replace("ǫ", "ö"), dict_cleasby, verb_forms = verb_forms)
        flag_success_cleasby = flag_success_cleasby_1 or flag_success_cleasby_2     # Check if direct (flag_success_cleasby_1) or fuzzy (flag_success_cleasby_2) searches have brought any result.

        # Add link to Richard Cleasby web-page which correspond to the first letter of the searched word.
        try:
            cleasby_page_check = "http://norroen.info/dct/cleasby/" + dict_link_cleasby[search_word.replace("ǫ", "ö")[0]] + ".html"
        except:
            cleasby_page_check = "http://norroen.info/dct/cleasby/"

        # Implement search in Oldicelandic Russian dictionary
        new_text, new_respond_main, flag_success_rus_1 = dict_functions.find_word(search_word.replace("ö", "ǫ"), dict_new, "New")
        new_respond_alt, new_respond_found, flag_success_rus_2 = dict_functions.new_alt_find(search_word.replace("ö", "ǫ"), dict_new, verb_forms = verb_forms)
        flag_success_rus = flag_success_rus_1 or flag_success_rus_2   # Check if direct (flag_success_rus_1) or fuzzy (flag_success_rus_2) searches have brought any result.

        # Add link to Oldicelandic Russian web-page which correspond to the first letter of the searched word.
        try:
            new_page_check = "http://norroen.info/dct/new/" + dict_link_new[search_word[0]] + ".html"
        except:
            new_page_check = "http://norroen.info/dct/new/"

        # Check if any search in dictionaries has non-empty result.
        flag_success = flag_success_zoega or flag_success_cleasby or flag_success_rus

        # Check word entrences in saga texts and get paragraphs with the word
        text_blocks = dict_functions.search_word(search_word, master_edda_texts_fixed_on, master_edda_texts_fixed_ru)

        # Store the searched word in log file with corresponding flags of non-empty results.
        with open(os.path.join(os.getcwd(), "stats/history.txt"), 'a', encoding='utf-8') as file:
            (file.write(str(dt.datetime.now()) + '    |    ' + search_word.ljust(12) +  '    | ' + str(flag_success_zoega) + ' | '
                + str(flag_success_cleasby) +  ' | ' + str(flag_success_rus) + '\n'))

        # For non-empty result, add the searched word to the recent queries with replacing the last word in the list.
        # Thus unsuccessful or erroneous queries are not displayed on website.
        if flag_success:
            recent_words.append(search_word)
            recent_words.pop(0)

        # Generate html-page with search results.
        html_page = render_template('results.html',
        zoega_text = zoega_text, zoega_respond_1 = zoega_respond_main, zoega_respond_2 = zoega_respond_alt,
        zoega_alt_results = zoega_respond_found, zoega_check_link  = zoega_page_check,
        cleasby_text = cleasby_text, cleasby_respond_1 = cleasby_respond_main, cleasby_respond_2 = cleasby_respond_alt,
        cleasby_alt_results = cleasby_respond_found, cleasby_check_link  =  cleasby_page_check,
        new_text = new_text, new_respond_1 = new_respond_main, new_respond_2 = new_respond_alt,
        new_alt_results = new_respond_found, new_check_link  =  new_page_check,
        recent_results = recent_words[::-1], text_blocks = text_blocks)

        # Save generated html-page to the website catalog if the search was successful.
        if flag_success:
            with open("results/" + search_word + ".html", "w", encoding='utf-8') as file:
                file.write(html_page)

        return html_page

    else:   # If the input is empty, no need to conduct any search.
        html_page = render_template('results_empty.html',
        zoega_text = "Sorry, you didn't enter anything!", zoega_respond_1 = "Please try again or: ",
        zoega_respond_2 = "", zoega_alt_results ="", zoega_check_link  =  "http://norroen.info/dct/zoega/",
        cleasby_text = "", cleasby_respond_1 = "", cleasby_respond_2 = "",
        cleasby_alt_results ="", cleasby_check_link  =  "http://norroen.info/dct/cleasby/",
        new_text = "", new_respond_1 = "", new_respond_2 = "",
        new_alt_results ="", new_check_link  =  "http://norroen.info/dct/new/",
        recent_results = recent_words[::-1])

        return html_page

# Handle 404-error (page not found) with custom html-page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error_handlers/page_404.html'), 404

# Handle 403-error (access denied) with custom html-page
#@app.errorhandler(403)
#def forbidden(e):
#    return render_template('error_handlers/page_403.html'), 403

# Handle 500-error (internal server error) with custom html-page
#@app.errorhandler(500)
#def serverError(e):
#    return render_template('error_handlers/page_500.html'), 500

if __name__ == "__main__":

# Load old icelandic dictionaries and links to web-dict pages

    with open('dicts/dict_zoega.pickle', 'rb') as f:   #  Geir T. Zoega  dictionary
        dict_zoega = pickle.load(f)

    with open('dicts/dict_link_zoega.pickle', 'rb') as f:   #  Links to alphabetic Geir T. Zoega web-pages at http://norroen.info/dct/zoega/
        dict_link_zoega = pickle.load(f)

    with open('dicts/dict_cleasby.pickle', 'rb') as f:   # Richard Cleasby dictionary
        dict_cleasby = pickle.load(f)

    with open('dicts/dict_link_cleasby.pickle', 'rb') as f:   # Links to alphabetic Richard Cleasby web-pages at http://norroen.info/dct/cleasby/
        dict_link_cleasby = pickle.load(f)

    with open('dicts/dict_new.pickle', 'rb') as f:   # Oldicelandic Russian dictionary
        dict_new = pickle.load(f)

    with open('dicts/dict_link_new.pickle', 'rb') as f:   # Links to alphabetic Oldicelandic Russian web-pages at http://norroen.info/dct/new/
        dict_link_new = pickle.load(f)

    with open('dicts/verb_forms_all.pickle', 'rb') as f:   #  Custom dictionary of strong and weak verbs generated from https://paradigms.langeslag.org/landing
        verb_forms = pickle.load(f)

    with open('dicts/master_edda_texts_fixed_on.pickle', 'rb') as f:   #  Texts of Edda in Old-Norse
        master_edda_texts_fixed_on = pickle.load(f)

    with open('dicts/master_edda_texts_fixed_ru.pickle', 'rb') as f:   # Texts of Edda in Russian
        master_edda_texts_fixed_ru = pickle.load(f)


    app.run(debug=True)


# To run application use python command shell:
# $ python -m flask run
# * Running on http://127.0.0.1:5000/

# Now head over to http://127.0.0.1:5000/, and you should see your hello world greeting.
# Source: https://flask.palletsprojects.com/en/1.1.x/quickstart/
