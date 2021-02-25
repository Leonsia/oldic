import re
import jellyfish

def find_word(word, dictionary, dict_name):
    """Return word definition from dictionary"""
    try:
        return ("Geir T. Zoega dictionary: " if dict_name == "Zoega"
            else "Richard Cleasby dictionary: " if dict_name == "Cleasby"
            else "Новый древнеисландско-русский словарь: "), dictionary[word], 1
    except:
        #return ("К сожалению, \"{}\" не найдено.".format(word) if dict_name == "New"
        #    else "Sorry, no \"{input_word}\" was directly found in {dict_name} vocabualary.".format(input_word = word, dict_name = dict_name)), ""
        return ("Geir T. Zoega dictionary: " if dict_name == "Zoega"
            else "Richard Cleasby dictionary: " if dict_name == "Cleasby"
            else "Новый древнеисландско-русский словарь: "), "", 0


def find_levi(word, dictionary):
    """Find closest words to the given according to Levenstein distance"""
    first_letter = word[0]
    dict_words = [key.lower() for key in dictionary.keys() if key.lower()[0] == first_letter]

    if word[-2:] == "ar" or word[-2:] == "ir":
        word = word[:-2]
    elif word[-3:] == "ðum" or word[-3:] == "ðuð" or word[-3:] == "ðir":
        word = word[:-3].replace("ö", "a")
    elif word[-2:] == "ið" or word[-2:] == "ði" or word[-2:] == "ða" or word[-2:] == "ðu":
        word = word[:-2]
    elif word[-2:] == "um":
        if word[:-2] in dict_words:
            return [word[:-2]]
        else:
            word = word[:-2].replace("ö", "a")
    else:
        word = word

    levi_words = ([letter_word for letter_word in dict_words
                   if jellyfish.levenshtein_distance(word, letter_word) == 1
                   or jellyfish.levenshtein_distance(word, re.sub(r"ja$", "", letter_word)) == 1])
    return levi_words


def drop_noun_article(word):
    """Drop article from the word to get it's lemma"""
    lemmas = []

    if word[-5:] in ("innar"):
        lemmas.append(word[:-5])

    if word[-4:] in ("inni", "inum", "nnar", "unum"):
        lemmas.append(word[:-4])

    if word[-3:] in ("ina", "inn", "ins", "nar", "nir", "nna",  "nni", "num"):
        lemmas.append(word[:-3])

    if word[-2:] in ("in", "it", "na", "nn", "ns", "nu"):
        lemmas.append(word[:-2])

    if word[-1:] in ("t", "n"):
        lemmas.append(word[:-1])

    return lemmas


