#!/usr/bin/env python
# coding: utf-8

# In[177]:




import numpy as np
import pandas as pd
import re
# from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import sys
from nltk.stem import WordNetLemmatizer
import csv
import pickle


lemmatizer = WordNetLemmatizer() 

StopWords=open("D:\MY SEMESTER\SEMESTER 6\INFORMATION RETRIEVAL\ASSIGNMENT 1\Stopword-List.txt")
StopWords=StopWords.readlines()
Results=open("D:\MY SEMESTER\SEMESTER 6\INFORMATION RETRIEVAL\ASSIGNMENT 1\Querry List.txt")
Results=Results.readlines()





def QuerryAndOperation(TermL,TermR):
    
    if isinstance(TermL,list)==False:
        
        TermL=lemmatizer.lemmatize(TermL)
        Left=SortedDictionary[TermL]
        LeftDocumentId=Left.keys()
    else:
        LeftDocumentId=TermL
    
    if isinstance(TermR,list)==False:
        TermR=lemmatizer.lemmatize(TermR)
        Right=SortedDictionary[TermR]
        RightDocumentId=Right.keys()
    else:
        RightDocumentId=TermR
    Ans=[]
    for i in LeftDocumentId:
        for j in RightDocumentId:
            if i==j:
                Ans.append(i)
    return Ans
    
    
def QuerryOrOperation(TermL,TermR):
    
    if isinstance(TermL,list)==False:
        TermL=lemmatizer.lemmatize(TermL)
        Left=SortedDictionary[TermL]
        LeftDocumentId=Left.keys()
    else:
        LeftDocumentId=TermL
    
    if isinstance(TermR,list)==False:
        TermR=lemmatizer.lemmatize(TermR)
        Right=SortedDictionary[TermR]
        RightDocumentId=Right.keys()
    else:
        RightDocumentId=TermR
    Ans=[]
    AnsSet=set() #For Unique Values
    
    for i in LeftDocumentId:
        AnsSet.add(i)
    for j in RightDocumentId:
        AnsSet.add(j)
        
    for ans in AnsSet:
        Ans.append(ans)
    return Ans

def GeneratingStopWordsList(File):
    StopWordList=[]
    for word in StopWords:
        word=re.split("\\n",word)
        if word[0]!="":
            StopWordList.append(word[0].replace(" ",""))
    return StopWordList

def GenerateTokensBySpace(File):
    Tokens=[]
    for Word in File:
        Token=""
        for Character in Word:
            if Character!=" ":
                Token+=Character
            else:
                Tokens.append(Token)
                Token=""
    return Tokens

def RemovingDots(Tokens):
    Result=[]
    for Token in Tokens:
        if Token.count(".")>=2: #For Initials like U.S.A
            Result.append(Token.replace(".",""))
        else:
            SplitByDot=re.split("\.",Token) # For Words Like Thousands.So
            for Word in SplitByDot:
                if Word!="":
                    Result.append(Word)
    return Result
def RemovingContractions(Tokens):
    Result=[]
    for Token in Tokens:
        Word=Token.replace("?","").replace(":","").replace(",","").replace('"',"")
        Word=re.split(r"n't",Word)
        if len(Word)>1:
            Word[1]="not"
        if len(Word)<2:
            Word=re.split(r"'s",Word[0])
            if len(Word)>1:
                Word[1]="is"
        if len(Word)<2:
            Word=re.split(r"'re",Word[0])
            if len(Word)>1:
                Word[1]="are"
        if len(Word)<2:
            Word=re.split(r"'m",Word[0])
            if len(Word)>1:
                Word[1]="am"
        if len(Word)<2:
            Word=re.split(r"'ll",Word[0])
            if len(Word)>1:
                Word[1]="will"
        if len(Word)<2:
            Word=re.split(r"'ve",Word[0])
            if len(Word)>1:
                Word[1]="have"
        if len(Word)<2:
            Word=re.split(r"'d",Word[0])
            if len(Word)>1:
                Word[1]="had"
        for W in Word:
            if W!="":
                Result.append(W)
    return Result

def LOWERCASECONVERTOR(Tokens):
    Result=[]
    for Token in Tokens:
        Result.append(Token.lower())
    return Result

