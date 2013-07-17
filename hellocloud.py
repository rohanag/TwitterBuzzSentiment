'''
good test cases
washington fun
'''
from __future__ import division
import porter
import cgi
import datetime
import urllib
import webapp2
import urllib
import json as simplejson
from re import split

from collections import defaultdict
from google.appengine.ext import db
from google.appengine.api import users
from pygeocoder import Geocoder

'''
Initializing the porter stemmer object
'''
stemObj = porter.PorterStemmer()
stemmedWords = {}


    
    
class Tweet(db.Model):
    """Models an individual Guestbook entry with author, content, and date."""
    location = db.StringProperty(multiline=True)
    category = db.StringProperty(multiline=True)
    tweetId = db.StringProperty(multiline=True)
    fromUser = db.StringProperty(multiline=True)
    fromUserName = db.StringProperty(multiline=True)
    createdAt = db.StringProperty(multiline=True)
    tweetText = db.StringProperty(multiline=True)
    imageURL = db.StringProperty(multiline=True)


class MainPage(webapp2.RequestHandler):
    def getStopWords(self):
        ''' returns the list of stopwords '''
        stopwords = ['a','able','about','across','after','all','almost','also','am','among','an','and','any','are','as','at','be','because','been','but','by','can','could','dear','did','do','does','either','else','ever','every','for','from','get','got','had','has','have','he','her', 'here', 'hers','him','his','how','however','i','if','in','into','is','it','its','just','least','let','like','likely','may','me','might','most','must','my','of','off','often','on','only','or','other','our','own','rather','said','say','says','she','should','since','so','some','than','that','the','their','them','then','there','these','they','this','tis','to','too','twas','us','wants','was','we','were','what','when','where','which','while','who','whom','why','will','with','would','yet','you','your', 'make', 'damn']
        stopwords2 = ['a','as','able','about','above','according','accordingly','across','actually','after','afterwards','again','against','ain','aint','all','allow','allows','almost','alone','along','already','also','although','always','am','among','amongst','an','and','another','any','anybody','anyhow','anyone','anything','anyway','anyways','anywhere','apart','appear','appreciate','appropriate','are','around','as','aside','ask','asking','associated','at','available','away','awfully','be','became','because','become','becomes','becoming','been','before','beforehand','behind','being','believe','below','beside','besides','best','better','between','beyond','both','brief','but','by','cmon','cs','came','can','cant','can','cant','cause','causes','certain','certainly','changes','clearly','co','com','come','comes','concerning','consequently','consider','considering','contain','containing','contains','corresponding','could','course','currently','definitely','described','despite','did','didnt','different','do','does','doing','done','down','downwards','during','each','edu','eg','eight','either','else','elsewhere','enough','entirely','especially','et','etc','even','ever','every','everybody','everyone','everything','everywhere','ex','exactly','example','except','far','few','fifth','first','five','followed','following','follows','for','former','formerly','forth','four','from','further','furthermore','get','gets','getting','given','gives','go','goes','going','gone','got','gotten','greetings','had','happens','hardly','has','have','having','he','hes','hello','help','hence','her','here','heres','hereafter','hereby','herein','hereupon','hers','herself','hi','him','himself','his','hither','hopefully','how','howbeit','however','id','ill','im','ive','ie','if','ignored','immediate','in','inasmuch','inc','indeed','indicate','indicated','indicates','inner','insofar','instead','into','inward','is','it','itd','itll','its','its','itself','just','keep','keeps','kept','know','knows','known','last','lately','later','latter','latterly','least','less','lest','let','lets','like','liked','likely','little','look','looking','looks','ltd','mainly','many','may','maybe','me','mean','meanwhile','merely','might','more','moreover','most','mostly','much','must','my','myself','name','namely','nd','near','nearly','necessary','need','needs','nevertheless','new','next','nine','nobody','non','noone','normally','novel','now','obviously','of','off','often','oh','ok','okay','old','on','once','one','ones','only','onto','or','other','others','otherwise','ought','our','ours','ourselves','out','outside','over','overall','own','particular','particularly','per','perhaps','placed','please','plus','possible','presumably','probably','provides','que','quite','qv','rather','rd','re','really','reasonably','regarding','regardless','regards','relatively','respectively','right','said','same','saw','say','saying','says','second','secondly','see','seeing','seem','seemed','seeming','seems','seen','self','selves','sensible','sent','serious','seriously','seven','several','shall','she','should','since','six','so','some','somebody','somehow','someone','something','sometime','sometimes','somewhat','somewhere','soon','sorry','specified','specify','specifying','still','sub','such','sup','sure','ts','take','taken','tell','tends','th','the','than','thank','thanks','thanx','that','thats','thats','the','their','theirs','them','themselves','then','thence','there','theres','thereafter','thereby','therefore','therein','theres','thereupon','these','they','theyd','theyll','theyre','theyve','think','third','this','thorough','thoroughly','those','though','three','through','throughout','thru','thus','to','together','too','took','toward','towards','tried','tries','truly','try','trying','twice','two','un','under','unfortunately','unless','unlikely','until','unto','up','upon','us','use','used','useful','uses','using','usually','value','various','very','via','viz','vs','want','wants','was','wasnt','way','we','wed','well','were','weve','welcome','well','went','were','werent','what','whats','whatever','when','whence','whenever','where','wheres','whereafter','whereas','whereby','wherein','whereupon','wherever','whether','which','while','whither','who','whos','whoever','whole','whom','whose','why','will','willing','wish','with','within','without','wonder','would','would','yes','yet','you','youd','youll','youre','youve','your','yours','yourself','yourselves','zero']
        ''' twitter specific special stopwords '''
        content_stopwords = ['http', 'rt', 'co', 'de', 'isn', 'gt', 'la' , 'lt', 'via', 'amp', 'plz', 'en'] 
        stopwords.extend(stopwords2)
        stopwords.extend(content_stopwords)
        return stopwords
    
    def getSwingWords(self):
        ''' returns the list of swing words '''
        return ['no','nor', 'not', 'neither', 'never', 'nothing', 'nowhere', 'none', 'havent', 'hasnt', 'hadn', 'hadnt' , 'cannot', 'couldnt', 'shouldn', 'shouldnt', 'wont', 'dont', 'wouldnt', 'doesnt', 'isnt', 'arent']
        
    def stemList(self, swingwords):
        ''' stems the list of swingwords '''
        return [stemObj.stem(word,0,len(word)-1) for word in swingwords]
        
    def getDocumentFrequency(self, word, tweetList):
        ''' get document frequency, i.e the number of tweets that contains the given word '''
        freq = 0
        for text, _ in tweetList:
            if word in text:
                freq+=1
        return freq
            
            
    def get_scores(self, scoreFile):
        ''' get sentiment scores from the file scoreFile AFINN-111.txt '''
        file = open(scoreFile)
        scores = defaultdict(int)
        for row in file:
            if len(row.split()) == 2:
                word, score = row.split()
                word = word.strip().lower()
                word = stemObj.stem(word,0,len(word)-1)
                score = int(score)
                scores[word] = score
        return scores
        
    def return_sentiment(self, score):
        ''' based on the score, return sentiment '''
        V_POS = 6
        POS = 3
        NEUTRAL = 0
        NEG = -3
        V_NEG = -6
        if score >= V_POS:
            return 'very positive'
        if score <= V_NEG:
            return 'very negative'
        if score >= POS:
            return 'positive'
        if score <= NEG:
            return 'negative'
        return 'neutral'
        
    def do_sentiment_analysis(self, tweet_by_category, swingwords, internethappywords, internetsadwords):
        '''performs the main sentiment analysis, using the scores from AFINN-111, internet happy words, sad words and swingwords '''
        scores = self.get_scores('AFINN-111.txt')
        sentiments = []
        
        for cat in tweet_by_category:
            cat_score = 2*scores[cat]
            for pre_pro_tweet, tweetObj in tweet_by_category[cat]:
                swingScope = 3
                swingIndex = -4
                for i,words in enumerate(pre_pro_tweet):
                    if words in swingwords:
                        swingIndex = i
                    if swingIndex + swingScope > i:
                        #self.response.write('<p>%s %s %d</p>' % ("negatedddddd", pre_pro_tweet, swingIndex))
                        cat_score -= scores[words]
                    else:
                        cat_score += scores[words]
                text = tweetObj[0]
            for terms in internethappywords:
                if terms in text:
                    cat_score += 2
            for terms in internetsadwords:
                if terms in text:
                    cat_score -= 2
            
            sentiments.append([cat, self.return_sentiment(cat_score)])
        return sentiments

    def categorize_tweets(self, popular_words, number_of_categories, tweetList):
        ''' categorizes tweets given a list of popular words '''
        res = defaultdict(list)
        for (t,tweetText) in tweetList:
            for popwords in popular_words:
                if popwords in t:
                    res[popwords].append([t,tweetText])
        return res

                    
    def preprocess(self, words, stopwords):
        ''' does the preprocessing as described in the README '''
        global stemmedWords
        words = words.encode('utf-8')
        if words == None or words == '':
            return ['']
        words = words.replace('\'','').replace(',',' ').replace('.',' ')
        temp = words.lower().split()
        temp = [w for w in temp if w not in stopwords]
        temp = [w for w in temp if str.isalpha(str(w))]
        temp = [w for w in temp if len(w) > 1]
        ret = []
        for w in temp:
           stemmed = stemObj.stem(w,0,len(w)-1)
           ret.append(stemmed)
           stemmedWords[stemmed] = w
        return [x for x in ret if x not in stopwords]

    def get(self):
        self.response.write('<html><body style="font-family:calibri;color:blue;i;background-color:lightcyan;"><h1>What\'s on your mind twitter?</h1>')
        self.response.write("""<b><font size = "4" >Enter the location in the first dialog box and the category in the next:</font></b>
        <form method = "post">
        <input type = "textarea" name = "location"></input>
        <input type = "textarea" name = "category"></input>
        <input type = "submit" ></input>
        </form>""")

        self.response.write('</body></html>')
		
    def post(self):
        stopwords = self.getStopWords()
        swingwords = self.stemList(self.getSwingWords())
        internethappywords = ['lol', 'lolz', 'rofl', 'lmao', 'roflmao', ':)', ':D', '=D', ':]', ':-)', ':-))', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D', '=-3', '=3', 'B^D', ';-)', ';)', '*-)', '*)', ';-]', ';]', ';D', ';^)', ':-,']
        internetsadwords = ['wtf', '>:[', ':-(', ':(',  ':-c', ':c', ':-<',  ':<', ':-[', ':[', ':{', ':\'-(', ':\'(', '>:\\', '>:/', ':-/', ':-.', ':/', ':\\', '=/', '=\\', ':L', '=L', ':S', '>.<']
        
        tweetList = []
        self.response.write('<html><body style="font-family:calibri;color:blue;i;background-color:lightcyan;"><h1>What\'s on your mind twitter?</h1>')
		
        location = self.request.get('location')
        try:
            '''Using pygeocoder to get the latitude and longitude'''
            results = Geocoder.geocode(location)
        except:
            self.response.write('<p>%s</p>' % "Location Not Found!!!")
            return

        strs = results[0].coordinates
        latitude =  strs[0]
        longitude = strs[1]
        		
        searchTerm = self.request.get('category')
        stopwords.extend(searchTerm.lower().split())
        if " " in searchTerm:
		    category = searchTerm.split(" ")
		    userCategory = "%20".join(category)
           
        else:
            userCategory = searchTerm
        
        '''Query to get data from database if it already exists'''
        tweets = db.GqlQuery("SELECT * "
                                "FROM Tweet "
                                "WHERE category = :1 AND location = :2",
                                searchTerm,location)

        strs2 = "There are no existing records hence fetching new data from twitter"
        strs4 = "Data already exists hence retreiving the tweets from database"
		
        '''Fetching from twitter if data not is not already present in database, and inserting into the database'''
        if tweets.count(1) == 0:
            self.response.write('<p>%s</p>' %strs2)
            
            search = urllib.urlopen("http://search.twitter.com/search.json?q="+userCategory+"&rpp=100&include_entities=true&result_type=mixed&geocode:"+repr(latitude)+","+repr(longitude)+",25mi" + '&lang%3Aen')
            dict = simplejson.loads(search.read())
            strs1="No tweets found!!! Search for something better!!"

            if not dict["results"]:
                self.response.write('<p>%s</p>' % strs1)
                return
            uniqueTweets = []
            for result in dict["results"]: # result is a list of dictionaries
                text =result["text"]
                fromUser = result["from_user"]
                fromUserName = result["from_user_name"]
                userId = result["from_user_id_str"]
                createdAt =result["created_at"]
                imageURL = result["profile_image_url"]
                language = result["iso_language_code"]
                if language == 'en':
                    if text not in uniqueTweets:
                        uniqueTweets.append(text)
                        self.tweet = Tweet()
                        self.tweet.location = location
                        self.tweet.category = searchTerm
                        self.tweet.tweetId = userId
                        self.tweet.fromUser = fromUser
                        self.tweet.fromUserName = fromUserName
                        self.tweet.createdAt = createdAt
                        self.tweet.tweetText = text
                        self.tweet.imageURL = imageURL
                        self.tweet.put()
                        tweetList.append([self.preprocess(text, stopwords), [text, fromUser, fromUserName, userId, createdAt, imageURL]])
                        
        else:
            self.response.write('<p>%s</p>' %strs4)
            for tweet in tweets:
                tweetList.append([self.preprocess(tweet.tweetText, stopwords), [tweet.tweetText, tweet.fromUser, tweet.fromUserName, tweet.tweetId, tweet.createdAt, tweet.imageURL]])                
        freq = defaultdict(int)        
        for (tweet, _) in tweetList:
            for word in tweet:
                freq[word] += 1
        ''' for each word , get document frequency too, dont invert it, cos we want the buzz word to be present in most documents '''
        for word in freq:
            freq[word] *= self.getDocumentFrequency(word, tweetList)
        
        popular_words = sorted(freq, key = freq.get, reverse = True)
        popular_words = [w for w in popular_words if w not in swingwords]
        if len(popular_words) > 10:
            popular_words = popular_words[:10]
        number_of_categories = len(popular_words)
                
        tweet_by_category = self.categorize_tweets(popular_words, number_of_categories, tweetList)
        sentiments = self.do_sentiment_analysis(tweet_by_category, swingwords, internethappywords, internetsadwords)
        for cat in tweet_by_category:
            for tweet,senti in sentiments:
                if(cat == tweet):
                    self.response.write('<br>')
                    self.response.write('<hr>')
                    self.response.write('<p><b><font size = "4">Buzz:</font></b> <i>%s</i> <b><font size = "4">Sentiment:</font></b><i> %s</i></p>' % (stemmedWords[tweet], senti))
                    break
            self.response.write('<table border="1">')
            self.response.write('<tr><th>Tweet</th><th>Twitter Handle</th><th>UserName</th><th>Created At</th><th>Image</th>')
            for (_, tweetText) in tweet_by_category[cat]:
                text1, fromUser1, fromUserName1, userId1, createdAt1, imageURL1 = tweetText
                self.response.write('<tr><td>%s</td>' % cgi.escape(text1))
                self.response.write('<td>%s</td>' % cgi.escape(fromUser1))
                self.response.write('<td>%s</td>' % cgi.escape(fromUserName1))
                self.response.write('<td>%s</td>' % cgi.escape(createdAt1.rstrip('0+')))
                self.response.write('<td><img src =%s></img></td></tr>' % cgi.escape(imageURL1))
            self.response.write('</table>')
        self.response.write('</body></html>')

        

app = webapp2.WSGIApplication([('/', MainPage)],
                              debug=True)