def paradigm_nouns(word, dict_words):
    """Search for noun normal form using grammar rules"""
    para_words = []

    if word + "r" in dict_words:
        para_words.append(word + "r")
    elif word.replace("ö", "a") in dict_words:
        para_words.append(word.replace("ö", "a"))


    if word[-2:] in ("ar"):
        if word[:-2] in dict_words:
            para_words.append(word[:-2])
        if word[:-3] in dict_words:
            para_words.append(word[:-3])
        if word[:-2] + "r" in dict_words:
            para_words.append(word[:-2] + "r")
        if word[:-2] + "i" in dict_words:
            para_words.append(word[:-2] + "i")
        if word[:-2] + "ir" in dict_words:
            para_words.append(word[:-2] + "ir")
        if word[:-2].replace("a", "ö") in dict_words:
            para_words.append(word[:-2].replace("a", "ö"))
        if word[:-2].replace("a", "ö") + "r" in dict_words:
            para_words.append(word[:-2].replace("a", "ö")  + "r")
        if word[:-3].replace("a", "e").replace("u", "y") + "ill" in dict_words:               # change
            para_words.append(word[:-3].replace("a", "e").replace("u", "y") + "ill")

    elif word[-2:] in ("ir"):
        if word[:-2] + "r" in dict_words:
            para_words.append(word[:-2] + "r")
        if word[:-2].replace("e", "ö") + "r" in dict_words:
            para_words.append(word[:-2].replace("e", "ö") + "r")
        if word[:-2].replace("i", "jö") + "r" in dict_words:
            para_words.append(word[:-2].replace("i", "jö") + "r")

    elif word[-2:] in ("um"):
        if word[:-2] in dict_words:
            para_words.append(word[:-2])
        if word[:-2] + "i" in dict_words:
            para_words.append(word[:-2] + "i")
        if word[:-3] in dict_words:
            para_words.append(word[:-3])
        if word[:-2].replace("ö", "a") in dict_words:
            para_words.append(word[:-2].replace("ö", "a"))
        if word[:-2].replace("ö", "a") + "r" in dict_words:
            para_words.append(word[:-2].replace("ö", "a") + "r")
        if word[:-2] + "ir" in dict_words:
            para_words.append(word[:-2] + "ir")
        if word[-3:-2] in ("r"):
            if word[:-2].replace("r", "ar") in dict_words:
                para_words.append(word[:-2].replace("r", "ar"))
        if word[-3:-2] in ("l"):
            word_kettle = word[:-3].replace("ö", "e").replace("u", "y") + "ill"
            if word_kettle in dict_words:
                para_words.append(word_kettle)
            if word[:-3].replace("u", "y") + "ill" in dict_words:    # change
                para_words.append(word[:-3].replace("u", "y") + "ill")

    elif word[-2:] in ("ur"):
        if word[:-2].replace("ö", "a") + "a" in dict_words:
            para_words.append(word[:-2].replace("ö", "a") + "a")
        if word[:-2] + "ar" in dict_words:
            para_words.append(word[:-2] + "ar")

    elif word[-2:] in ("na"):
        if word[:-2] + "a" in dict_words:
            para_words.append(word[:-2] + "a")

    if word[-1:] in ("i", "s", "a"):
        if word[:-1] in dict_words:
            para_words.append(word[:-1])
        if word[:-2] in dict_words:
            para_words.append(word[:-2])
        if word[:-1] + "r" in dict_words:
            para_words.append(word[:-1] + "r")
        if word[:-1] + "i" in dict_words:
            para_words.append(word[:-1] + "i")
        if word[:-1].replace("e", "ö") + "r" in dict_words:
            para_words.append(word[:-1].replace("e", "ö") + "r")
        if word[:-1].replace("a", "ö") + "r" in dict_words:
            para_words.append(word[:-1].replace("a", "ö") + "r")
        if word[:-1].replace("a", "ö") in dict_words:
            para_words.append(word[:-1].replace("a", "ö"))
        if word[:-1].replace("i", "jö") + "r" in dict_words:
            para_words.append(word[:-1].replace("i", "jö") + "r")
        if word[:-1].replace("œ", "ó") + "r" in dict_words:
            para_words.append(word[:-1].replace("œ", "ó") + "r")
        if word[:-1] + "ir" in dict_words:
            para_words.append(word[:-1] + "ir")
        if word[-2:-1] in ("r"):
            if word[:-1].replace("r", "ar") in dict_words:
                para_words.append(word[:-1].replace("r", "ar"))
        if word[-2:-1] in ("l"):
            if word[:-1] + "l" in dict_words:
                para_words.append(word[:-1] + "l")
            else:
                word_kettle = word[:-2].replace("a", "e").replace("u", "y") + "ill"          # change
                if word_kettle in dict_words:
                    para_words.append(word_kettle)

    elif word[-1:] in ("r"):
        if word[:-1].replace("e", "ö") in dict_words:
            para_words.append(word[:-1].replace("e", "ö"))
        if word.replace("œ", "ó") in dict_words:
            para_words.append(word.replace("œ", "ó"))
        if word[:-1].replace("œ", "ó") in dict_words:
            para_words.append(word[:-1].replace("œ", "ó"))

    elif word[-1:] in ("l"):
        if word + "l"  in dict_words:
            para_words.append(word + "l")

    elif word[-1:] in ("u"):
        if word[:-1] in dict_words:
            para_words.append(word[:-1])
        if word[:-1].replace("ö", "a") + "a" in dict_words:
            para_words.append(word[:-1].replace("ö", "a") + "a")

    return para_words