def RemovingBraces(Tokens): #[]
    Result=[]
    for Token in Tokens:
        Words=re.split(r"\[(\w+)\]",Token)
        for Word in Words:
            if Word!="":
                Result.append(Word)
    return Result
def RemovingStopWords(Tokens,StopWordList):
    Result=[]
    for Token in Tokens:
        if Token not in StopWordList:
            Result.append(Token)
    return Result
def RemovingHypens(Tokens):
    Result=[]
    for Token in Tokens:
        Words=re.split(r"\-",Token)
        for Word in Words:
            if Word!="":
                Result.append(Word)
    return Result

def PorterStemming(Tokens):
    Result=[]
    for Token in Tokens:
        Result.append(lemmatizer.lemmatize(Token))
    return Result

def GeneratingPostingList():
    
    Dictionary={}
    StopWordDictionary={}
    
    SortedDictionary={}
    SortedDictionaryWithStopWord={}
    
    TokensWithStopWords=[]
    
    for file in range(0,56):
        
        FileName="D:\MY SEMESTER\SEMESTER 6\INFORMATION RETRIEVAL\ASSIGNMENT 1\Trump Speechs\speech_"
        FileName+=str(file)
        FileName+=".txt"
        File=open(FileName)
        Speech=File.readlines()
#         print(FileName)
        Speech=Speech[1:]
        # Filtering Data
        StopWordList=GeneratingStopWordsList(StopWords)
        Tokens=GenerateTokensBySpace(Speech)
        Tokens=RemovingContractions(Tokens)
        Tokens=RemovingDots(Tokens)
        Tokens=LOWERCASECONVERTOR(Tokens)
        Tokens=RemovingBraces(Tokens)
        Tokens=RemovingHypens(Tokens)
        
        TokensWithStopWords=Tokens
        
        #StopWordsTokens
        Tokens=RemovingStopWords(Tokens,StopWordList)
        
        Tokens=PorterStemming(Tokens)
        
        #StopWordsTokens With Porter Stemming
        TokensWithStopWords=PorterStemming(TokensWithStopWords)
    
        #Generate Dictionary
    
    
        for i in range(0,len(Tokens)):
            Dictionary.setdefault(Tokens[i],{})
            Dictionary[Tokens[i]].setdefault(file,[])
            Dictionary[Tokens[i]][file].append(i)
            
            #StopWords Dictionary
            
            StopWordDictionary.setdefault(TokensWithStopWords[i],{})
            StopWordDictionary[TokensWithStopWords[i]].setdefault(file,[])
            StopWordDictionary[TokensWithStopWords[i]][file].append(i)
    
    SortedKeys=sorted(Dictionary)
    
    # Keys Of Dictionary Including Stop Words
    StopWordSortedKeys=sorted(StopWordDictionary)
    
    for key in SortedKeys:
        SortedDictionary.setdefault(key,{})
        for j in Dictionary[key]:
            SortedDictionary[key].setdefault(j,Dictionary[key][j])
            
    for key in StopWordSortedKeys:
        SortedDictionaryWithStopWord.setdefault(key,{})
        for j in StopWordDictionary[key]:
            SortedDictionaryWithStopWord[key].setdefault(j,StopWordDictionary[key][j])
            
    return Dictionary,SortedDictionary,SortedDictionaryWithStopWord

def QuerryNotOperation(Term):
    if isinstance(Term,list)==False:
        Term=lemmatizer.lemmatize(Term)
        Left=SortedDictionary[Term]
        LeftDocumentId=Left.keys()
    else:
        LeftDocumentId=Term
    Ans=[]
    for i in range(0,56):
        if i not in LeftDocumentId:
            Ans.append(i)
    return Ans

def ProximityQuerryOperation(TermL,TermR,Factor):
    
    if isinstance(TermL,list)==False:
        TermL=lemmatizer.lemmatize(TermL)
        Left=SortedDictionaryWithStopWord[TermL]
        LeftDocumentId=Left.keys()
    else:
        LeftDocumentId=TermL
    
    if isinstance(TermR,list)==False:
        TermR=lemmatizer.lemmatize(TermR)
        Right=SortedDictionaryWithStopWord[TermR]
        RightDocumentId=Right.keys()
    else:
        RightDocumentId=TermR
    Ans=[]
    AnsSet=set()
    
    
    for LeftId in LeftDocumentId:
        if LeftId in RightDocumentId:
            PositionsIndexLeft=SortedDictionaryWithStopWord[lemmatizer.lemmatize(TermL)][LeftId]
            PositionsIndexRight=SortedDictionaryWithStopWord[lemmatizer.lemmatize(TermR)][LeftId]
            for LeftPositionIndex in PositionsIndexLeft:
                if LeftPositionIndex+Factor in PositionsIndexRight:
                    AnsSet.add(LeftId)
    
    for ans in AnsSet:
        Ans.append(ans)
    return Ans

