import numpy as np

def gray_code(n):
 
    # power of 2
    l = []
    for i in range(1 << n):
       
        # Generating the decimal
        # values of gray code then using
        # bitset to convert them to binary form
        val = (i ^ (i >> 1))
         
        # Converting to binary string
        s = bin(val)[2::]
        l.append(s.zfill(n))
    return l