def paradigm_adj(word, dict_words):
    """Additional search for adjective normal form using grammar rules"""
    para_words = []

    if "ö" in word:
        if word.replace("ö", "a") + "r" in dict_words:
            para_words.append(word.replace("ö", "a") + "r")
        elif word[:-1].replace("ö", "a") + "r" in dict_words:
            para_words.append(word[:-1].replace("ö", "a") + "r")

    if word[-1:] in ("l"):
        if word.replace("ö", "a").replace("u", "a") + "l" in dict_words:
            para_words.append(word.replace("ö", "a").replace("u", "a") + "l")

    elif word[-1:] in ("n"):
        if word[:-2] + "ll" in dict_words:
            para_words.append(word[:-2] + "ll")

    elif word[-1:] in ("t"):
        if word[:-1] + "ll" in dict_words:
            para_words.append(word[:-1] + "ll")

    elif word[-1:] in ("a", "u") and word[-2:-1] in ("j", "v"):
        if word[:-2] + "r" in dict_words:
            para_words.append(word[:-2] + "r")

    elif word[-1:] in ("u"):
        if word[:-1] + "r" in dict_words:
            para_words.append(word[:-1] + "r")

    elif word[-1:] in ("i"):
        if word[:-2] + "r" in dict_words:
            para_words.append(word[:-2] + "r")

    if word[-2:-1] in ("l"):
        if word[:-2].replace("ö", "a") + "all" in dict_words:
            para_words.append(word[:-2].replace("ö", "a") + "all")
        if word[:-2] + "ill" in dict_words:
            para_words.append(word[:-2] + "ill")
        if word[:-2].replace("i", "í") + "ill" in dict_words:
            para_words.append(word[:-2].replace("i", "í") + "ill")

    if word[-2:] in ("um") and word[-3:-2] in ("l"):
        if word[:-2] + "r" in dict_words:
            para_words.append(word[:-2] + "r")
        if word[:-3].replace("ö", "a") + "all" in dict_words:
            para_words.append(word[:-3].replace("ö", "a") + "all")
        if word[:-3].replace("i", "í") + "ill" in dict_words:
            para_words.append(word[:-3].replace("i", "í") + "ill")

    elif word[-2:] in ("um") and word[-3:-2] in ("j"):
        if word[:-3] + "r" in dict_words:
            para_words.append(word[:-3] + "r")

    elif word[-2:] in ("um"):
        if word[:-2].replace("ö", "a") + "i" in dict_words:
            para_words.append(word[:-2].replace("ö", "a") + "i")

    elif word[-2:] in ("an", "ar", "ir") and word[-3:-2] in ("l"):
        if word[:-3] + "all" in dict_words:
            para_words.append(word[:-3] + "all")
        if word[:-3] + "ill" in dict_words:
            para_words.append(word[:-3] + "ill")
        if word[:-3].replace("i", "í") + "ill" in dict_words:
            para_words.append(word[:-3].replace("i", "í") + "ill")

    elif word[-2:] in ("an", "ar", "ir") and word[-3:-2] in ("j", "v"):
        if word[:-3] + "r" in dict_words:
            para_words.append(word[:-3] + "r")

    return para_words


def drop_verb_participle(word):
    """Drop participle to get verb's lemma"""

    lemmas = []

    if word[-5:] in ("innar"):
        lemmas.append(word[:-5])

    if word[-4:] in ("andi", "inna", "inni", "ðrar"):
        lemmas.append(word[:-4])

    if word[-3:] in ("inn", "ins", "nir", "nar", "ðan", "ðar", "ðir", "ðra", "ðri", "ðum"):
        lemmas.append(word[:-3])

    if word[-2:] in ("na", "ðr", "ðs", "ðu", "ða", "at", "in", "it"):
        lemmas.append(word[:-2])

    if word[-1:] in ("ð", "t"):
        lemmas.append(word[:-1])

    return lemmas


