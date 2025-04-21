from django.shortcuts import render, redirect
import re
# Create your views here.

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
            wordsLst = []
            wordsDict = {}
            for word in words:
                if word not in wordsLst:
                    wordsLst.append(word)
                    wordsDict[word] = {"tf":1, "idf":0}
                else:
                    wordsDict[word]["tf"] += 1
            tables.append({wordsLst:wordsDict})
            request.session['tables'] = tables
            return redirect('index')

    return render(request, "index.html", {"tables":tables})