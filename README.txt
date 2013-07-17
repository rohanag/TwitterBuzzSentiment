Rohan Agrawal, ra2616
Nandita Rao, nr2445

Cloud Assignment 3
==================

Design
------

Preprocessing
--------------------

1. Tweets are recovered using the geocode API and the twitter API, all of the tweets are encoded into the utf-8 format to avoid any problems with internet encoding.

2. Then special characters like ',' , ' ' ' and '/' are filtered out.

3. Tokenization is done based on spaces.

4. Stopwords are removed. These words are very common words and have no bearing on the meaning of the sentence, hence they can be taken out of the processing. List of stopwords taken from http://norm.al/2009/04/14/list-of-english-stop-words/ and http://www.textfixer.com/resources/common-english-words.txt

5. Then all words with symbols are removed, for example, words like '@username'.

6. All words of length lesser than 1 are also removed.

7. Then words are stemmed using the porter stemmer algorithm using code from http://tartarus.org/martin/PorterStemmer/python.txt

8. The steps described above are part of text preprocessing. All processing for buzzword extraction and sentiment analysis are done on these preprocessed words.

Buzzword Extraction
-----------------------

1. For ranking buzzwords, I have used the following evaluation metric, 
   BuzzwordScore(word) = frequency of word in the tweets * tweet frequency , where tweet frequency is the number of tweets in which the word appears. This is the opposite of tf-idf term weighting, because in tf-idf weights, we discourage words that appear across all documents. But in our case, we want words that appear across many tweets, that would represent buzzwords in the group of tweets. 
   
2. All of the words in the set of tweets is then sorted based on this BuzzwordScore and the top 10 words are returned as Buzzwords.

3. All of the tweets are parsed and if the tweet contains a buzzword, it is added to the list of tweets associated with that Buzzword.
   
Sentiment Analysis
-----------------------

1. Each tweet related to a buzzword is parsed, each word in the tweet is scored according the scores given in http://neuro.imm.dtu.dk/wiki/AFINN

2. The sum of the scores of each word for a particular buzzwords is calculated.

3. In addition to the above score, swing words are also taken into account. For, e.g. negation words like 'not' , 'isn't' change the sentiment of the words that appear after it. Therefore, words that appear in proximity (distance of 3) from the swingwords, have their sentiment negated. The proximity of the effect of the negation words was taken to be 3 for simplicity, as calculating the scope of these words is a research topic in itself.

4. In addition to the above calculation, We have also factored in smiley's to the sentiment score calculation. If happy smileys like :) , :] appear in the tweet, its sentiment score is biased towards positive, and sad smileys make the score go negative.

5. The final score is then mapped to a sentiment, if the score is less than -6, it is tagged as very negative, if the score is greater than 6, the tweet is tagged as very positive. If the score is between -6 and -3, it is tagged as negative, between 3 and 6 is tagged as positive, otherwise neutral.

Link for the app 
-----------------------

The application has been deployed on google app engine and can be found at the following link :

http://nr2445-ra2616-cloudassignment3.appspot.com/