def TermsOfFileAndTheirIndexes(FileName):
    for i in SortedDictionary:
        if FileName in SortedDictionary[i].keys():
            print(i,SortedDictionary[i][FileName])

def Querry(querry):
    
    #Proximity Querry Parsingy
    
    if '/' in querry:
        Factor=""
        ProximityList=[]
        Terms=re.split(r"\W+",querry)
        for i in range(len(Terms)-1,-1,-1):
            if Terms[i].isdigit():
                Factor=int(Terms[i])
            else:
                ProximityList.append(Terms[i])
        for i in range(len(ProximityList)-1,-1,-1):
            if i==1:
                Result=ProximityQuerryOperation(ProximityList[i],ProximityList[i-1],Factor+1)
        return Result
    
    #QuerryParsing
    Terms=re.split(r"\W+",querry)
    
    
    #For Phrasal Querry
    if len(re.split("and|AND|or|OR|NOT|not|/",querry))==1:
        Result=QuerryOrOperation(Terms[0],[])
        return Result
    
    
    if '' in Terms:
        Terms.remove("")
    
    Result=[]
    
    
    
    if len(Terms)==1:
        Result=QuerryOrOperation(Terms[0],[])
        return Result
    
    i=len(Terms)-1
    
    for Term in range(len(Terms)):
        
        if (Terms[i]=="or" or Terms[i]=="OR") and Term==1:
            
            Result=QuerryOrOperation(Terms[i+1],Terms[i-1])
            
            
        elif Term>2 and (Terms[i]=="or" or Terms[i]=="OR"):
            
            Result=QuerryOrOperation(Terms[i-1],Result)
            
        if (Terms[i]=="and" or Terms[i]=="AND") and Term==1:
            
            Result=QuerryAndOperation(Terms[i+1],Terms[i-1])
        
        elif Term>2 and (Terms[i]=="and" or Terms[i]=="AND"):
            
            Result=QuerryAndOperation(Terms[i-1],Result)
            
        if (Terms[i]=="NOT" or Terms[i]=="not") and Term==1:
            
            Result=QuerryNotOperation(Terms[i-1])
        
        elif Term>1 and (Terms[i]=="NOT" or Terms[i]=="not"):
            
            Result=QuerryNotOperation(Result)
            
        i-=1
        
    return Result


def VectorMagnitude(SortedDictionary,Doc):
    Matrix=[[0 for i in range(0,56)]for key in SortedDictionary.keys()]
    Term=0
    for key in SortedDictionary.keys():
        
        NoOfDocumentForTerm=len(SortedDictionary[key])
        TermIDF=np.log10((NoOfDocumentForTerm)/56)
        
        for doc in SortedDictionary[key].keys():
            Matrix[Term][doc]=len(SortedDictionary[key][doc])*TermIDF
        Term+=1
    
    Term=0
    SumOfSquareOfWeights=0
    
    for key in SortedDictionary.keys():
        SumOfSquareOfWeights+=np.square(Matrix[Term][Doc])
        Term+=1
    
    return np.sqrt(SumOfSquareOfWeights)