def paradigm_verb(word, dict_words):
    """Search for verb normal form using grammar rules"""
    para_words = []

    if word.replace("e", "a") + "a" in dict_words:
        para_words.append(word.replace("e", "a") + "a")

    if word.replace("ó", "a") + "a" in dict_words:
        para_words.append(word.replace("ó", "a") + "a")

    if word.replace("œ", "a") in dict_words:
        para_words.append(word.replace("œ", "a"))

    if word + "a" in dict_words:
        para_words.append(word + "a")

    if word + "ja" in dict_words:
        para_words.append(word + "ja")

    if word[-1:] in ("r"):
        if word[:-1].replace("e", "a") + "a" in dict_words:
            para_words.append(word[:-1].replace("e", "a") + "a")
        if word[:-1] + "ja" in dict_words:
            para_words.append(word[:-1] + "ja")

    elif word[-1:] in ("i"):
        if word[:-1] + "a" in dict_words:
            para_words.append(word[:-1] + "a")
        if word[:-1] + "ja" in dict_words:
            para_words.append(word[:-1] + "ja")
        if word[:-1].replace("œ", "a") + "a" in dict_words:
            para_words.append(word[:-1].replace("œ", "a")  + "a")

    elif word[-1:] in ("u", "t", "ð"):
        if word[:-1].replace("ó", "a") + "a" in dict_words:
            para_words.append(word[:-1].replace("ó", "a") + "a")
        if word[:-1].replace("ó", "a") + "nda" in dict_words:
            para_words.append(word[:-1].replace("ó", "a") + "nda")
        if word[:-2].replace("a", "e") + "ja" in dict_words:
            para_words.append(word[:-2].replace("a", "e") + "ja")
        if word[:-2].replace("ö", "a") + "a" in dict_words:
            para_words.append(word[:-2].replace("ö", "a") + "a")

    if word[-2:] in ("ir", "ið", "im"):
        if word[:-2] + "a" in dict_words:
            para_words.append(word[:-2] + "a")
        if word[:-2] + "ja" in dict_words:
            para_words.append(word[:-2] + "ja")
        if word[:-2].replace("œ", "a") + "a" in dict_words:
            para_words.append(word[:-2].replace("œ", "a")  + "a")

    elif word[-2:] in ("um"):
        if word[:-2].replace("ö", "a") + "a" in dict_words:
            para_words.append(word[:-2].replace("ö", "a") + "a")
        if word[:-2].replace("ó", "a") + "a" in dict_words:
            para_words.append(word[:-2].replace("ó", "a") + "a")

    elif word[-2:] in ("uð"):
        if word[:-2].replace("ó", "a") + "a" in dict_words:
            para_words.append(word[:-2].replace("ó", "a") + "a")

    elif word[-2:] in ("nu"):
        if word[:-2].replace("ö", "a") + "a" in dict_words:
            para_words.append(word[:-2].replace("ö", "a") + "a")

    elif word[-2:] in ("ða", "ði", "di", "ti"):
        if word[:-2] + "a" in dict_words:
            para_words.append(word[:-2] + "a")
        if word[:-2].replace("e", "a") + "a" in dict_words:
            para_words.append(word[:-2].replace("e", "a") + "a")
        if word[:-2].replace("a", "e") + "ja" in dict_words:
            para_words.append(word[:-2].replace("a", "e") + "ja")
        if word[:-2].replace("u", "y") + "ja" in dict_words:
            para_words.append(word[:-2].replace("u", "y") + "ja")

    elif word[-2:] in ("ðu", "du", "tu"):
        if word[:-2] + "a" in dict_words:
            para_words.append(word[:-2] + "a")
        if word[:-2].replace("ö", "e") + "ja" in dict_words:
            para_words.append(word[:-2].replace("ö", "e") + "ja")
        if word[:-2].replace("ö", "a") + "a" in dict_words:
            para_words.append(word[:-2].replace("ö", "a") + "a")
        if word[:-3].replace("ö", "a") + "a" in dict_words:
            para_words.append(word[:-3].replace("ö", "a") + "a")
        if word[:-2].replace("u", "y") + "ja" in dict_words:
            para_words.append(word[:-2].replace("u", "y") + "ja")
        if word[:-2].replace("ó", "a") + "nda" in dict_words:
            para_words.append(word[:-2].replace("ó", "a") + "nda")

    elif word[-2:] in ("ðr", "ðs", "dr", "tr"):
        if word[:-3].replace("a", "e") + "ja" in dict_words:
            para_words.append(word[:-3].replace("a", "e") + "ja")
        if word[:-2].replace("u", "y") + "ja" in dict_words:
            para_words.append(word[:-2].replace("u", "y") + "ja")
        if word[:-2] + "a" in dict_words:
            para_words.append(word[:-2] + "a")

    elif word[-2:] in ("sk","zk"):
        if word[:-2] in dict_words:
            para_words.append(word[:-2])
        if word[:-2].replace("e", "a") + "a" in dict_words:
            para_words.append(word[:-2].replace("e", "a") + "a")
        if word[:-2] + "ja" in dict_words:
            para_words.append(word[:-2] + "ja")
        if word[:-3] + "a" in dict_words:
            para_words.append(word[:-3] + "a")
        if word[:-2].replace("ó", "a") + "a" in dict_words:
            para_words.append(word[:-2].replace("ó", "a") + "a")

    if word[-3:] in ("ðir", "ðið", "ðim", "ðar", "ðan"):
        if word[:-3] in dict_words:
            para_words.append(word[:-3])
        if word[:-3] + "a" in dict_words:
            para_words.append(word[:-3] + "a")
        if word[:-3] + "ja" in dict_words:
            para_words.append(word[:-3] + "ja")
        if word[:-3].replace("a", "e") + "ja" in dict_words:
            para_words.append(word[:-3].replace("a", "e") + "ja")
        if word[:-3].replace("e", "a") + "a" in dict_words:
            para_words.append(word[:-3].replace("e", "a") + "a")

    elif word[-3:] in ("ðum", "ðuð"):
        if word[:-3] + "a" in dict_words:
            para_words.append(word[:-3] + "a")
        if word[:-3].replace("ö", "e") + "ja" in dict_words:
            para_words.append(word[:-3].replace("ö", "e") + "ja")
        if word[:-3].replace("ö", "a") + "a" in dict_words:
            para_words.append(word[:-3].replace("ö", "a") + "a")
        if word[:-4].replace("ö", "a") + "a" in dict_words:
            para_words.append(word[:-4].replace("ö", "a") + "a")

    elif word[-3:] in ("ðra", "ðri"):
        if word[:-4].replace("a", "e") + "ja" in dict_words:
            para_words.append(word[:-4].replace("a", "e") + "ja")

    elif word[-3:] in ("ddi", "ddu", "ddr"):
        if word[:-3].replace("a", "e") + "ðja" in dict_words:
            para_words.append(word[:-3].replace("a", "e") + "ðja")
        if word[:-3].replace("ö", "e") + "ðja" in dict_words:
            para_words.append(word[:-3].replace("ö", "e") + "ðja")

    elif word[-3:] in ("umk", "ask", "isk", "izk", "uzk", "usk"):
        if word[:-3] + "a" in dict_words:
            para_words.append(word[:-3] + "a")
        if word[:-3] + "ja" in dict_words:
            para_words.append(word[:-3] + "ja")
        if word[:-3].replace("ö", "a") + "a" in dict_words:
            para_words.append(word[:-3].replace("ö", "a") + "a")
        if word[:-3].replace("ó", "a") + "a" in dict_words:
            para_words.append(word[:-3].replace("ó", "a") + "a")
        if word[:-3].replace("œ", "a") + "a" in dict_words:
            para_words.append(word[:-3].replace("œ", "a") + "a")

    elif word[-3:] in ("num"):
        if word[:-3].replace("ö", "a") + "a" in dict_words:
            para_words.append(word[:-3].replace("ö", "a") + "a")

    if word[-4:] in ("imsk", "umsk"):
        if word[:-4] + "ja" in dict_words:
            para_words.append(word[:-4] + "ja")
        if word[:-4] + "a" in dict_words:
            para_words.append(word[:-4] + "a")
        if word[:-4].replace("ö", "a") + "a" in dict_words:
            para_words.append(word[:-4].replace("ö", "a") + "a")
        if word[:-4].replace("ó", "a") + "a" in dict_words:
            para_words.append(word[:-4].replace("ó", "a") + "a")
        if word[:-4].replace("œ", "a") + "a" in dict_words:
            para_words.append(word[:-4].replace("œ", "a") + "a")

    elif word[-4:] in ("ðisk", "ðizk", "ðumk", "ðusk", "ðuzk"):
        if word[:-4] + "a" in dict_words:
            para_words.append(word[:-4] + "a")
        if word[:-4].replace("a", "e") + "ja" in dict_words:
            para_words.append(word[:-4].replace("a", "e") + "ja")
        if word[:-4].replace("ö", "e") + "ja" in dict_words:
            para_words.append(word[:-4].replace("ö", "e") + "ja")
        if word[:-5].replace("ö", "a") + "a" in dict_words:
            para_words.append(word[:-5].replace("ö", "a") + "a")

    elif word[-4:] in ("ðrar"):
         if word[:-5].replace("a", "e") + "ja" in dict_words:
            para_words.append(word[:-5].replace("a", "e") + "ja")

    if word[-5:] in ("ðumsk", "ðimsk"):
        if word[:-5] + "ja" in dict_words:
            para_words.append(word[:-5] + "ja")
        if word[:-5].replace("ö", "e") + "ja" in dict_words:
            para_words.append(word[:-5].replace("ö", "e") + "ja")
        if word[:-6].replace("ö", "a") + "a" in dict_words:
            para_words.append(word[:-6].replace("ö", "a") + "a")

    return para_words


