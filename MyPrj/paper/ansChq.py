from nltk.tokenize import sent_tokenize,word_tokenize
import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''


def Marks1(ff1,ff2):
    #mark = int(input("Enter the marks"))
    #print("\n")
    
    '''Preprocessing the Teacher's Answer'''
    #f1 = open("sampleRealAns1.txt")             # open real ans file
    #ff1 = f1.read()                             # read real ans
    sent_f1 = sent_tokenize(ff1, 'english')     # list of sentence present in real ans file
    for x in sent_f1:
        print(x)
    print("\n")
    f1 = open("WORDLIST.txt")                   # open stop words
    stopwords = f1.read()                       # list of stopwords
    ls1 = []                                    # final list containing extracted data, tokens with pos
    tuppleR0 = []                               # final list containing extracted data, tokens without pos
    for x in sent_f1:                           # read sentences
        temp = word_tokenize(x)                 # generate list of tokens for each sentence
        temp = nltk.pos_tag(temp)               # part of speech tag each tokens
        abc = []                                # list containing important token with pos
        abc1 = []
        for m in temp:                          # read the list of tokens for each sentence                      
            a = m[0].lower()                    # tupple[0] contains the word
            if a not in stopwords:              # if it is important
                if re.match("([\w|\d])+", a):   # if it anything besides a word or number
                    abc.append(m)               # append the tupple whole as important
                    abc1.append(m[0].lower())   # append the tupple0 as important
        ls1.append(abc)                         # append the list of tokens with pos in a sentence to the final list
        tuppleR0.append(abc1)                   # append the list of tokens in a sentence to the final list
    for x in ls1:
        print(x)
    print("\n\n")
    
    for x in tuppleR0:
        print(x)
    print("-------------------------------------------------------------------------------")
    print("\n\n\n\n")    
    '''Same for preprocessing the Student's Answer'''
    #f2 = open("sampleRealAns2.txt")
    #ff2 = f2.read()
    sent_f2 = sent_tokenize(ff2, 'english')
    for x in sent_f2:
        print(x)
    print("\n")
    ls2 = []
    tuppleS0 = []
    for x in sent_f2:
        temp = word_tokenize(x)
        temp = nltk.pos_tag(temp)
        abc = []
        abc1 = []
        for m in temp:
            a = m[0].lower()
            if a not in stopwords:
                if re.match("([\w|\d])+", a):
                    abc.append(m)
                    abc1.append(m[0].lower())    
        ls2.append(abc)
        tuppleS0.append(abc1)
    for x in ls2:
        print(x)
    print("\n\n")
    for x in tuppleS0:
        print(x)
    print("-------------------------------------------------------------------------------")
    print("\n\n\n\n")
    
    
    
    dict = {}                                   # dictionary(student_ans_sentence:teacher_ans_sentence)
    '''association of sentences'''
    for m2 in tuppleS0:
        max = 0
        ind = -1
        for m1 in tuppleR0:
            count = 0
            for x2 in m2:
                for x1 in m1:
                    if(x1.lower() == x2.lower()):
                        count += 1
                        break
            if(count > max and count > 0):
                max = count
                ind = tuppleR0.index(m1)
        if ind not in dict.values() and ind != -1:
            dict[tuppleS0.index(m2)] = ind
    print(dict, "\n\n")
    for x in dict.keys():
        print(tuppleS0[x], end="")
        print(tuppleR0[dict[x]])
    print("-------------------------------------------------------------------------------")        
    print("\n\n\n\n")
    
    

    total_count1 = 0;
    match_count = 0;
    total_count2 = 0;
    TrueFalse1 = []
    TrueFalse2 = []
    for x in tuppleR0:
        temp = {}
        for a in x:
            total_count1 += 1
            temp[a] = False
        TrueFalse1.append(temp)
    for x in tuppleS0:
        for a in x:
            total_count2 += 1
            
    for x in dict.keys():
        b = TrueFalse1[dict[x]]
        for a in tuppleS0[x]:
            if a in b.keys():
                b[a] = True
    
    for x in TrueFalse1:
        print(x)
        for a in x.keys():
            if(x[a] == True):
                match_count += 1
    print("-------------------------------------------------------------------------------")        
    print("\n\n\n\n")
    
    
    frac = (match_count * 2) / (total_count1 + total_count2)
    print(frac*100)
    return frac*100
    #marks = (frac) * mark
    #print("PERCENTAGE MATCHING IS: ", float("{0:.2f}".format(frac * 100)))
    #print("MARKS OBTAINED OUT OF ", mark, " marks" , round(marks))
    #return marks





