import sys
#import numpy as np
#import matplotlib.pyplot as plt

def getngrams(sentence, n):
    for i in range(n-1):
        sentence = "#" + sentence
    for i in range(n-1):
        sentence += "#"
    #print sentence
    ngrams = []
    for i in range(len(sentence)-n):
        ngrams.append(sentence[i:i+n])
        
    
    return ngrams

        
if __name__ == '__main__':
    #print "Hello World"
    lines = [line.rstrip('\n') for line in open(sys.argv[1], "r")]
    test = [line.rstrip('\n') for line in open(sys.argv[2], "r")]

    
#     nList = [1,2,3,4,5,6,7,8,9,10]
#     lambList = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
# 
# #     nList = [1,2,3,4,5,6,7,8,9]
# #     lambList = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.9,1.0]
#     
#     nList = [4]
#     lambList = [0.1]
    
#     maxn = 1
#     maxLamb = 0.0
#     maxAcc = 0
    
    #accuracies = np.zeros(shape=(len(nList), len(lambList)))
    
#     ncount = -1
    
#     for n in nList:
#         ncount += 1
#         lambCount = -1
#         for lamb in lambList:
#             lambCount += 1
    n = int(sys.argv[3])
    lamb = float(sys.argv[4])
#     ngramscount = {}
    langCount = {}
    languages = {}
    vocab = set()
    result = str()
    # training
    for line in lines:
        sentence = line.split("|")[1]
        lang = line.split("|")[2]
        if langCount.has_key(lang):
            langCount[lang] += 1
        else:
            langCount[lang] = 1
        #sentence = ''.join(ch for ch in sentence if ch not in (',',':','.','!','@','#','$','/','_'))
        sentence = ''.join(ch for ch in sentence if ch not in (',',':','.','!','@','#','$','/','_','\'','-','?','*'))
        
        if not languages.has_key(lang):
            languages[lang] = {}
        ngrams = getngrams(sentence, n)
#         if ngramscount.has_key(lang):
#             ngramscount[lang] += len(ngrams)
#         else:
#             ngramscount[lang] = len(ngrams)
            
        for ngram in ngrams:
            vocab.add(ngram)
            if languages[lang].has_key(ngram):
                languages[lang][ngram] += 1
            else:
                languages[lang][ngram] = 1
        
        
#     print len(languages)
#     print len(vocab)
    
#     for lang in languages:
#         print lang, len(languages[lang].keys()), ngramscount[lang]/len(languages[lang].keys())
    
    #calculating denominators for each language
    denoms = {}
    for lang in languages:
        sum = 0
        for k in languages[lang].keys():
            sum += languages[lang][k]
        
        denoms[lang] = (sum + lamb*len(vocab))/10000
        #print lang, denoms[lang]
    
    
    
    #testing
#     correct = 0
#     wrong = 0
#     notfound = 0
    for line in test:
        sentence = line.split("|")[1]
        #trueLang = line.split("|")[2]
        #print trueLang
        #sentence = ''.join(ch for ch in sentence if ch not in (',',':','.','!','@','#','$','/','_'))
        sentence = ''.join(ch for ch in sentence if ch not in (',',':','.','!','@','#','$','/','_','\'','-','?','*'))
        ngrams = getngrams(sentence, n)
        prob = {}
        maxProd = 0.0
        predicLang = "None"
        for lang in languages.keys():
            prod = 1
            for ngram in ngrams:
                if languages[lang].has_key(ngram):
                    prod = prod * float(languages[lang][ngram] + lamb)/denoms[lang]
                else:
                    prod = prod *  (lamb)/denoms[lang]
             
            prod = prod * langCount[lang]/len(lines)
                    
            if prod > maxProd:
                called = True
                maxProd = prod
                predicLang = lang 
            
            #print prod  
        
            
#         if trueLang == predicLang:
#             correct += 1
#         else:
#             #print trueLang, " ", predicLang
#             wrong += 1
        
        result = result + line.split("|")[0] + "|" + predicLang + "\n"
        #print line.split("|")[0],"|",predicLang
    print result