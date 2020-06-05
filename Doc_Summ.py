import re
import nltk
import textract as txt
import requests as req
#import speech_recognition as sr
import heapq as hp
# import requests as req
from bs4 import BeautifulSoup as Bs

#nltk.download('stopwords')
class Doc_Summ:

    scraped_content = ''
    refined_text_content = ''
    sentence_token = ''
    word_token = ''
    word_frequency = {}
    sentence_score = {}

    def txt_sum(self):
        self.scraped_content = ''
        self.scraped_content = str(txt.process(".\\test.txt"), 'utf-8')
        # print(self.scraped_content)
        self.text_cleaning()

    def web_scraping(self, string):
        # Web Scraping
        html_doc = req.get(string) #'https://en.wikipedia.org/wiki/Machine_learning'
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

    def text_cleaning(self):
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

    def stopwords(self):
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

    def score_sentence(self):
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

    def create_summary(self, n):
        summary = hp.nlargest(n, self.sentence_score)
        # print(summary)
        # for sent in summary:
        #     print(sent)
        return summary


# if __name__ == "__main__":
#     doc_summ = Doc_Summ()
#     #print(type('https://en.wikipedia.org/wiki/Machine_learning'))
#     while True:
#         #try:
#         choice = int(input('1) Url: \n2) Text: \n3) Doc: \n-1) Exit:'))
#         #except EOFError:
#         #    x = ''
#         if choice == 1:
#             string = input('Enter url: ')
#             #print(type(string))
#             doc_summ.web_scraping(string)
#         elif choice == 2:
#             #string = input('Enter text: ')
#             doc_summ.set_text()
#         elif choice == 3:
#             doc_summ.txt_sum()
#         elif choice == -1:
#             exit()
#         else:
#             print("Select from the given choice")
#         n = int(input('No. of lines: '))
#         doc_summ.create_summary(n)
    #doc_summ.web_scraping()
    #doc_summ.create_summary()
    #doc_summ.speech_text()











