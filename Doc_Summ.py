import re
import nltk
import textract as txt
import requests as req
#import speech_recognition as sr
import heapq as hp
import requests as req
from bs4 import BeautifulSoup as Bs

class Doc_Summ:

    url = ''
    scraped_content = ''
    refined_text_content = ''
    sentence_token = ''
    word_token = ''
    word_frequency = {}
    sentence_score = {}

    '''def speech_text(self):
        #vid_aud = 'ffmpeg -i https://youtu.be/pfonnzvxLvE aud.mp3'
        aud_wav = 'ffmpeg -i C:\\Users\\admin\\Downloads\\alan-walker-on-my-way-xH1ItQmf7.mp3 C:\\Users\\admin\\Downloads\\alan-walker-on-my-way-xH1ItQmf7.wav'
        #os.system(vid_aud)
        os.system(aud_wav)
        r = sr.Recognizer()
        aud = sr.AudioFile('C:\\Users\\admin\\Downloads\\alan-walker-on-my-way-xH1ItQmf7.wav')
        audio = r.record(source='C:\\Users\\admin\\Downloads\\alan-walker-on-my-way-xH1ItQmf7.mp3', duration=100)
        print(r.recognize_google(audio))'''

    #def __init__(self, *args, **kwargs):

    def set_url(self, url):
        print(type(url))
        self.url = url
        self.web_scraping()

    def txt_sum(self):
        self.scraped_content = str(txt.process(filename="F:\\DBMS\\PR1\\PR1.odt"))
        print(self.scraped_content)
        self.text_cleaning()

    def set_text(self):
        self.scraped_content = '''History and relationships to other fields
See also: Timeline of machine learning
Arthur Samuel, an American pioneer in the field of computer gaming and artificial intelligence, coined the term "Machine Learning" in 1959 while at IBM.[8] A representative book of the machine learning research during the 1960s was the Nilsson's book on Learning Machines, dealing mostly with machine learning for pattern classification.[9] The interest of machine learning related to pattern recognition continued during the 1970s, as described in the book of Duda and Hart in 1973. [10] In 1981 a report was given on using teaching strategies so that a neural network learns to recognize 40 characters (26 letters, 10 digits, and 4 special symbols) from a computer terminal. [11] As a scientific endeavor, machine learning grew out of the quest for artificial intelligence. Already in the early days of AI as an academic discipline, some researchers were interested in having machines learn from data. They attempted to approach the problem with various symbolic methods, as well as what were then termed "neural networks"; these were mostly perceptrons and other models that were later found to be reinventions of the generalized linear models of statistics.[12] Probabilistic reasoning was also employed, especially in automated medical diagnosis.[13]:488

However, an increasing emphasis on the logical, knowledge-based approach caused a rift between AI and machine learning. Probabilistic systems were plagued by theoretical and practical problems of data acquisition and representation.[13]:488 By 1980, expert systems had come to dominate AI, and statistics was out of favor.[14] Work on symbolic/knowledge-based learning did continue within AI, leading to inductive logic programming, but the more statistical line of research was now outside the field of AI proper, in pattern recognition and information retrieval.[13]:708–710; 755 Neural networks research had been abandoned by AI and computer science around the same time. This line, too, was continued outside the AI/CS field, as "connectionism", by researchers from other disciplines including Hopfield, Rumelhart and Hinton. Their main success came in the mid-1980s with the reinvention of backpropagation.[13]:25

Machine learning, reorganized as a separate field, started to flourish in the 1990s. The field changed its goal from achieving artificial intelligence to tackling solvable problems of a practical nature. It shifted focus away from the symbolic approaches it had inherited from AI, and toward methods and models borrowed from statistics and probability theory.[14] It also benefited from the increasing availability of digitized information, and the ability to distribute it via the Internet.

Relation to data mining
Machine learning and data mining often employ the same methods and overlap significantly, but while machine learning focuses on prediction, based on known properties learned from the training data, data mining focuses on the discovery of (previously) unknown properties in the data (this is the analysis step of knowledge discovery in databases). Data mining uses many machine learning methods, but with different goals; on the other hand, machine learning also employs data mining methods as "unsupervised learning" or as a preprocessing step to improve learner accuracy. Much of the confusion between these two research communities (which do often have separate conferences and separate journals, ECML PKDD being a major exception) comes from the basic assumptions they work with: in machine learning, performance is usually evaluated with respect to the ability to reproduce known knowledge, while in knowledge discovery and data mining (KDD) the key task is the discovery of previously unknown knowledge. Evaluated with respect to known knowledge, an uninformed (unsupervised) method will easily be outperformed by other supervised methods, while in a typical KDD task, supervised methods cannot be used due to the unavailability of training data.

Relation to optimization
Machine learning also has intimate ties to optimization: many learning problems are formulated as minimization of some loss function on a training set of examples. Loss functions express the discrepancy between the predictions of the model being trained and the actual problem instances (for example, in classification, one wants to assign a label to instances, and models are trained to correctly predict the pre-assigned labels of a set of examples). The difference between the two fields arises from the goal of generalization: while optimization algorithms can minimize the loss on a training set, machine learning is concerned with minimizing the loss on unseen samples.[15]

Relation to statistics
Machine learning and statistics are closely related fields in terms of methods, but distinct in their principal goal: statistics draws population inferences from a sample, while machine learning finds generalizable predictive patterns.[16] According to Michael I. Jordan, the ideas of machine learning, from methodological principles to theoretical tools, have had a long pre-history in statistics.[17] He also suggested the term data science as a placeholder to call the overall field.[17]

Leo Breiman distinguished two statistical modeling paradigms: data model and algorithmic model,[18] wherein "algorithmic model" means more or less the machine learning algorithms like Random forest.

Some statisticians have adopted methods from machine learning, leading to a combined field that they call statistical learning.[19]

Theory
Main articles: Computational learning theory and Statistical learning theory
A core objective of a learner is to generalize from its experience.[2][20] Generalization in this context is the ability of a learning machine to perform accurately on new, unseen examples/tasks after having experienced a learning data set. The training examples come from some generally unknown probability distribution (considered representative of the space of occurrences) and the learner has to build a general model about this space that enables it to produce sufficiently accurate predictions in new cases.

The computational analysis of machine learning algorithms and their performance is a branch of theoretical computer science known as computational learning theory. Because training sets are finite and the future is uncertain, learning theory usually does not yield guarantees of the performance of algorithms. Instead, probabilistic bounds on the performance are quite common. The bias–variance decomposition is one way to quantify generalization error.

For the best performance in the context of generalization, the complexity of the hypothesis should match the complexity of the function underlying the data. If the hypothesis is less complex than the function, then the model has under fitted the data. If the complexity of the model is increased in response, then the training error decreases. But if the hypothesis is too complex, then the model is subject to overfitting and generalization will be poorer.[21]

In addition to performance bounds, learning theorists study the time complexity and feasibility of learning. In computational learning theory, a computation is considered feasible if it can be done in polynomial time. There are two kinds of time complexity results. Positive results show that a certain class of functions can be learned in polynomial time. Negative results show that certain classes cannot be learned in polynomial time.'''
        self.text_cleaning()

    def web_scraping(self=None):
        # Web Scraping
        html_doc = req.get('https://en.wikipedia.org/wiki/Machine_learning') #'https://en.wikipedia.org/wiki/Machine_learning'
        soup = Bs(html_doc.content, 'html.parser')
        acc_ele = ['a', 'abbr', 'acronym', 'b', 'big',
                   'blockquote', 'br', 'center', 'cite', 'code', 'dd',
                   'dfn', 'dir', 'div', 'dl', 'dt', 'em',
                   'font', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'i',
                   'ins', 'kbd', 'label', 'legend', 'li', 'ol',
                   'p', 'pre', 'q', 'samp', 'small', 'span',
                   'strong', 'sub', 'sup', 'tt', 'u', 'ul', 'var', 'head', 'header', 'body', 'article', 'section']
        para_contents = soup.findAll('p')  # Extracts value in <p> tags of HTML
        for tag in soup.findAll(True):  # find all tags
            if tag.name not in acc_ele:
                tag.extract()  # remove the bad ones
        # print(para_contents)
        for contents in para_contents:
            self.scraped_content += contents.text  # Appends only the value(text) present inside <p> tags
        # print(text_content)
        #self.scraped_content = text_content
        self.text_cleaning()

    def text_cleaning(self=None):
        # Text Cleaning & Tokenizing sentences and words
        # ref_text_content = re.sub(r'\[[0-9a-zA-Z]*\]', ' ', text_content) #Subs [no] with white space
        self.refined_text_content = re.sub(r'\[.*?\]', ' ', self.scraped_content)  # Remove all the contents from square braces
        self.refined_text_content = re.sub(r'[_!#$%^*?/\|~:]', ' ', self.refined_text_content)  # Remove all the special characters
        self.refined_text_content = re.sub(r'\([^()]*\)', ' ', self.refined_text_content)  # Remove all the contents from parentheses
        self.refined_text_content = re.sub(r'\{[^{}]*\}', ' ', self.refined_text_content)  # Remove all the contents from curly braces
        self.refined_text_content = re.sub(r'\<[^<>]*\>', ' ', self.refined_text_content)  # Remove all the contents from angular braces
        self.refined_text_content = re.sub(r'\s+\/\s+', ' ', self.refined_text_content)  # Remove urls
        self.refined_text_content = re.sub(r'@\s+', ' ', self.refined_text_content)  # Remove mentions
        self.refined_text_content = re.sub(r'#\s+', ' ', self.refined_text_content)  # Remove trends
        self.refined_text_content = re.sub(r'['
                                  u'\U0001F600-\U0001F64F'  # emoticons
                                  u'\U0001F300-\U0001F5FF'  # symbols & pictographs
                                  u'\U0001F680-\U0001F6FF'  # transport & map symbols
                                  u'\U0001F1E0-\U0001F1FF'  # flags (iOS)
                                  ']+', ' ', self.refined_text_content)  # Remove emojis and symbols
        self.refined_text_content = re.sub(r'\n', ' ', self.refined_text_content)
        self.refined_text_content = re.sub(r'\t', ' ', self.refined_text_content)
        self.refined_text_content = re.sub(r'\s+', ' ', self.refined_text_content)  # Extra spaces are removed

        self.sentence_token = self.refined_text_content
        self.sentence_token = nltk.sent_tokenize(self.sentence_token)  # Tokenizing sentences

        self.refined_text_content = re.sub(r'[^a-zA-Z]', ' ', self.refined_text_content)  # Only alphabets are allowed in this text
        self.refined_text_content = re.sub(r'\s+', ' ', self.refined_text_content)  # Extra spaces are removed

        self.word_token = self.refined_text_content
        self.word_token = nltk.word_tokenize(self.word_token)  # Tokenizing words
        self.stopwords()

    def stopwords(self=None):
        # Getting stopwords
        stopwords = nltk.corpus.stopwords.words('english')
        # print(stopwords)

        # Counting freq of those unique words which are not in stopwords
        for word in self.word_token:
            if word not in stopwords:
                if word not in self.word_frequency.keys():
                    self.word_frequency[word] = 1
                else:
                    self.word_frequency[word] += 1
        # print(word_freq)

        # Finding word having max freq
        max_word_freq = max(self.word_frequency.values())
        # print(max_word_freq)

        # Dividing freq of every word with the freq of max freq word
        for word in self.word_frequency.keys():
            self.word_frequency[word] /= max_word_freq
        # print(word_freq)
        self.score_sentence()

    def score_sentence(self=None):
        # Scoring sentence as per the word freq
        for sent in self.sentence_token:  # Select a sentence from sentence token
            for word in nltk.word_tokenize(sent.lower()):  # Select a word from each sentence
                if word in self.word_frequency.keys():  # That selected word shouldn't be a stopword or any other non-alphabetical value
                    if len(sent.split(' ')) < 30:  # If length of that sentence is less than 30
                        if sent not in self.sentence_score.keys():  # And that selected sent isn't in the sent_score then inialize that sent by the value of that word
                            self.sentence_score[sent] = self.word_frequency[word]
                        else:  # If it's already there then just increment it by the value of selected word
                            self.sentence_score[sent] += self.word_frequency[word]
        # print(sent_score)

    def create_summary(self=None):
        summary = hp.nlargest(10, self.sentence_score)
        # print(summary)
        for sent in summary:
            print(sent)


if __name__ == "__main__":
    doc_summ = Doc_Summ()
    #print(type('https://en.wikipedia.org/wiki/Machine_learning'))
    while True:
        #try:
        choice = int(input('1) Url: \n2) Text: \n3) Doc: \n-1) Exit:'))
        #except EOFError:
        #    x = ''
        if choice == 1:
            #string = input('Enter url: ')
            #print(type(string))
            doc_summ.web_scraping()
        elif choice == 2:
            #string = input('Enter text: ')
            doc_summ.set_text()
        elif choice == 3:
            doc_summ.txt_sum()
        elif choice == -1:
            exit()
        else:
            print("Select from the given choice")
        doc_summ.create_summary()
    #doc_summ.web_scraping()
    #doc_summ.create_summary()
    #doc_summ.speech_text()











