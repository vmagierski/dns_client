
''' 
check if the nth bit of provided byte is set

return true if n'th bit is set to 1, False otherwise

n starts numbering from left 

i.e.

      1 0 1 1 1 0 0 0

      ^ ^ ^ ^ ^ ^ ^ ^
      | | | | | | | | 
n=    0 1 2 3 4 5 6 7


'''
def is_set(n, somebyte):
    if (n < 0 or n > 7):
        print('n must be 0 <= n <= 7')
        print("n=" + str(n))
        raise ValueError('n index should be between 0 and 7, was not')


    if (len(somebyte) != 1):
        raise ValueError('can only take one byte')

    i = 7 - n

    return True if somebyte[0] & (1 << i) > 0 else False