def DocumentVectorSpaceModel(SortedDictionary,Querry,alpha):
    
    #Filtering Querry
    
    
    
    StopWordList=GeneratingStopWordsList(StopWords)
    
    Tokens=re.split(" ",Querry)
    
    Tokens=RemovingContractions(Tokens)
    
    Tokens=RemovingDots(Tokens)
    
    Tokens=LOWERCASECONVERTOR(Tokens)
    
    Tokens=RemovingBraces(Tokens)
    
    Tokens=RemovingHypens(Tokens)
    
    Tokens=RemovingStopWords(Tokens,StopWordList)
    
    
    QueryTerms=Tokens
    QuerryTermFrequency={}
    for QueryTerm in QueryTerms:
        QuerryTermFrequency.setdefault(lemmatizer.lemmatize(QueryTerm),0)

    for QueryTerm in QueryTerms:
        Quantity=QuerryTermFrequency[lemmatizer.lemmatize(QueryTerm)]
        Quantity+=1
        QuerryTermFrequency[lemmatizer.lemmatize(QueryTerm)]=Quantity
    
    for QueryTerm in QueryTerms:
        Quantity=QuerryTermFrequency[lemmatizer.lemmatize(QueryTerm)]
    
        NoOfDocumentForTerm=len(SortedDictionary[lemmatizer.lemmatize(QueryTerm)])
    
        TermIDF=np.log10((NoOfDocumentForTerm)/56)
    
        Quantity=TermIDF*Quantity
        QuerryTermFrequency[lemmatizer.lemmatize(QueryTerm)]=Quantity
        
        
    TermDocumentFrequency={}
    Result={}
    for QueryTerm in QueryTerms:
        
        TermDocumentFrequency.setdefault(lemmatizer.lemmatize(QueryTerm),{})
    
        Result.setdefault(lemmatizer.lemmatize(QueryTerm),{})
    
        NoOfDocumentForTerm=len(SortedDictionary[lemmatizer.lemmatize(QueryTerm)])
    
        TermIDF=np.log10((NoOfDocumentForTerm)/56)
    
        for Doc in SortedDictionary[lemmatizer.lemmatize(QueryTerm)]:
        
            TermDocumentFrequency[lemmatizer.lemmatize(QueryTerm)].setdefault(Doc,len(SortedDictionary[lemmatizer.lemmatize(QueryTerm)][Doc])*TermIDF)
        
            Result[lemmatizer.lemmatize(QueryTerm)].setdefault(Doc,len(SortedDictionary[lemmatizer.lemmatize(QueryTerm)][Doc])*TermIDF)
    
    
    SumOfSquareOfWeightsOfQuery=0
    for key in QuerryTermFrequency:
        SumOfSquareOfWeightsOfQuery+=(QuerryTermFrequency[key]*QuerryTermFrequency[key])
   

    SumOfSquareOfWeightsOfQuery=np.sqrt(SumOfSquareOfWeightsOfQuery)
    
    
    for Term in QuerryTermFrequency:
        QuerryScore=QuerryTermFrequency[Term]
        for Doc in TermDocumentFrequency[Term]:
            Result[Term][Doc]=(QuerryScore*TermDocumentFrequency[Term][Doc])/((VectorMagnitude(SortedDictionary,Doc)*SumOfSquareOfWeightsOfQuery))
    
    FinalResult={}

    for i in range(0,56):
        FinalResult.setdefault(i,0)

    for Term in Result:
        for Doc in Result[Term]:
            Quantity=FinalResult[Doc]
            Quantity+=Result[Term][Doc]
            FinalResult[Doc]=Quantity
    
    
    # Need to Recheck
    R={}
    SortedResult=[]
    for w in sorted(FinalResult, key=FinalResult.get, reverse=True):
        if FinalResult[w]!=0 and FinalResult[w]>=alpha:
            R.setdefault(w, FinalResult[w])
            SortedResult.append(w)
    
    return SortedResult


# In[178]:


def GenerateFile(SortedDictionary):
    with open('data.p', 'wb') as fp:
        pickle.dump(SortedDictionary, fp, protocol=pickle.HIGHEST_PROTOCOL)





try:
    with open('data.p', 'rb') as fp:
         SortedDictionary= pickle.load(fp)
except IOError:
    Dictionary,SortedDictionary,SortedDictionaryWithStopWord = GeneratingPostingList()
    GenerateFile(SortedDictionary)
    


def main(inp,inp2):
    Ans=DocumentVectorSpaceModel(SortedDictionary,inp,inp2)
    print(Ans)
    return(Ans)
    
def Nothing():
    return([])






if __name__=="__main__":
    term=""
    alpha=0.0005
    try:
        j=0
        for i in sys.argv:
            if j>=2:
                term+=i
                term+=" "
            j+=1
        print(term)
        alpha=float(sys.argv[1])
        main(term,alpha)
    except:
        Nothing()




