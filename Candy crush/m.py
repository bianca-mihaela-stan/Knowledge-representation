import copy
from heapq import heappush, heapify, heappop
import sys
import os
import time
from NodParcurgere import NodParcurgere
from Graph import Graph
from helpers import refactor

max_nodes_ucs = 0
max_nodes_a_star = 0
max_nodes_optimized_a_star = 0
max_nodes_ida_star = 0
max_nodes_ida_iteration=0
total_ucs_nodes = 0
total_noduri_a_star = 0
total_noduri_a_star_optimizat = 0
total_noduri_ida_star = 0

def initialize_file(out):
    out.write("<!DOCTYPE html>\n <html> \n <body> \n\n <p>")

def close_file(out):
    out.write("\n </p>\n </body> \n </html>")

def uniform_cost(out,  gr,  nrSolutiiCautate=1, timeOut = 60):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    global max_nodes_ucs, total_ucs_nodes
    max_nodes_ucs=0
    total_ucs_nodes=0
    
    initialize_file(out)
    c =[]
    gr.start = refactor(gr.start)
    heappush(c, NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start)))
    max_nodes_ucs =1
    total_ucs_nodes=1
    start_time = time.time()
    now = time.time()
    while len(c)>0 and now-start_time<timeOut:
        nodCurent=heappop(c)
        if gr.testeaza_scop(nodCurent):
            out.write("Solutie: <br>")
            nodCurent.afisDrum(out, time.time()-start_time, max_nodes_ucs, total_ucs_nodes, afisCost=True, afisLung=True)
            out.write("<br>----------------<br>")
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                out.write("Am gasit toate solutiile cautate.")
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent)
        for s in lSuccesori:
            heappush(c, s)
        max_nodes_ucs=max(max_nodes_ucs, len(c) + len(lSuccesori))
        total_ucs_nodes+=len(lSuccesori)
        now = time.time()
    if now - start_time >= timeOut:
        out.write("Timeout.<br>")
        print("Timeout")
    else:
        out.write("Nu mai exista solutii.<br>")
    close_file(out)


def a_star(out,  gr, tip_euristica="euristica banala", nrSolutiiCautate=1, timeOut = 60):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    global max_nodes_a_star, total_noduri_a_star
    max_nodes_a_star=0
    total_noduri_a_star=0
    
    initialize_file(out)
    c = []
    gr.start = refactor(gr.start)
    heappush(c, NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start)))
    max_nodes_a_star=1
    total_noduri_a_star=1
    start_time = time.time()
    now = time.time()
    while len(c) > 0 and now-start_time < timeOut:
        nodCurent = heappop(c)

        if gr.testeaza_scop(nodCurent):
            out.write("Solutie: <br>")
            nodCurent.afisDrum(out, time.time()-start_time, max_nodes_a_star, total_noduri_a_star, afisCost=True, afisLung=True)
            out.write("<br>----------------<br>")
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                out.write("Am gasit toate solutiile cerute.<br>")
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica)
        total_noduri_a_star+=len(lSuccesori) + len(c)
        for s in lSuccesori:
            heappush(c, s)
        max_nodes_a_star=max(max_nodes_ucs, len(c)+len(lSuccesori))
        now = time.time()
    if now - start_time >=timeOut:
        out.write("Timeout.<br>")
        print("Timeout")
    else:
        out.write("Nu mai exista solutii.<br>")
    close_file(out)


def a_star_optimizat(out,  gr, tip_euristica="euristica banala", nrSolutiiCautate=1, timeOut = 60):
    global max_nodes_optimized_a_star, total_noduri_a_star_optimizat
    max_nodes_optimized_a_star=0
    total_noduri_a_star_optimizat=0

    initialize_file(out)
    gr.start = refactor(gr.start)

    nodStart = NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))
    c = [nodStart]
    heapify(c)
    max_nodes_optimized_a_star=1
    total_noduri_a_star_optimizat=1

    closed = []

    start_time = time.time()
    now = time.time()
    while len(c) > 0 and now-start_time< timeOut:
        # iau un element din pq
        nodCurent = heappop(c)

        # il adaug la lista de closed
        closed.append(nodCurent)

        # verific daca e solutie
        if gr.testeaza_scop(nodCurent):
            out.write("Solutie: <br>")
            nodCurent.afisDrum(out, time.time()-start_time, max_nodes_optimized_a_star, total_noduri_a_star_optimizat, afisCost=True, afisLung=True)
            out.write("<br>----------------<br>")
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                out.write("S-au afisat toate solutiile cautate.<br>")
                return

        # daca nu e solutie generez succesorii
        lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica)
        max_nodes_optimized_a_star=max(max_nodes_optimized_a_star,
                                        len(lSuccesori) + len(closed) + len(c))
        total_noduri_a_star_optimizat += len(lSuccesori)

        # pentru fiecare succesor
        succesori_marcati = [False]*len(lSuccesori)
        c_marcat=-1
        closed_marcat= -1
        for s in lSuccesori:
            gasitC = False
            for nodC in c:
                nodC = nodC
                if s.info == nodC.info:
                    gasitC=True
                    if s.f >= nodC.f:
                        lSuccesori[:] = [x for x in lSuccesori if x!=s]
                    else:
                        c[:] = [x for x in c if x!=nodC]
            if not gasitC:
                for nodC in closed:
                    if s.info == nodC.info:
                        if s.f >= nodC.f:
                            lSuccesori[:] = [x for x in lSuccesori if x != s]
                        else:
                            closed[:] = [x for x in closed if x != nodC]
            heapify(c)
        for s in lSuccesori:
            heappush(c, s)
        now = time.time()
    if now-start_time>=timeOut:
        out.write("Timeout.<br>")
        print("Timeout")
    else:
        out.write("Nu mai sunt solutii.<br>")
    close_file(out)