def paradigm_search(word, dictionary, replace_o = False):
    """Search for normal word form based on words grammar paradigms"""
    lemmas_noun = drop_noun_article(word)                                       # change
    lemmas_verb = drop_verb_participle(word)

    if replace_o:

        dict_words = [key.replace("ǫ", "ö") for key in dictionary.keys() if key.lower()[0] == word[0]]
        # --------------Nouns-------------------------------------------------
        para_words = paradigm_nouns(word.replace("ǫ", "ö"), dict_words)
        for lemma in lemmas_noun:
            para_words.extend(paradigm_nouns(lemma.replace("ǫ", "ö"), dict_words))
        # --------------Adjectives-------------------------------------------------
        para_words.extend(paradigm_adj(word.replace("ǫ", "ö"), dict_words))  # add
        # --------------Verbs-----------------------------------------------------
        para_words.extend(paradigm_verb(word.replace("ǫ", "ö"), dict_words))
        for lemma in lemmas_verb:                                                             # add
            para_words.extend(paradigm_verb(lemma.replace("ǫ", "ö"), dict_words))

        return [dictionary[key.replace("ö", "ǫ")] for key in set(para_words) if key != word]

    else:

        dict_words = [key for key in dictionary.keys() if key.lower()[0] == word[0]]
        # --------------Nouns-------------------------------------------------
        para_words = paradigm_nouns(word, dict_words)
        for lemma in lemmas_noun:
            para_words.extend(paradigm_nouns(lemma, dict_words))
        # --------------Adjectives-------------------------------------------------
        para_words.extend(paradigm_adj(word, dict_words))  #add
         # --------------Verbs-----------------------------------------------------
        para_words.extend(paradigm_verb(word, dict_words))
        for lemma in lemmas_verb:                                                             # add
            para_words.extend(paradigm_verb(lemma, dict_words))

        return [dictionary[key] for key in set(para_words) if key != word]



