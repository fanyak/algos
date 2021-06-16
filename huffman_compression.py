# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 11:06:14 2021

@author: Panos
"""
import heapq
import numpy as np
import matplotlib.pyplot as plt;
import string;
import re
import time
import os

# Δημιουργία κόμβου σε ένα δένδρο Huffman.
class Tree:
    def __init__(self,p,left,right=None):
        self.p = p          # η συχνότητα με τη μορφή πιθανότητας που σχετίζεται με τον κομβο
        self.left = left    # αριστερός θυγατρικός κόμβος
        self.right = right  # δεξιός θυγατρικός κόμοβς (None αν ο κόμβος είναι φύλλο)
        # με την χρήση του depth προτιμούμε να συγχωνεύουμε
        # δέντρα με μικρό ύψος όταν οι κόμβοι έχουν την ίδια συχνότητα
        self.depth = 1 if right is None \
                     else 1 + max(self.left.depth,self.right.depth)

    # συγκρίση 2 κόμβων.
    # αν 2 κόμβοι έχουν την ίδια συχνότητα (πιθανότητα) προτιμούμε αυτόν που έχει μικρότερο ύψος
    def __lt__(self,other):
        return self.p < other.p or \
               (self.p == other.p and self.depth < other.depth)

    # ελεγχος για το αν ο κόμβος είναι φύλλο (δεν έχει θυγατρικούς κομβους)
    def isLeaf(self):
        return self.depth == 1

    # κώδικας με αναδρομή για να δημιουργήσυμε το λεξικό κωδικοποίησης
    # βρίσκοντας όλα τους κόμβους που είναι φύλλα
    def walk(self,encode_dict,prefix):
        if self.isLeaf():
            encode_dict[self.left] = prefix
        else:
            self.left.walk(encode_dict,prefix+[0])# add 0 if we move to the left
            self.right.walk(encode_dict,prefix+[1]) # add 1 if we move to the right

######################################## Κωδικοποίηση #########################################
# ορίσματα συνάρτησης:
#   plist -- σειρά που περιλαμβάνει τα tuples (πιθανότητα,χαρακτήρας)
# επιστρέφει:
#   (dict,tree) όπου
#     dict είναι το λεξικό που αντιστοιχίζει τον χαρακτήρα με την κωδικοποίηση
#     δέντρο είναι το δέντρο Huffman που δημιουργείται από τον αλγόριθμο.
def huffman(plist):
    # initialize set of tree nodes as leaves of the tree
    tlist = [Tree(p,obj) for p,obj in plist]

    # Δημουργούμε το δέντρο Huffman ακολουθώντας τον αλγόριθμό

    # αριθμός υπάρχοντων κόμβων
    n = len(tlist);
    # χρησιμοποιούμε the heapq module για να δημουργήσουμε αυτόματα την ουρά προτεραιότητας 
    # από τη λίστα μας
    heapq.heapify(tlist);
    for i in range(n-1):
        # αφαιρούμε από τον σωρό τους κόμβους που έχουν τη μικρότερη πιθανότητα
        left_child = heapq.heappop(tlist); # αριστερός θυγατρικός κόμβος
        right_child = heapq.heappop(tlist); # δεξιός θυγατρικός κόμβος
        # δημιουργούμε την πιθανότητα από την συγχώνευση των κόμβων
        propability = left_child.p + right_child.p 
        # δημιουργούμε νέο κόμβο με τους 2 παραπάνω θυγατρικούς και τη νέα πιθανότητα που υπολογίσαμε
        new_node = Tree(propability,left_child,right_child) 
        # προσθέτουμε τον νέο κόμβο στο σωρό
        heapq.heappush(tlist,new_node);

    # δημιουργούμε το λεξικό με τις κωδικοποιήσεις των χαρακτήρων
    root = tlist[0]
    encoding_dict = {}
    root.walk(encoding_dict,[])

    # επιστρέφουμε 1 tuple με το λεξικό και το δέντρο huffman
    return (encoding_dict,root)

def encode(encoding_dict,message):
    return np.concatenate([encoding_dict[obj] for obj in message])

######################################## Αποκωδικοποίηση #########################################

# ορίσματα:
#   το κωδικοποιημένο μήνυμα -- numpy array από 0's and 1's
#   huffman_tree -- η ρίζα του δέντρου  Huffman 
# επιστρέφουμε:
#  σειρά από αποδικωποιημένα σύμφβολα
def decode(huffman_tree,encoded_message, cdict):
    result = []

    # Χρησιμοποιούμα τα δυφία για να επιλέξουμε κατεύθυνση στο δέντρο
    # όταν φτάσουμε σε φύλλο, έχουμε βρει τον χαρακτήρα που αντιστοιχή στην κωδικοποίηση   
    next_node = huffman_tree;
    current = [];
    for bit in encoded_message:
        if bit:
            next_node = next_node.right
        else:
            next_node = next_node.left;
        current.append(bit);
        if next_node.isLeaf():
            for el in cdict:
                if cdict[el] == current:
                    result.append(el)
                    current = [];
            next_node = huffman_tree;

    # return the result sequence
    return result;

# gather the data in lists to display later in plot
x = []
y = []

for i in range (7):
    fname = './text%s.txt' %(i+1);
    with open(fname) as file:
        file_size = os.path.getsize(fname)
        x.append(file_size)
        prob_dict = {char: 0 for char in string.ascii_lowercase}
        txt = [];
        total = 0;
        line = file.readline()
        while line:
            l = re.sub(r'\W', ' ', line).strip() 
            l = re.sub(r'\s+', ' ', l).lower()
            total += len(re.sub(r'\s', '', l))        
            for w in l:
                if w in prob_dict:
                    prob_dict[w] += 1;
            txt.extend(l.split(' '))
            line = file.readline();
    
    for w in prob_dict:
        prob_dict[w] /= total;
        
    prob_tupple = [(prob_dict[w], w) for w in prob_dict]
    encoding_dict,root = huffman(prob_tupple)
    
    start_time = time.time()
    
    for t in txt:
        if(t):
            encoded_message = encode(encoding_dict,list(t))
            decoded_message = decode(root,encoded_message, encoding_dict)
            if t !=''.join(decoded_message):
                raise Exception('no match found {} {}'.format(t,''.join(decoded_message)))
    t = (time.time() - start_time)
    print("--- %s seconds ---" % (round(t,3)), 'for size %s' %(file_size))
    y.append(round(t,3))

    
plt.scatter(x,y)
plt.xlabel('size of text in bytes')
plt.ylabel('execution time in seconds');
plt.savefig('./plot.png')

        

        
