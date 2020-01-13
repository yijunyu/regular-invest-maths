#Problem: see https://github.com/yijunyu/regular-invest-maths/blob/master/Mixin_BTC-v1.0.pdf
# 
import matplotlib.pyplot as plt
import numpy as np
import math
import array
from random import random

prize = 0.000001 # 100 satoshi
pool = 1000 # amount of BTC in the intial pool
m = 100000 # number of participants initially
balance = array.array('f', range(m))
total_balance = array.array('f', range(m))
debt = 0.0

states = array.array('i', range(m))

p0 = 0.005 # new participants spawned s0

### p1, or 1-p1 are the transitions on state 0
p1 = 0.99 # probability of continue taking the prize

### p2, p3, or 1-p2-p3 are the transitions on state 1
p2 = 0.8 # succeed in collect btc
p3 = 0.2 # decide not to quit

### p4, p5, or 1-p4-p5 are the transitions on state 2
p4 = 0.4 # decide to transfer to fiat
p5 = 0.4 # decide to transfer back from fiat

# initialisation
for i in range(m):
    balance[i] = 0 # initial balance is 0
    total_balance[i] = 0 # initial total balance is 0
    states[i] = 0 # initial state is s0

day = 0
while pool - debt > prize:
    day+=1
    M = 0
    m2 = m
    for i in range(m):
        if states[i] == 0 or states[i] == 1 or states[i] == 2:
            M += 1
        if random() < p0:
            m2 += 1
    s2 = array.array("i", range(m2))
    b2 = array.array("f", range(m2))
    tb2 = array.array("f", range(m2))
    s2[:m] = states
    b2[:m] = balance
    tb2[:m] = total_balance
    for i in range(m2-m):
        s2[m + i] = 0
        b2[m + i] = 0.0
        tb2[ m+i] = 0.0
    states = s2
    balance = b2
    total_balance = tb2
    m = m2
    # print("m = %d " % m)
    if M == 0: # no more participants
        print ("no more participants")
        break
    for i in range(m):
        if states[i] == 3:
            continue
        r = random() # a decision is made randomly
        n = int((math.sqrt(8 * balance[i]/prize + 1) - 1)/2) # number of days in the current collecting streak
        pr = (n + 1) * prize
        if(states[i] == 0 and r < p1):
            balance[i] += pr
            total_balance[i] += pr
            states[i] = 1 # change to s1
        elif(states[i] == 1 and r < p2): # succeed in the free task, keep collecting
            balance[i] += pr
            total_balance[i] += pr
            states[i] = 2
        elif(states[i] == 1 and r < p2 + p3): # failed the free task, but keep collecting from beginning
            balance[i] = 0
            states[i] = 0
        elif(states[i] == 2):
            if r < p4: # transfer all total balance from BTC to fiat
                balance[i] = 0
                debt += total_balance[i]
                total_balance[i] = 0
                states[i] = 3
            elif r < p4 + p5 and total_balance[i] < n*(n+1)/2*prize: # transfer sufficient fund from fiat to BTC
                r1 = random()
                debt -= n*(n+1)/2*prize - total_balance[i] + r1 * prize * 100
                total_balance[i] = n*(n+1)/2*prize + r1 * prize * 100
                states[i] = 1
            else:
                states[i] = 1
    if day % 10 == 0:
        print("day = %d" % day)
        sum = 0
        for i in range(m):
            sum += total_balance[i]
        print("no of participants = %d" % M)
        print("total balances = %f" % sum)
        print("debt = %f" % debt)