def fuzzy_search(word, dictionary, verb_forms, search_values = False, limit_values = False, search_para = True, replace_o = False, add_levi = False):
    """Fuzzy search of words"""

    findings = []
    val_findings = []

    if not replace_o:
        verb_forms = { key.replace("ǫ", "ö"): value for key, value in verb_forms.items()}

    if word in verb_forms and word not in dictionary:
        verb_inf = verb_forms[word]
        try:
            findings.append(dictionary[verb_inf])
        except:
            findings.append("<a href=\"https://paradigms.langeslag.org/?q=" + verb_inf + "\" target=\"_blank\">" + verb_inf + "</a>")

    findings_para = paradigm_search(word, dictionary, replace_o = replace_o)
    for item in findings_para:
        if item not in findings:
            findings.append(item)


    for key, value in dictionary.items():
        if key.lower() == word or value in findings:
            pass
        else:
            if word in key.lower():
                findings.append(value.replace(word, "<span>" + word + "</span>"))

            if search_values and len(word) > 2:
                if limit_values:
                    if word in value[:300].lower():
                        val_findings.append(value.replace(word, "<span>" + word + "</span>"))
                else:
                    if word in value.lower():
                        val_findings.append(value.replace(word, "<span>" + word + "</span>"))


    if add_levi:
        levi = find_levi(word = word, dictionary = dictionary)
        for key in levi:
            try:
                if dictionary[key] not in findings:
                    findings.append(dictionary[key])
            except:
                pass


    return findings, val_findings



