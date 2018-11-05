from django.http import JsonResponse
import random
#Ta funkcja wyniki dla wybranej gry i zwraca je dla boxa.
def roll (request):
    if request.is_ajax():
        radio = request.POST['gamesel']
        lst1 = []
        if radio == "1" :
            lst1.append(sorted(random.sample(list(range(1,81)),k=20)))
            print(lst1)
        elif radio == "2" :
            lst1.append(sorted(random.sample(list(range(1,50)),k=6)))
        elif radio == "3" :
            lst1.append(sorted(random.sample(list(range(1,43)),k=5)))
        elif radio == "4" :
            lst1.append(sorted(random.sample(list(range(1,36)),k=5)))
            lst1.append(random.sample(list(range(1,5)),k=1))
            print(lst1)
        else:
            pass
        responsedata = {
            'number' : lst1
        }
        return JsonResponse(responsedata)