def ida_star(out,  gr, tip_euristica="euristica banala", nrSolutiiCautate=1, timeOut = 1000000):
    global max_nodes_ida_star, max_nodes_ida_iteration, total_noduri_ida_star
    max_nodes_ida_star=0
    max_nodes_ida_iteration=0
    total_noduri_ida_star=0

    def construieste_drum(gr, nodCurent, limita, nrSolutiiCautate):
        global max_nodes_ida_star, max_nodes_ida_iteration, total_noduri_ida_star
        if nodCurent.f>limita:
            return nrSolutiiCautate, nodCurent.f
        if gr.testeaza_scop(nodCurent) and nodCurent.f ==limita:
            out.write("Solutie: <br>")
            nodCurent.afisDrum(out, time.time()-start_time, max_nodes_ida_star, total_noduri_ida_star, afisCost=True, afisLung=True)
            out.write(str(limita)+"<br>")
            out.write("<br>----------------<br>")
            nrSolutiiCautate-=1
            if nrSolutiiCautate==0:
                out.write("Am gasit toate solutiile cautate.")
                return 0, "gata"
        lSuccesori= gr.genereazaSuccesori(nodCurent)
        total_noduri_ida_star+=len(lSuccesori)
        max_nodes_ida_iteration+=len(lSuccesori)
        max_nodes_ida_star=max(max_nodes_ida_star, max_nodes_ida_iteration)
        minim = float('inf')
        for s in lSuccesori:
            nrSolutiiCautate, rez = construieste_drum(gr, s, limita, nrSolutiiCautate)
            if rez == "gata":
                return 0, "gata"
            if rez < minim:
                minim = rez
        return nrSolutiiCautate, minim

    initialize_file(out)
    gr.start = refactor(gr.start)
    nodStart = NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))
    total_noduri_ida_star=1
    limita = nodStart.f
    start_time = time.time()
    now = time.time()
    while now-start_time < timeOut:
        max_nodes_ida_iteration=0
        nrSolutiiCautate, rez = construieste_drum(gr, nodStart, limita, nrSolutiiCautate)
        if rez=="gata":
            break
        if rez == float('inf'):
            out.write("Nu mai exista solutii!")
            break
        limita = rez
        now = time.time()
    if now-start_time>=timeOut:
        out.write("Timeout.<br>")
        print("Timeout")
    close_file(out)



if len(sys.argv) != 5:
    print('Usage: python m.py path_to_input_directory path_to_output_directory nr_sol timeout')
    print('Ex: python m.py Inputs Outputs 5 6')
    exit()

functii = [a_star, a_star_optimizat, ida_star]
euristici = ["euristica banala", "euristica1", "euristica2", "neadmisibila"]


dir_input = sys.argv[1]
dir_output = sys.argv[2]
nrSol = int(sys.argv[3])
timeOut = int(sys.argv[4])

if not os.path.exists(sys.argv[2]):
    os.mkdir(sys.argv[2])


for numeFisier in os.listdir(dir_input):
    # if g.valid:  # Daca sunt ok datele de intrare
    print(f"Apelez uniform_cost pentru {numeFisier}")
    numeFisierOutputLocal = "uniform_cost" + "_" + numeFisier[:-3] + ".html"
    stream = open(sys.argv[2] + "/" + numeFisierOutputLocal, "w")
    gr = Graph(dir_input + '/' + numeFisier, stream)
    uniform_cost(stream, gr, nrSol, timeOut)
    stream.close()
    for functie in functii:
        for euristica in euristici:
            print(f"Apelez {functie.__name__} cu {euristica} pentru {numeFisier}")
            numeFisierOutputLocal = functie.__name__ + "_" + euristica + "_" + numeFisier[:-3] + ".html"
            stream = open(sys.argv[2] + "/" + numeFisierOutputLocal, "w")
            functie(stream, gr, euristica, nrSol, timeOut)
            stream.close()
