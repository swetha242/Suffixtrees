#Assignment done by S.Swetha(01FB15ECS250)
import string
import operator
file = open('AesopTales.txt','r')
s=''#stores all stories(only story and not title)
cnt=0
c=0
f_occur=[]
title=[]#stores all titles
first=1

def generate_substr(s):#generate substrings
    l=len(s)
    lst=[s[i:j+1] for i in range(l) for j in range(i,l)]
    lst=sorted(lst,key=len)#sort list based on length
    lst.reverse()#lst has substrings stored in decreasing order of length
    return(lst)
for line in file:#Processing input
    line=line.strip('\n')
    line = line.strip('\t')
    line = line.strip(' ')
    if (cnt != 2 and line != '' and first==0):
        #print(line)
        s += ' '+line   #content stored in s
    # count is 2 when we read title of next story
    if(line!='' and (first or cnt==2)):
        title.append(line) #titles stored in list title
        first=0
        if(cnt>=2):
            s+='$' #all stories separated by a $
    if(line==''):
        cnt+=1#increment every time you encounter a new line/empty string
        #print('---------------')
    else:
        cnt=0
#print(s)
l=s.split('$')#l is a list of stories
cont=[]#list of contents of all stories
idx=[]#list of list of indexes of fullstops
#remove newline characters and spaces at end of sentences of each story
for i in l:
    j=i.split('.')#j is a list of sentences in each story i
    for k in range(len(j)):
        j[k]=j[k].strip('\n')#remove spaces and newline at end of sentences
        j[k]=j[k].strip(' ')
    i='.'.join(j)

    i=i.strip(' ')

    cont.append(i)#content of each document stored here

class SuffixTree(object):
    class Node(object):
        def __init__(self,fr,to):
            self.fr = fr  # starting index of label
            self.to=to  #ending index
            self.out = {}  # outgoing edges; maps characters to nodes
            self.docs=[] #list of all occurances(empty for non-leaf nodes)
    def __init__(self, s):
        """ Make suffix tree, without suffix links, from s in quadratic time
            and linear space """
        s += '$'
        self.root = self.Node(None,None)
        l=len(s)
        for i in range(l):
            # start at root; we’ll walk down as far as we can go
            cur = self.root
            j = i
            while j < l:
                if s[j] in cur.out:#node mapped by s[j] exists
                    child = cur.out[s[j]]
                    # Walk along edge until we exhaust edge label or
                    # until we mismatch
                    k = j + 1
                    fr=child.fr
                    to=child.to
                    dif=to-fr #length of label
                    #compare label of node and suffix of s
                    while k - j < dif and s[k] == s[k - j + fr]:
                        k += 1
                    if k - j == dif:
                        cur = child  # we exhausted the edge i.e entire label
                        j = k
                    else:#mismatch occured in middle of label
                            # create new node whose label is the matched portion
                            split=self.Node(fr,k-j+fr)
                            # create new node mapped by s[k] where k is index of mismatch in suffix
                            split.out[s[k]]=self.Node(k,l)
                            #Append occurance to new node
                            split.out[s[k]].docs=[j]
                            #old node becomes a child of split
                            #it is mapped by index of mismatch in the label
                            split.out[s[k-j+fr]]=child
                            child.fr=k-j+fr
                            child.to=l
                            #make split a child of cur
                            cur.out[s[j]]=split
                            break

                else:
                    # Fell off tree at a node: make new edge hanging off it
                    cur.out[s[j]] = self.Node(j,len(s))
                    #append index
                    cur.out[s[j]].docs.append(j)

    def followPath(self, s,k):
        """ Follow path given by s.  If s doesn't exist in tree, return None.If we
            finish mid-edge or on a node, return node"""
        cur = self.root
        i = 0
        l=len(s)
        while i < l:
            c = s[i]
            if c not in cur.out:
                return None # s not in tree
            child = cur.out[s[i]]
            fr = child.fr
            to=child.to
            dif=to-fr
            j = i + 1
            #compare node label and query string s
            while j - i < dif and j < len(s) and s[j] == cont[k][j - i + fr]:
                j += 1
            if j - i == dif:
                cur = child  # exhausted edge
                i = j
            elif j == len(s):
                return child  # exhausted query string in middle of edge
            else:
                return None # fell off in the middle of the edge
        return cur # exhausted query string at internal node

    def alloccur(self, s,c):
        """ print all occurances of s """
        node = self.followPath(s,c)
        l = len(s) - 1
        if node is not None:
            if len(node.out)==0:#leaf node
                occur = node.docs#all occurances
                #print('--------------------ALL OCCURANCES-------------------------')
                print('\nQuerystring ' + '"' + s + '"' + ' PRESENT in:')
                print('\nTitle: ', title[c])
                for i in occur:
                        self.printres(c, i, l)
                        print('\n')
            else:
                print('\nQuerystring ' + '"' + s + '"' + ' PRESENT in:')
                print('\nTitle: ', title[c])
                #if not leaf node, do dfs to get the occurances
                self.dfs(node,c,l)
        else:
            print('"'+s+'"'+ ' NOT PRESENT in '+title[c])

    def firstoccur(self, s,c):
            """ print 1st occurance, if s not present print 1st occurance
             of longest substring"""
            node = self.followPath(s,c)
            l = len(s) - 1
            global f_occur
            print('--------------------FIRST OCCURANCE-----------------------------')
            if node is not None:
                if len(node.out)==0:#leaf
                    occur = node.docs
                    print('\nQuerystring ' + '"' + s + '"' + ' occurs in:')
                    print('Title: ', title[c])
                    j = occur[0]#first occurance
                    self.printres(c, j, l)
                else:
                    f_occur=[]#stores all occurances of s
                    self.dfs1(node, c, l)
                    print('\nQuerystring ' + '"' + s + '"' + ' occurs in:')
                    print('Title: ', title[c])
                    j=min(f_occur)#find first occurance
                    self.printres(c, j, l)


            else:

                subs = generate_substr(s)  # returns a list of substrings of s ordered by length(descending)
                for i in subs:
                    node1 = self.followPath(i,c)
                    l = len(i) - 1
                    if node1 is not None:#substring i in tree
                        if len(node1.out) == 0:  # leaf
                            occur = node1.docs
                            print('\nSubstring ' + '"' + i + '"' + ' occurs in:')
                            print('Title: ', title[c])
                            j = occur[0]
                            self.printres(c, j, l)
                        else:

                            f_occur = []
                            self.dfs1(node1, c, l)
                            print('\nQuerystring ' + '"' + i + '"' + ' occurs in:')
                            print('Title: ', title[c])
                            j = min(f_occur)
                            self.printres(c, j, l)
                        break





    def printres(self, i, j, l):
        """ Given document no(i),index of query string(j) and length of query string(l)
        print the sentence(s) in which it is present"""
        idx=j
        k=j+l-1
        #find index of previous fullstop
        while(j>=0):
            if(cont[i][j]=='.'):
                break
            j-=1
        #find index of next fullstop
        while(k<len(cont[i])):
            if (cont[i][k] == '.'):
                break
            k += 1
        if(j==-1):
            if(k==len(cont[i])-1):
                print('Sentence:', cont[i])
            else:
                print('Sentence:', cont[i][:k+1])
        else:
            print('Sentence:', cont[i][j+1:k+1])
        print('Index:',idx)
        print()


    def relevance(self,s,c,subs):
        """Stories that have exact query string have highest rank.Stories that
        have all words of querystring have higher relevance than those which has
        a subset"""
        node=self.followPath(s,c)
        #if exact querystring present return no of words plus one
        if node is not None:
            return(len(subs)+1)
        else:
            #no_occur stores no of words of s present in story
            no_occur=0
            for i in subs:
                node=self.followPath(i,c)
                #if i in tree increment no_occur
                if node is not None:
                    no_occur+=1
            return(no_occur)


    def dfs(self,node,c,l):
        if len(node.out)==0:#leaf
            occur=node.docs
            for j in occur:
                self.printres(c,j,l)
        for i in node.out.values():
            self.dfs(i,c,l)

    def dfs1(self,node,c,l):
        if len(node.out)==0:#leaf
            occur=node.docs
            #append occurances in a global list f_occur
            for j in occur:
                f_occur.append(j)
        for i in node.out.values():
            self.dfs1(i,c,l)

