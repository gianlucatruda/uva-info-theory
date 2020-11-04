## copy right: https://repl.it/@Pathemeous/TextFrequencies#main.py by Wouter Smit
########### YOU DO NOT HAVE TO EDIT THIS PART #########

from collections import Counter
import math
import string
import re
import itertools

## parse input file, convert to lowercase, remove punctuation
f = open("/kaggle/input/hw2-input/input.txt")
data = f.read().lower()
regex = re.compile('[^a-z ]')
data = regex.sub('', data)

## create a dictionary containing the frequencies for all characters (incl. space)
alphabet = "abcdefghijklmnopqrstuvwxyz "
frequencies = {c:data.count(c) for c in alphabet}
total = sum(frequencies.values())

########### EDIT BELOW THIS LINE #########
list_p = []
entropy = 0
for c in alphabet:
  p = frequencies[c] / total
  list_p.append(p)
  summand = p * math.log2(1/p)
  entropy += summand

print("Entropy:", entropy)

tuples = (a+b for a in alphabet for b in alphabet)
conditionals = {t:data.count(t) for t in tuples}
ctotal = sum(conditionals.values())

list_q = []
joint_entropy = 0
for t in conditionals.keys():
  if conditionals[t] > 0:
    q = (conditionals[t] / ctotal)
    list_q.append(q)
    summand = q * math.log2(1/q)
    joint_entropy += summand

print("Joint Entropy:", joint_entropy)


## Cross-entropy between two distributions
from math import log2
def cross_entropy(p, q):
    cross_entropy = []
    for i in range(len(p)):
        for j in range(len(q)):
            cross_entropy.append(p[i]*log2(q[j]))
     
    return -sum(cross_entropy)

products = [a * b for a, b in zip(list_p, list_p)]
print("Cross Entropy:", cross_entropy(list_q, products)) 
