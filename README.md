# CSC_Assignment2: Sentence Reconstruction

## 1. Scope and Goals
#### 1) Goals
In this assignment, a text file containing quantities of lines of sentences, with all the whitespaces missing, is given. Based on another file containing most of the words appearing in those sentences (one word per line), a programme is designed to restored the sentences as much as possible by adding whitespace in proper position. 

#### 2) Scope
Here are some requirements for the reconstruction:

**a. The sentences should be read and wrote in fixed order. In the new file, each line contain one sentence.
b. Some sentences in which all the words can be found in the word file should be restored by adding whitespaces between words.
c. Some sentences in which some words cannot be found in the word file should be returned as how it is read from the initial file.
d. Punctuation marks should be separated by whitespaces according to writing convention properly.**

## 2. Programming Solution
#### 1) Modules Import
Modules `re` is imported:
```
import re
```

#### 2) Functions Design
Seven functions are designed for the reconstruction.

**a.** `splitRemainder(sentence, new_word)`
This function is designed to split out every word which can be found in the word file. Each word is string-typed and put in a list, which representing one specified sentence. And this list, as one possible separation of the raw sentence, will be stored in another list `possible_sentences`. 
Then a `while` loop is applied. `re.match` is used to find word from the beginning of the raw sentence. If any word matches, the word would be separated from the sentence and the remainder with the word would be stored in a list as possible separation. For each round, a list `previous_sentences` is used to keep the previous possible ones and the function will match from the beginning of the remainder in every possible list. If no word matches, this list will not be added to the `possible_sentences`. The loop will break when there is no possible list in `possible_sentences` :
```Python
if possible_sentences == [] or isfinished(possible_sentences, words):
    break
return possible_sentences
```
or the raw sentence has been split into words completely. A function `isfinished(possible_sentences, words)` is used to check if it is split completely, which will be explained later. 
This function returns a list containing some list of strings.

**b.** `isfinished(list_of_sentences, words)`
This function is to check if the raw sentence is split completely. It checks the last string of every list containing possible separation in the list`possible_sentences`. If all the last strings can be found in the word file or the last string is a punctuation mark, the function returns `True`.

```Python
def isfinished(list_of_sentences, words):
    for sentence in list_of_sentences:
        if sentence[-1] not in words and re.fullmatch('\W+', sentence[-1]) == None:
            return False
    return True
```

**c.** `splitRemainder(sentence, new_word)`
This function is to separate the word found from the remainder and put them in the end of the previous possible separation. It is used in the function `splitRemainder(sentence, new_word)`. If punctuation marks are found at the beginning of the remainder, they will also be separated as a string.

**d.** `concatenateWords(word_list, connecter)`
This function is defined to connect every string in a list with a whitespace. Since it is applied on the separation of the raw sentence, it could connect every word, including the punctuation marks, with whitespace as delimiter. Finally, it returns a string.

**e.** `checkPunctuation(sentence)`
Since, after using `concatenateWords(word_list, connecter)`, some punctuation marks are not in proper position, such as `i am kind , but not cute .`, which should conventionally be `i am king, but not cute.`. So this function is designed for correcting those punctuation marks' positions, by removing the whitespace before them or behind them or both. According to some characteristics of this sentence file, four pattern are applied to match:
```Python
return re.sub('\s([\.,;:!?])', r'\1', 
    re.sub('\s-\s', '-', 
    re.sub('\(\s(.+)\s\)', r'(\1)', 
    re.sub('''(["'])\s(.+)\s(["'])''', r'''\1\2\3''', sentence))))
```

**f.** `reconstruction(raw_sentences, words)`
This function integrate those mentioned above and offer a process of reconstructing raw sentences: check if the raw sentence can be split; if it can, split it, reconnect it with whitespaces, and modify the punctuation marks; if not, return the raw sentence and put it into the list.

**g.** `writeIntoFile(seq)`
This function use `file.writelines(seq)` to write every string-typed sentence, which has been already restored, into a new file, namely, 'restored_sentences.txt'.

#### 3) Startup Design
After defining the functions above, the programme can be started by the following option:
```Python
if __name__ == '__main__':
    initial_sentences = [line.strip() for line in open('sentence.txt', 'r')]
    words = set([line.strip() for line in open('word.txt', 'r')])
    new_sentences = reconstruction(initial_sentences, words)
    writeIntoFile(new_sentences)
```
The codes deliver such instructions: read in the sentences and words and put them in separate lists (for the words, `set()` is used to disable the frequency of words, making each of them unique); reconstruct the sentences using `reconstruction(initial_sentences, words)` (see the description above in **Functions Design**) and put them in a new list; write all the strings in the new list to a new file, one string (sentence) per line.


## 3. Limitation and Enhancement
#### 1) Composite Words
It is found that some composite words make it hard to split the sentence which contains them. For instance, 'under', 'graduate', and 'undergraduate' are in the word file and hence it will be in dilemma when splitting any sentence containing the substring 'undergraduate'. Actually, for this situation, the function `splitRawSentence(initial_sentence, words)` will return all possible separations of the raw sentence, such as `[... 'under', 'graduate', ...]` and `[... 'undergraduate', ...]`. For simplification, only one possibility is chosen to represent the restored sentence. So the programme can be designed to return one possibility, with other possibilities in a following bracket, like '......undergraduate (under graduate)......', for better reference for readers.

#### 2) Punctuation
Only four kinds of situation have been considered when checking and modifying the punctuation in this programme, since the sentence file contains simple and elementary usage of punctuation marks. In face, arranging these marks can be challenging due to complicated combinations of themselves and various usage conventions. Hence, more pattern should be added to the regular expression in the function `checkPunctuation(sentence)` to make it sophisticated enough to handle all kinds of situation.