def zoega_alt_find(word, dict_zoega, verb_forms):
    """Alternative search of words by similarity"""
    # Get direct and fuzzy search results for a given word
    findings, val_findings = (fuzzy_search(word, dict_zoega, verb_forms = verb_forms,
    search_values = True, limit_values = False, search_para = True, replace_o = False, add_levi = False))

    if len(findings) == 0:      # Case there are no direct search results in Zoega dictionary.

        if len(val_findings) == 0:      # And case there are no fuzzy search results in Zoega dictionary.

            if len(word) > 6:    # If the word is long enough, let's suggest it is compounded and search again but it's first part.
                findings_part, val_findings_part = (fuzzy_search(word[:4], dict_zoega, verb_forms = verb_forms,
                search_values = True, limit_values = False, search_para = True, replace_o = False, add_levi = False))

                if len(findings_part) or len(val_findings_part) > 0:    # If the first partial search brings some result, return it.
                    findings = findings_part
                    val_findings = val_findings_part
                    for value in val_findings:  # Append fuzzy search results to direct search results, such that direct search results go first.
                        if value not in findings:
                            findings.append(value)
                    return "Nothing for \"{input_word}\". {res_num} fuzzy search results for \"{part_word}\" in \"{input_word}\":".format(
                    res_num = str(len(findings)), input_word = word, part_word = word[:4]), findings, 1

                else:    # Case the first partial search doesn't bring any result, go to the second search with first 3 letters.
                    findings_part, val_findings_part = (fuzzy_search(word[:3], dict_zoega, verb_forms = verb_forms,
                    search_values = True, limit_values = False, search_para = True, replace_o = False, add_levi = False))

                    if len(findings_part) or len(val_findings_part) > 0:    # If the second partial search brings some result, return it.
                        findings = findings_part
                        val_findings = val_findings_part
                        for value in val_findings:  # Append fuzzy search results to direct search results, such that direct search results go first.
                            if value not in findings:
                                findings.append(value)
                        return "Nothing for \"{input_word}\". {res_num} fuzzy search results for \"{part_word}\" in \"{input_word}\":".format(
                    res_num = str(len(findings)), input_word = word, part_word = word[:3]), findings, 1

                    else:   # Case none partial search bring any result, return empty result.
                        return "No fuzzy search results for \"{}\".".format(word), findings, 0

            else:   # Case the word is not long enough to be compounded and no search results for it, return empty result.
                return "No fuzzy search results for \"{}\".".format(word), findings, 0

        else:   # Case there are fuzzy search results in Zoega dictionary, but there are no direct search results
            return "{} fuzzy search results for \"{}\":".format(len(val_findings), word), val_findings, 1

    else:   # Case there are direct search results in Zoega dictionary
        for value in val_findings: # Append fuzzy search results to direct search results, such that direct search results go first.
            if value not in findings:
                findings.append(value)
        return "{res_num} fuzzy search results for \"{input_word}\":".format(res_num = str(len(findings)), input_word = word), findings, 1


def cleasby_alt_find(word,  dict_cleasby, verb_forms):
    """Alternative search of words by similarity"""
    # Get direct and fuzzy search results for a given word
    findings, val_findings = fuzzy_search(word, dict_cleasby, verb_forms = verb_forms, search_values = True, limit_values = True, search_para = True, replace_o = False, add_levi = False)

    if len(findings) == 0:  # Case there are no direct search results in Cleasby dictionary.

        if len(val_findings) == 0:   # And case there are no fuzzy search results in Cleasby dictionary.

            if len(word) > 6:    # If the word is long enough, let's suggest it is compounded and search again but it's first part.
                findings_part, val_findings_part = fuzzy_search(word[:4], dict_cleasby, verb_forms = verb_forms,
                search_values = True, limit_values = True, search_para = True, replace_o = False, add_levi = False)

                if len(findings_part) or len(val_findings_part) > 0:    # If the first partial search brings some result, return it.
                    findings = findings_part
                    val_findings = val_findings_part
                    for value in val_findings:  # Append fuzzy search results to direct search results, such that direct search results go first.
                        if value not in findings:
                            findings.append(value)
                    return "Nothing for \"{input_word}\". {res_num} fuzzy search results for \"{part_word}\" in \"{input_word}\":".format(
                    res_num = str(len(findings)), input_word = word, part_word = word[:4]), findings, 1

                else:    # Case the first partial search doesn't bring any result, go to the second search with first 3 letters.
                    findings_part, val_findings_part = fuzzy_search(word[:3], dict_cleasby, verb_forms = verb_forms,
                    search_values = True, limit_values = True, search_para = True, replace_o = False, add_levi = False)

                    if len(findings_part) or len(val_findings_part) > 0:    # If the second partial search brings some result, return it.
                        findings = findings_part
                        val_findings = val_findings_part
                        for value in val_findings:  # Append fuzzy search results to direct search results, such that direct search results go first.
                            if value not in findings:
                                findings.append(value)
                        return "Nothing for \"{input_word}\". {res_num} fuzzy search results for \"{part_word}\" in \"{input_word}\":".format(
                        res_num = str(len(findings)), input_word = word, part_word = word[:3]), findings, 1

                    else:   # Case none partial search bring any result, return empty result.
                        return "No fuzzy search results for \"{}\".".format(word), findings, 0

            else:   # Case the word is not long enough to be compounded and no search results for it, return empty result.
                return "No fuzzy search results for \"{}\".".format(word), findings, 0


        else:     # Case there are fuzzy search results in Cleasby dictionary, but there are no direct search results
            return "{} fuzzy search results for \"{}\":".format(len(val_findings), word), val_findings, 1

    else:    # Case there are direct search results in Cleasby  dictionary
        for value in val_findings:  # Append fuzzy search results to direct search results, such that direct search results go first.
            if value not in findings:
                findings.append(value)
        return "{res_num} fuzzy search results for \"{input_word}\":".format(
        res_num = str(len(findings)), input_word = word), findings, 1