def Marks2(ff1,ff2):
    #mark=int(input("Enter the marks"))
    #print("\n")
    ps=WordNetLemmatizer()
    '''Preprocessing the Teacher's Answer'''
    #f1=open("sampleRealAns3.txt")           #open real ans file
    #ff1=f1.read()                           #read real ans
    sent_f1= sent_tokenize(ff1,'english')   #list of sentence present in real ans file
    for x in sent_f1:
        print(x)
    print("\n")
    f1=open("WORDLIST.txt")                 #open stop words
    stopwords=f1.read()                     #list of stopwords
    ls1=[]                                  #final list containing extracted data, tokens with pos
    tuppleR0=[]                             #final list containing extracted data, tokens without pos
    for x in sent_f1:                       #read sentences
        temp=word_tokenize(x)               #generate list of tokens for each sentence
        temp=nltk.pos_tag(temp)             #part of speech tag each tokens
        abc=[]                              #list containing important token with pos
        abc1=[]
        for m in temp:                      #read the list of tokens for each sentence                      
            a=m[0].lower()                  #tupple[0] contains the word
            if a not in stopwords:          #if it is important
                if re.match("([\w|\d])+",a):#if it anything besides a word or number
                    abc.append(m)
                    if re.match("JJ.?|RB.?|VB.?|NN.?|NNPS",m[1]):           #append the tupple whole as important
                        abc1.append(ps.lemmatize(a, pos=get_wordnet_pos(m[1])))       #append the tupple0 as important
                    else:
                        abc1.append(a)
        ls1.append(abc)                     #append the list of tokens with pos in a sentence to the final list
        tuppleR0.append(abc1)               #append the list of tokens in a sentence to the final list
    for x in ls1:
        print(x)
    print("\n\n")
    
    for x in tuppleR0:
        print(x)
    print("-------------------------------------------------------------------------------")
    print("\n\n\n\n")
    '''Same for preprocessing the Student's Answer'''
    #f2=open("sampleRealAns4.txt")
    #ff2=f2.read()
    sent_f2= sent_tokenize(ff2,'english')
    for x in sent_f2:
        print(x)
    print("\n")
    ls2=[]
    tuppleS0=[]
    for x in sent_f2:
        temp=word_tokenize(x)
        temp=nltk.pos_tag(temp)
        abc=[]
        abc1=[]
        for m in temp:
            a=m[0].lower()
            if a not in stopwords:
                if re.match("([\w|\d])+",a):
                    abc.append(m)
                    if re.match("JJ|RB|VB|NN",m[1]):           #append the tupple whole as important
                        abc1.append(ps.lemmatize(a, pos=get_wordnet_pos(m[1])))  #append the tupple0 as important
                    else:
                        abc1.append(a)    
        ls2.append(abc)
        tuppleS0.append(abc1)
    for x in ls2:
        print(x)
    print("\n\n")
    for x in tuppleS0:
        print(x)
    print("-------------------------------------------------------------------------------")
    print("\n\n\n\n")
    
    dict={}                                 #dictionary(student_ans_sentence:teacher_ans_sentence)    
    '''association of sentences'''
    for m2 in tuppleS0:
        max=0
        ind=-1
        for m1 in tuppleR0:
            count=0
            for x2 in m2:
                for x1 in m1:
                    if(x1.lower()==x2.lower()):
                        count+=1
                        break
            if(count>max and count >0):
                max=count
                ind=tuppleR0.index(m1)
        if ind not in dict.values() and ind!=-1:
            dict[tuppleS0.index(m2)]=ind
    print(dict,"\n\n")
    for x in dict.keys():
        print(tuppleS0[x],end="")
        print(tuppleR0[dict[x]])
    print("-------------------------------------------------------------------------------")        
    print("\n\n\n\n")
    
    
    total_count1=0;
    match_count=0;
    total_count2=0;
    TrueFalse1=[]
    TrueFalse2=[]
    for x in tuppleR0:
        temp={}
        for a in x:
            total_count1+=1
            temp[a]=False
        TrueFalse1.append(temp)
    for x in tuppleS0:
        for a in x:
            total_count2+=1
            
    for x in dict.keys():
        b=TrueFalse1[dict[x]]
        for a in tuppleS0[x]:
            if a in b.keys():
                b[a]=True
    
    for x in TrueFalse1:
        print(x)
        for a in x.keys():
            if(x[a]==True):
                match_count+=1
    print("-------------------------------------------------------------------------------")        
    print("\n\n\n\n")
    
    
    frac=(match_count*2)/(total_count1+total_count2)
    print(frac*100)
    return frac*100
    #marks=(frac)*mark
    #print("PERCENTAGE MATCHING IS: ",float("{0:.2f}".format(frac*100)))
    #print("MARKS OBTAINED OUT OF ",mark," marks" ,round(marks))
    
    #return marks

