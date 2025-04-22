import re
import math
from django.shortcuts import render, redirect


def index(request):
    tables = request.session.get('tables', [])
    if request.method == "POST":
        print(request.FILES)
        if "txt" in request.FILES:
            file = request.FILES["txt"]
            text = file.read().decode('utf-8')
            text = re.sub(r'[^\w\s]', '', text)
            text = text.replace('\r', ' ').replace('\n', ' ').split(" ")
            words = list(filter(None, text))
            words = list(map(str.lower, words))
            wordsDict = {}
            for word in words:
                if word not in wordsDict.keys():
                    wordsDict[word] = {"pretf":1, "tf":0, "preidf":0, "idf":0}
                else:
                    wordsDict[word]["pretf"] += 1                    
                    
            tables.append(wordsDict)


            for table in tables:
                for word in table:
                    table[word]["preidf"] = 0
                    for i in range(len(tables)):
                        if word in tables[i].keys():
                            table[word]["preidf"] += 1

                                
                    table[word]["idf"] = math.log10( len(tables) / table[word]["preidf"])
                    print(word, "preidf", table[word]["preidf"], len(tables))
                    table[word]["tf"] = table[word]["pretf"] / len(table.keys())
                    #print(f"tf: {word}", table[word]["pretf"], len(table.keys()), table[word]["tf"])
            request.session['tables'] = tables
            return redirect('index')
        if 'reset' in request.POST:
            request.session['tables'] = []
            request.session.modified = True
            return redirect('index')
    
        

    return render(request, "index.html", {"tables":tables})