def new_alt_find(word, dict_new, verb_forms):
    """Alternative search of words by similarity"""
    # Get direct and fuzzy search results for a given word
    findings, val_findings = fuzzy_search(word, dict_new, verb_forms = verb_forms, search_values = True,
    limit_values = False, search_para = True, replace_o = True, add_levi = False)

    if len(findings) == 0:   # Case there are no direct search results in NewIsl dictionary.

        if len(val_findings) == 0:   # And case there are no fuzzy search results in NewIsl dictionary.

                if len(word) > 6:    # If the word is long enough, let's suggest it is compounded and search again but it's first part.
                    findings_part, val_findings_part = fuzzy_search(word[:4], dict_new, verb_forms = verb_forms,
                    search_values = True, limit_values = False, search_para = True, replace_o = True, add_levi = False)

                    if len(findings_part) or len(val_findings_part) > 0:    # If the first partial search brings some result, return it.
                        findings = findings_part
                        val_findings = val_findings_part
                        for value in val_findings:  # Append fuzzy search results to direct search results, such that direct search results go first.
                            if value not in findings:
                                findings.append(value)
                        return "Не найдено \"{input_word}\". {length} {res_form} нечеткого поиска для \"{part_word}\" в \"{input_word}\":".format(
                            input_word = word,
                            length = str(len(findings)),
                            res_form = "результат" if str(len(val_findings))[-1] == "1" else "результата" if str(len(findings))[-1] in ["2","3","4"]  else "результатов",
                            part_word = word[:4]), findings, 1

                    else:    # Case the first partial search doesn't bring any result, go to the second search with first 3 letters.
                        findings_part, val_findings_part = fuzzy_search(word[:3], dict_new, verb_forms = verb_forms,
                        search_values = True, limit_values = False, search_para = True, replace_o = True, add_levi = False)

                        if len(findings_part) or len(val_findings_part) > 0:    # If the second partial search brings some result, return it.
                            findings = findings_part
                            val_findings = val_findings_part
                            for value in val_findings:  # Append fuzzy search results to direct search results, such that direct search results go first.
                                if value not in findings:
                                    findings.append(value)
                            return "Не найдено \"{input_word}\". {length} {res_form} нечеткого поиска для \"{part_word}\" в \"{input_word}\":".format(
                                input_word = word,
                                length = str(len(findings)),
                                res_form = "результат" if str(len(val_findings))[-1] == "1" else "результата" if str(len(findings))[-1] in ["2","3","4"]  else "результатов",
                                part_word = word[:3]), findings, 1

                        else:   # Case none partial search bring any result, return empty result.
                            return "Нет результатов нечеткого поиска для \"{}\".".format(word), findings, 0

                else:   # Case the word is not long enough to be compounded and no search results for it, return empty result.
                    return "Нет результатов нечеткого поиска для \"{}\".".format(word), findings, 0

        else:    # Case there are fuzzy search results in NewIsl dictionary, but there are no direct search results
            return "{length} {res_form} нечеткого поиска для \"{input_word}\"".format(
            res_form = "результат" if str(len(val_findings))[-1] == "1" else "результата" if str(len(findings))[-1] in ["2","3","4"]  else "результатов",
            length = len(val_findings), input_word = word), val_findings, 1

    else:    # Case there are direct search results in NewIsl  dictionary
        for value in val_findings:  # Append fuzzy search results to direct search results, such that direct search results go first.
            if value not in findings:
                findings.append(value)
        return "{length} {res_form} нечеткого поиска для \"{input_word}\":".format(
            res_form = "результат" if str(len(findings))[-1] == "1" else "результата" if str(len(findings))[-1] in ["2","3","4"]  else "результатов",
            length = len(findings), input_word = word), findings, 1
