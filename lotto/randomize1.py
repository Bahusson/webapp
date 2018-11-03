import random

#Ta funkcja wyniki dla wybranej gry i zwraca je dla boxa.
def roll(radio):
    #list2.delete(0,END)
        lst1 = []
    if radio == 1 :
        lst1.append(sorted(random.sample(list(range(1,81)),k=20)))
        return lst1
    elif radio == 2 :
        lst1.append(sorted(random.sample(list(range(1,50)),k=6)))
        return lst1
    elif radio == 3 :
        lst1.append(sorted(random.sample(list(range(1,43)),k=5)))
        return lst1
    elif radio == 4 :
        lst1.append(sorted(random.sample(list(range(1,36)),k=5)))
        lst1.append(random.sample(list(range(1,5)),k=1))
        return lst1
    else:
        pass