print('Enter query string')
q=input().strip('\n')
print('1-Find all occurences in all documents')
print('2-Find first occurence of longest possible substring in all documents')
print('3-Rank documents based on relevance')
print('Enter choice')
ch=int(input().strip('\n'))
#dictionary where key is story no. and value is relevance
rel={}
if(ch in [1,2,3]):
    if(ch==3):
        delim = ['\"', ',', '.', ' ', ';', ':', '?']
        subs = []  # store all words in querystring q
        tmp = ''
        st = list(q)
        for i in st:
            if i not in delim:
                tmp += i
            else:
                if tmp not in delim:
                    subs.append(tmp)
                tmp = ''
        if tmp not in delim:
            subs.append(tmp)
        no_sub=len(subs) #no of words in querystring q
    for i in range(len(cont)):
        #create suffix tree for every story
        stree=SuffixTree(cont[i])
        print('------------------------------------------------------------')
        if(ch==1):
            stree.alloccur(q,i)
        elif(ch==2):
            stree.firstoccur(q,i)
        else:
            rel[i]=stree.relevance(q,i,subs)
            print('Title :'+title[i])
            if(rel[i]==no_sub+1):
                print('Entire query string matched')
            else:
                print(rel[i],' words matched')

    if(ch==3):
        #sort dictionary based on value(i.e relevance)
        rel=sorted(rel.items(),key=operator.itemgetter(1))
        #rel is a list of tuples (i,j) where i is index of story and j is relevance
        #reverse rel,rel is sorted in descending order of relevance
        rel.reverse()
        rank=1
        #Assign rank for each document
        #Two or more documents have the same rank if they have equal no_occur
        no_occ=rel[0][1]
        print('\nRank:',rank)
        if(no_occ==no_sub+1):
            print('Entire query string matched')
        else:
            print(no_occ,'words of '+q+' occurs in:')
        print('Title: ', title[rel[0][0]])
        for i in range(1,len(rel)):
                    if(no_occ==rel[i][1]):
                        print('\nRank:', rank)
                        print(no_occ, 'words of ' + q + ' occurs in:')
                        print('Title: ', title[rel[i][0]])
                    else:
                        rank+=1
                        no_occ=rel[i][1]
                        print('\nRank:', rank)
                        print(no_occ, 'words of ' + q + ' occurs in:')
                        print('Title: ', title[rel[i][0]])


