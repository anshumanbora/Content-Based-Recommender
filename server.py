import warnings
import urllib.request
import re
import pysolr
from flask import jsonify
import subprocess
from bs4 import BeautifulSoup, SoupStrainer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from flask import Flask, render_template, request, redirect
from flask_cors import CORS, cross_origin

warnings.filterwarnings("ignore")
app = Flask(__name__, template_folder = 'templates')
app.secret_key = 'NoSoupForYou!'
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#solr styff
def getSolrObject():
	solr = pysolr.Solr('http://127.0.0.1:8983/solr/adaptiveweb', timeout = 1000)
	return solr

def solrStartUp():
	response = subprocess.call("solr-7.1.0\\bin\\solr start -p 8983", shell = True)
	return response

def scraper():
   indexList = 0
   listItems = []

   response =  urllib.request.urlopen('https://en.wikibooks.org/wiki/Java_Programming')
   allTheLinks = []
   for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
      if link.has_attr('href'):
         if link['href'][1:5]=='wiki':
            if('Help:' not in link['href']):

               allTheLinks.append('https://en.wikibooks.org'+link['href'])
   count = 0
   for x in allTheLinks:
      print(count)

      if (count>18 and count<107):
         detailed_response =  urllib.request.urlopen(x)
         detailed_soup = BeautifulSoup(detailed_response)

         #getting title of this page
         maintitle = detailed_soup.find('b')
         #print(maintitle.getText())

         # getting all intro content
         intro = detailed_soup.find('table', {'class': 'wikitable'})
         # print(intro.getText())

         try:
            nextintro = intro.next_siblings

         except:
            pass
         introtext = ''
         introhtml = ''
         for y in nextintro:
            if y.name == 'h2':
               break
            try:
               introtext += y.text
               introhtml += str(y)
            except:
               pass
         #print(introhtml)

         dictItems = {}
         dictItems['id'] = indexList
         dictItems['url'] = x
         dictItems['text'] = introtext
         dictItems['title'] = maintitle
         dictItems['stemdata'] = introtext
         dictItems['html'] = introhtml
         indexList+=1
         listItems.append(dictItems)

         #getting all h2 and its content
         allh2Tags = detailed_soup.findAll('h2')
         for z in allh2Tags:
            next = z.next_siblings
            title=z.getText()
            siblingtext = ' '
            siblinghtml = ' '
            for y in next:

               if y.name=='h2':
                  break
               try:
                  siblingtext+=y.text
                  siblinghtml+=str(y)
               except:
                  pass

            #print(siblinghtml)
            dictItems = {}
            dictItems['id'] = indexList
            dictItems['url'] = x
            dictItems['text'] = siblingtext
            dictItems['title'] = title
            dictItems['stemdata'] = siblingtext
            dictItems['html'] = siblinghtml
            indexList+=1
            listItems.append(dictItems)

      count += 1
   #print(listItems[0])
   return listItems

@app.route("/")
def index():
    response = solrStartUp()
    solr = getSolrObject()
    search = solr.search(q = 'id:["" TO *]')

    if len(search) != 0:
        print('housefull')
        pass
    else:
        listItems = scraper()
        response = solr.delete(q = "*:*")

        for x in listItems:
            try:
                response = solr.add([x])
            except:
                pass

    return render_template('index.html')
    #return True

@app.route('/recommend', methods = ['POST'])
@cross_origin()
def recommend():

    optionsMap = {
    'op1': "I was presented with this question in an end of module open book exam today and found myself lost. i was reading Head first Javaand both definitions seemed to be exactly the same. i was just wondering what the MAIN difference was for my own piece of mind. i know there are a number of similar questions to this but, none i have seen which provide a definitive answer.Thanks, Darren",
	'op2': "Inheritance is when a 'class' derives from an existing 'class'.So if you have a Person class, then you have a Student class that extends Person, Student inherits all the things that Person has.There are some details around the access modifiers you put on the fields/methods in Person, but that's the basic idea.For example, if you have a private field on Person, Student won't see it because its private, and private fields are not visible to subclasses.Polymorphism deals with how the program decides which methods it should use, depending on what type of thing it has.If you have a Person, which has a read method, and you have a Student which extends Person, which has its own implementation of read, which method gets called is determined for you by the runtime, depending if you have a Person or a Student.It gets a bit tricky, but if you do something likePerson p = new Student();p.read();the read method on Student gets called.Thats the polymorphism in action.You can do that assignment because a Student is a Person, but the runtime is smart enough to know that the actual type of p is Student.Note that details differ among languages.You can do inheritance in javascript for example, but its completely different than the way it works in Java.",
	'op3': "Polymorphism: The ability to treat objects of different types in a similar manner.Example: Giraffe and Crocodile are both Animals, and animals can Move.If you have an instance of an Animal then you can call Move without knowing or caring what type of animal it is.Inheritance: This is one way of achieving both Polymorphism and code reuse at the same time.Other forms of polymorphism:There are other way of achieving polymorphism, such as interfaces, which provide only polymorphism but no code reuse (sometimes the code is quite different, such as Move for a Snake would be quite different from Move for a Dog, in which case an Interface would be the better polymorphic choice in this case.In other dynamic languages polymorphism can be achieved with Duck Typing, which is the classes don't even need to share the same base class or interface, they just need a method with the same name.Or even more dynamic like Javascript, you don't even need classes at all, just an object with the same method name can be used polymorphically.",
	'op4': "I found out that the above piece of code is perfectly legal in Java. I have the following questions. ThanksAdded one more question regarding Abstract method classes.",
	'op5': "In java it's a bit difficult to implement a deep object copy function. What steps you take to ensure the original object and the cloned one share no reference? ",
	'op6': "You can make a deep copy serialization without creating some files. Copy: Restore:",
	'op7': "Java has the ability to create classes at runtime. These classes are known as Synthetic Classes or Dynamic Proxies. See for more information. Other open-source libraries, such as and also allow you to generate synthetic classes, and are more powerful than the libraries provided with the JRE. Synthetic classes are used by AOP (Aspect Oriented Programming) libraries such as Spring AOP and AspectJ, as well as ORM libraries such as Hibernate.",
	'op8': "A safe way is to serialize the object, then deserialize.This ensures everything is a brand new reference.about how to do this efficiently. Caveats: It's possible for classes to override serialization such that new instances are created, e.g. for singletons.Also this of course doesn't work if your classes aren't Serializable.",
	'op9': "comment this code",
	'op10': "     in a class i can have as many constructors as i want with different argument types. i made all the constructors as private it didn't give any error because my implicit default constructor was public but when i declared my implicit default constructor as private then its showing an error while extending the class.  why?       this works fine         this can not be inherited      "
	}

    option = request.form['index']
    option = 'op' + str(option)
    text = optionsMap[option]
    words = re.split("\W+", text)

    stemmer = PorterStemmer()
    words = [word for word in words if word not in stopwords.words('english')]
    words = [stemmer.stem(word) for word in words]
    query = ' or '.join(words)

    q = "stemdata:(" + query + ")"
    print(q)
    solr = getSolrObject()
    results = solr.search(q = q, rows = 10)

    sendResults = []
    for i in results:
        title = str(i['title'])[2:-8]
        print(title)
        item={}
        # sendResults.append(i)
        item['html']=i['html']
        item['title']=title
        item['url']=i['url']
        sendResults.append(item)
    return jsonify(sendResults)



if __name__ == '__main__':
    app.run(debug = True, threaded=True)
