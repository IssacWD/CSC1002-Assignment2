import re

def splitRemainder(sentence, new_word):                                                          # A function for separating the new-matched word from the remainder string
    a = len(new_word)
    if re.match('\W+', sentence[-1][a:]):
        punc = re.match('\W+', sentence[-1][a:]).group()
        b = len(punc)
        if len(sentence[-1]) == a + b:
            return sentence[:-1] + [new_word, punc]                                              # Return the new word and the punctuation mark if only the mark is left after separating
        return sentence[:-1] + [new_word, punc, sentence[-1][a+b:]]                              # Return the new word, the punctuation mark, and the remainder
    return sentence[:-1] + [new_word, sentence[-1][a:]]                                          # Return the new word and the remainder if no punctuation mark in the comming position

def isfinished(list_of_sentences, words):                                                        # A function for checking if the all the sentences in a list are splited into words completely
    for sentence in list_of_sentences:
        if sentence[-1] not in words and re.fullmatch('\W+', sentence[-1]) == None:
            return False
    return True

def splitRawSentence(initial_sentence, words):                                                   # A function that separates every word in a string-typed raw sentence and put them into a list
    possible_sentences = [[initial_sentence]]
    while True:
        previous_sentences = possible_sentences
        possible_sentences = []                                                                  # This is a list keeping some lists, each of which contains a possible separation of the raw sentence
        for sentence in previous_sentences:
            if re.fullmatch('\W+', sentence[-1]) or sentence[-1] in words :
                possible_sentences.append(sentence)
            else:
                for word in words:
                    new_word = re.match(word, sentence[-1], re.I)
                    if new_word:
                        possible_sentences.append(splitRemainder(sentence, new_word.group()))
        if possible_sentences == [] or isfinished(possible_sentences, words):                    # When there is any word that is not in the word list, or the raw sentence is splited completely, the loop will break
            break
    return possible_sentences

def concatenateWords(word_list, connecter):                                                      # A function for concatenating the words in a list with the delimiter being whitespace.
    return connecter.join(word_list)

def checkPunctuation(sentence):                                                                  # A function for modifying the punctuation marks, using regular expression to match specified marks.
    return re.sub('\s([\.,;:!?])', r'\1', 
        re.sub('\s-\s', '-', 
        re.sub('\(\s(.+)\s\)', r'(\1)', 
        re.sub('''(["'])\s(.+)\s(["'])''', r'''\1\2\3''', sentence))))

def reconstruction(raw_sentences, words):                                                        # A function for reconstructing a list of string-typed raw sentences.
    restored_sentences = []
    for sentence in raw_sentences:
        splited_sentences = splitRawSentence(sentence, words)                                    # Break it into words
        if splited_sentences == []:
            restored_sentences.append(sentence)                                                  # If any word not in the word list, return the raw sentence.

        else:
            conected_sentence = concatenateWords(splited_sentences[0], ' ')                      # Concatenate the words, and punctuation marks, with whithspace.
            restored_sentence = checkPunctuation(conected_sentence)                              # Correct the position of punctuation marks.
            restored_sentences.append(restored_sentence)                                         # Store them in a list.
    return restored_sentences

def writeIntoFile(seq):                                                                          # A function for writing a list of strings in a new file, one string per line.
    lines = map(lambda x: x + '\n', seq)
    f = open('restored_sentences.txt', 'w')
    f.writelines(lines)

if __name__ == '__main__':
    initial_sentences = [line.strip() for line in open('sentence.txt', 'r')]                     # Read the sentences into a list.
    words = set([line.strip() for line in open('word.txt', 'r')])                                # Read the words into a list.
    new_sentences = reconstruction(initial_sentences, words)                                     # Put the restored sentences into a new list.
    writeIntoFile(new_sentences)                                                                 # Write them into a new flie, one sentence per line.