import re

def search_word(word, saga_texts_on, saga_texts_ru):
    ''' Search for word entrance in Old-Norse texts and return corresponding Old-Norse and Russian paragraphs
        where this word could be found.

        Parameters:
        1. word - the Old-Norse word or lemma to search;
        2. saga_texts_on - corpus of Old-Norse texts in the form of dictionary, where each key is a name of song,
        such as "hyndlu", and value is a dictionary with keys as numbers of paragraphs, and values as corresponding texts itself.
        Meta-information, such as song name, url and source, is also provided in the inner dicitionary key-value pairs.
        3. saga_texts_ru - corpus of corresponding to saga_texts_on Russian texts. The structure and objective are the same as
        the ones for saga_texts_on parameter.

    '''
     # Create a set of short song names, without any language postfix, such as "hyndlu".
    edda_song_names = saga_texts_on.keys()

    # Normalize input word
    search_word = word.lower().strip()

    text_blocks = []

    for song_name in edda_song_names:
        dict_isl = saga_texts_on[song_name]
        dict_rus = saga_texts_ru[song_name]

        for paragraph, text in dict_isl.items():
            # Normalize Old-Norse text
            text_norm = re.sub(r"[«»,:.;!?—\[\]()]", " ", text.lower())

            # Search for the word itself, not as for the part of another word
            if " " + search_word +  " " in text_norm and paragraph not in ["text_name", "song_name", "source", "link"]:

                block_title = dict_isl["song_name"] + ". " + dict_rus["song_name"] + ': ' + paragraph
                block_isltext = "<span>" + text + "</span>"
                block_isllink = ("<a href=\"{}\" target=\"_blank\">".format(dict_isl["link"] + "#" + paragraph) +
                dict_isl["link"] + "</a>")
                block_rustext = dict_rus[paragraph]
                block_ruslink = ("<a href=\"{}\" target=\"_blank\">".format(dict_rus["link"] + "#" + paragraph) +
                dict_rus["link"] + "</a>")
                block_source = dict_isl["source"] + ' ' + dict_rus["source"]

                text_block = [block_title, block_isltext, block_isllink, block_rustext, block_ruslink, block_source]

                text_blocks.append(text_block)


    return text_blocks
