import re
import math
from django.shortcuts import render, redirect


def index(request):
    tables = request.session.get('tables', [])
    if request.method == "POST":
        if "txt" in request.FILES:
            file = request.FILES["txt"]
            text = file.read().decode('utf-8')
            text = re.sub(r'[^\w\s]', '', text)
            text = text.replace('\r', ' ').replace('\n', ' ').split(" ")
            words = list(filter(None, text))
            words = list(map(str.lower, words))
            wordsLst = []

            for word in words:
                if wordsLst != []:
                    is_append = True
                    for wordLst in wordsLst:
                        if word in list(wordLst.keys())[0]: 
                            is_append = False                           
                            break
                    if is_append:
                        wordsLst.append({word:{"tf":words.count(word)/len(words), "preidf":0, "idf":0}})
                else:
                    wordsLst.append({word:{"tf":words.count(word)/len(words), "preidf":0, "idf":0}})                   
            tables.append(wordsLst)
            
            # Добавляя новую таблицу нужно пересчитывать IDF для всех таблиц, устанавливая у каждого слова его на 0
            for table in tables:
                for word in table:
                    word[list(word.keys())[0]]["preidf"] = 0
                    for tab in tables:
                        for wrd in tab:
                            if list(word.keys())[0] in list(wrd.keys())[0]:
                                word[list(word.keys())[0]]["preidf"] += 1
                                break
                    print(len(tables), word[list(word.keys())[0]]["preidf"])
                    word[list(word.keys())[0]]["idf"] = math.log10(len(tables) / (word[list(word.keys())[0]]["preidf"] if word[list(word.keys())[0]]["preidf"] > 0 else 1))
            
            request.session['tables'] = tables
            return redirect('index')
        if 'reset' in request.POST:
            request.session['tables'] = []
            request.session.modified = True
            return redirect('index')
    

    new_tables = []  
    for table in tables:
        new_table = []
        for word in table:
            key = list(word.keys())[0]
            tf = word[key]["tf"]
            idf = word[key]["idf"]
            new_table.append({"word": key, "tf": tf, "idf": idf})
        new_table = sorted(new_table, key=lambda x:x['idf'], reverse=True)
        new_tables.append(new_table[:50])
    output = {"tables":new_tables}
    return render(request, "index.html", output)


#for table in tables: # table список словарей с ключом - значением словарём
            #    for i, word in enumerate(table): # word словарь с ключом - значением словарём
            #        print("Таблица и слово: ", table, list(word.keys())[0])
            #        table[i][list(word.keys())[0]]["preidf"] = 0
            #        for j in range(len(tables)):   
            #            if any(list(word.keys())[0] in x for x in tables[j]):
            #                print('table[i][list(word.keys())[0]]["preidf"] += 1 - ', list(word.keys())[0], table[j][list(word.keys())[0]])
            #                table[i][list(word.keys())[0]]["preidf"] += 1                                
            #        table[i][list(word.keys())[0]]["idf"] = math.log10(len(tables) / table[i][list(word.keys())[0]]["preidf"])
            #        #print(word, "preidf", table[word]["preidf"], len(tables))
            #        table[i][list(word.keys())[0]]["tf"] = table[i][list(word.keys())[0]]["pretf"] / len(table)
            #        #print(f"tf: {word}", table[word]["pretf"], len(table.keys()), table[word]["tf"])




                #for index, table in enumerate(tables):
    #    print("index: ",index, "table: ", type(table))
    #    sortedLstDct = sorted(lstDct, key=lambda x: list(x.values())[0]["key"], reverse=True)
    #    #table = sorted(table, key=lambda x:x['idf'], reverse=True)
    #    #tables[index] = table


    #for word in words:
    #            print(word, type(word))
    #            if wordsLst != []:
    #                is_word_in = False
    #                for i, dict in enumerate(wordsLst):
    #                    if word in list(dict.keys())[0]:
    #                        is_word_in = [i, word]
    #                        break
    #                if is_word_in:
#
    #                    wordsLst[is_word_in[0]][is_word_in[1]]["pretf"] += 1
    #                else:
    #                    wordsLst.append({word:{"pretf":1, "tf":0, "preidf":0, "idf":0}})
    #            else:
    #                wordsLst.append({word:{"pretf":1, "tf":0, "preidf":0, "idf":0}})  