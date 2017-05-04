from time import time

def time_random():
 return time() - float(str(time()).split('.')[0])

def gen_random_range(val=32):
    min='1'
    min=min+(val-1)*'0'
    max=''
    max=max+val*'9'
    min=int(min)
    max=int(max)
    return int(time_random() * (max - min) + min)
