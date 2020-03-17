import string
import math
import operator

vocabulario = {}
idf = {}
vecDoc = {}
norma = {}

def addTerm(id,term):
    if term in vocabulario: # verifica se o termo esta no vocabulario
        listaInvertida = vocabulario[term] # se sim, recupera a lista invertida
        if id in listaInvertida:           # verifica se o termo ja foi mencionado no mesmo documento
            listaInvertida[id] += 1
        else:                              # se nao tiver na lista invertida, adiciona o termo com frequencia 1
            listaInvertida[id] = 1
    else:
        vocabulario[term] = {id:1}         # caso nao esteja no vocabulario, adiciona o termo e inicializa sua lista invertida

def criaVocabulario(id, terms):
    for term in terms:
        addTerm(id,term)

def calculaIdf(N):
    for term, listaInvertida in vocabulario.items():
        n = len(listaInvertida)
        termIdf = round(math.log10(N/float(n)), 2)
        idf[term] = termIdf

def calculaTfIdf(idTerm, term, listaInvertida):
    for docId,freq in listaInvertida.items():
        pesos = vecDoc[docId]
        pesos[idTerm] = freq * idf[term]

def printVetores(vetores):
    for id, lista in vetores.items():
        strPesos = "\t"
        for peso in lista:
            strPesos += " " + str(peso)
        print (str(id) + strPesos)

def calculaPesos(docs):

    # inicializa vetor de documentos
    for id,doc in docs.items():
        vecDoc[id] = [0] * len(vocabulario)


    counter = 0 #identificacao do id dos termos na ordem do dicionario
    for term,listaInvertida in vocabulario.items():
        calculaTfIdf(counter, term, listaInvertida)
        counter += 1

def calculaNormas():

    for id,listaInv in vecDoc.items():
        acc = 0
        for peso in listaInv:
            acc += peso**2
        norma[id]=round(math.sqrt(acc),2)

def indexador():
    # colecao de documentos
    docs = {
                1: "To do is to be. To be is to do.",
                2: "To be or not to be. I am what I am.",
                3: "I think therefore I am. Do be do be do.",
                4: "Do do do, da da da. Let it be, let it be."
            }

    for id, doc in docs.items():
        doc = doc.lower() # todos os caracteres em minusculo
        doc = doc.translate(None, string.punctuation) #remove todas as pontuacoes
        terms = doc.split() # separar os termos do documentos
        criaVocabulario(id,terms) #adiciona vocabulario

    calculaIdf(len(docs))
    calculaPesos(docs)
    calculaNormas()

###################################################################################
###################################################################################
################################Processador de consultas###########################
###################################################################################
###################################################################################

vocabularioQ = {}
normaQ = 0
q = "to do"

def addTermQ(id,term):
    if term in vocabularioQ: # verifica se o termo esta no vocabulario
        listaInvertida = vocabularioQ[term] # se sim, recupera a lista invertida
        if id in listaInvertida:           # verifica se o termo ja foi mencionado no mesmo documento
            listaInvertida[id] += 1
        else:                              # se nao tiver na lista invertida, adiciona o termo com frequencia 1
            listaInvertida[id] = 1
    else:
        vocabularioQ[term] = {id:1}         # caso nao esteja no vocabulario, adiciona o termo e inicializa sua lista invertida

def criaVocabularioQ(id, terms):
    for term in terms:
        addTermQ(id,term)

def pegaPosicaoTerm(termQ):
    counter = 0 #identificacao do id dos termos na ordem do dicionario
    for term,listaInvertida in vocabulario.items():
        if termQ == term:
            return counter
        counter += 1

def produtoVetorial(vec1,vec2):
    if(len(vec1) == len(vec2)):
        tam = len(vec1)
        acc = 0
        for i in range(tam):
            acc += vec1[i] * vec2[i]
        return acc
    else:
        print("Tamanho dos vetores diferente")
        exit(1)

def processadorConsultas():
    #Passos para criar o processador de consultas:
    #1. normalizar os termos
    global normaQ
    global q
    q = q.lower()
    q = q.translate(None, string.punctuation)
    terms = q.split()
    criaVocabularioQ(0,terms)

    # #2. vetor da consulta (tamanho do vocabulario)
    vecQ = [0] * len(vocabulario)

    counter = 0 #identificacao do id dos termos na ordem do dicionario
    for term,listaInvertida in vocabularioQ.items():
        idfTerm = idf[term]
        pos = pegaPosicaoTerm(term)
        lista = vocabularioQ[term]
        vecQ[pos] = lista[0] * idfTerm

    #3. norma do vetor
    acc = 0
    for peso in vecQ:
        acc += peso**2
    normaQ = round(math.sqrt(acc),2)

    sim = {}
    #4. calculo de similaridade entre consulta e documentos indexados
    for id,vetorDoc in vecDoc.items():
        valorProduto = produtoVetorial(vecQ,vetorDoc)
        sim[id] = valorProduto / (normaQ*norma[id])

    #5. ranking de similaridades
    sorted_sim = sorted(sim.items(), key=operator.itemgetter(1), reverse=True) # ornade o rankind de similaridades
    print("******Ranking para consulta******")
    for docId,s in sorted_sim:
        print("Documento " + str(docId) + ": " + str(s))

def main():
    indexador()
    processadorConsultas()

if __name__ == '__main__':
    main()
