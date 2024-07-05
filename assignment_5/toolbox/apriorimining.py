# Based on script by github user nalinaksh 
# Adapted by Lisa Tostrams (august 2017)
from __future__ import print_function
import itertools
import os

"""apriori_gen function to compute candidate k-itemset, (Ck) , using frequent (k-1)-itemset, (Lk_1)"""
def apriori_gen(Lk_1, k):
    length = k
    Ck = [] 
    for list1 in Lk_1:
        for list2 in Lk_1:
            count = 0
            c = []
            if list1 != list2:
                while count < length-1:
                    if list1[count] != list2[count]:
                        break
                    else:
                        count += 1
                else:
                    if list1[length-1] < list2[length-1]:
                        for item in list1:
                            c.append(item)
                        c.append(list2[length-1])
                        if not has_infrequent_subset(c, Lk_1, k):
                            Ck.append(c) 
                            c = []
    return Ck


"""function to compute 'm' element subsets of a set S"""
def findsubsets(S,m):
    return set(itertools.combinations(S, m))


"""has_infrequent_subsets function to determine if pruning is required to remove unfruitful candidates (c) using the Apriori property, with prior knowledge of frequent (k-1)-itemset (Lk_1)"""
def has_infrequent_subset(c, Lk_1, k):
    list = []
    list = findsubsets(c,k)
    for item in list: 
        s = []
        for l in item:
            s.append(l)
        s.sort()
        if s not in Lk_1:
            return True
    return False


"""frequent_itemsets function to compute all frequent itemsets"""
def frequent_itemsets(L1, D, support):
    k = 2
    Lk_1 = []
    Lk = []
    L = []
    L.append(L1)
    count = 0
    transactions = 0
    for item in L1:
        Lk_1.append([item[0][0]])
    while Lk_1 != []:
        Ck = []
        Lk = []
        Ck = apriori_gen(Lk_1, k-1)
        for c in Ck:
            count = 0
            transactions = 0
            s = set(c)
            for T in D:
                transactions += 1
                t = set(T)
                if s.issubset(t) == True:
                    count += 1
            if (count/transactions) >= support:
                c.sort()
                Lk.append((c, ('sup=', round(count/transactions,2))))
        Lk_1 = []
        if(len(Lk)>0):
            print ("-------TOP 10 (or less) FREQUENT %d-ITEMSET------------------------" % k)
            print (*['set= {{ {} }},  {} {}'.format(', '.join(item[0]),item[1][0],item[1][1]) for item in sorted(Lk, key=lambda item: item[1][1], reverse=True)][:10],sep='\n')
            print ("------------------------------------------------------------------")
        for l in Lk:
            Lk_1.append(l[0])
        k += 1
        if Lk != []:
            L.append(Lk)
    
    return L
     
        


def generate_association_rules(filename, support, confidence, max_rules=0, names = None):
    """
    function to mine and print all the association rules with given min support and confidence value.
    
    
    Parameters
    ----------
    filename : str
        The filename of the file which is to be loaded
    support: float
        The support, given as a fraction (0-1) of the wanted association rules.
    confidence: float
        The confidence, given as a fraction (0-1) of the wanted association rules.
    max_rules: int, optional
        The maximum number of association rules that need to be displayed (default is 0)
        If zero, all rules will be printed
    names: dict, optional
        A dictionary of names, the file that is to be mined needs to contain the keys. (default is None)
        If None, the rules will just print the keys as found in the dataset.
    """
    
    
    """Compute candidate 1-itemset"""
    C1 = {}
    """total number of transactions contained in the file"""
    transactions = 0.0
    D = []
    T = []
    with open(filename, "r") as f:
        for line in f:
            T = []
            transactions += 1
            for word in line.split(','):
                word = word.rstrip()
                
                #Use dictionary for names
                if names is not None:
                    T.append(names[word])
                    if names[word] not in C1.keys():
                        C1[names[word]] = 1
                    else:
                        count = C1[names[word]]
                        C1[names[word]] = count + 1
                          
                #Don't use dictionary for names
                else:
                    T.append(word)
                    if word not in C1.keys():
                        C1[word] = 1
                    else:
                        count = C1[word]
                        C1[word] = count + 1
            D.append(T)

    """Compute frequent 1-itemset"""
    L1 = []
    for key in C1:
        if (C1[key]/transactions) >= support:
            L1.append(([key],('sup=', round(C1[key]/transactions,2))))

    print ("---------------TOP 10 FREQUENT 1-ITEMSET-------------------------")
    print (*['set= {{ {} }},  {} {}'.format(item[0][0],item[1][0],item[1][1]) for item in sorted(L1, key=lambda item: item[1][1], reverse=True)][:10],sep='\n')
    print ("-----------------------------------------------------------------")

    
    s = []
    r = []
    length = 0
    count = 1
    inc1 = 0
    inc2 = 0
    num = 1
    m = []
    L= frequent_itemsets(L1, D, support)
    print ("---------------------ASSOCIATION RULES------------------")
    print ("--------------------------------------------------------")
    RULES = []
    for list in L: #for each group of K size frequent itemsets e.g. all size 3 frequent itemssets
        for l in list: #for each frequent itemset e.g. {a,b,c}
            l = l[0] 
            length = len(l) 
            count = 0
            while count < length: #compute at all length <count> subsets of that itemset e.g. for count =2 {a,b} {a,c} {b,c}
                s = []
                r = findsubsets(l,count)
                count += 1
                for item in r:  #for each length <count> subset of the frequent itemset e.g. {a,b}
                    inc1 = 0
                    inc2 = 0
                    s = []
                    m = []
                    for i in item:
                        s.append(i)
                    for T in D:
                        if set(s).issubset(set(T)) == True:  #count how often that subset occurs e.g. {a,b} occurs 9 times
                            inc1 += 1
                        if set(l).issubset(set(T)) == True:  #count how often the frequent itemset occurs e.g. {a,b,c} occurs 5 times
                            inc2 += 1
                    if inc2/inc1 >= confidence:  #compute confidence of {a,b} => {c} == #{a,b,c}/#{a,b} %
                        for index in l:
                            if index not in s:
                                m.append(index)
                        RULES.append((num, s, m, inc2/len(D), inc2/inc1)) #add rule
                        
                        num += 1
    if(max_rules<1):
        max_rules=len(RULES)
    print (*["Rule #{}: {{ {} }} ==> {{ {} }}, sup= {:.2f}, conf= {:.2f}".format(r[0],', '.join(r[1]),', '.join(r[2]),r[3],r[4]) for r in sorted(RULES,key=lambda r: r[4],reverse=True)][:max_rules],sep='\n\n')
    print ("--------------------------------------------------------")
  
