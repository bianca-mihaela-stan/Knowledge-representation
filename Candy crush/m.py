import copy
from heapq import heappush, heapify, heappop
import sys
import os
import time
from NodParcurgere import Node
from Graph import Graph
from helpers import refactor

max_nodes_ucs = 0
max_nodes_a_star = 0
max_nodes_optimized_a_star = 0
max_nodes_ida_star = 0
max_nodes_ida_iteration=0
total_ucs_nodes = 0
total_nodes_a_star = 0
total_nodes_optimized_a_star = 0
total_nodes_ida_star = 0

def initialize_file(out):
    """
    Initializes the html output file.
    """
    out.write("<!DOCTYPE html>\n <html> \n <body> \n\n <p>")

def close_file(out):
    """
        Closes the html output file.
    """
    out.write("\n </p>\n </body> \n </html>")
    out.close()

def uniform_cost(out,  gr,  nr_sol=1, timeout = 60):
    global max_nodes_ucs, total_ucs_nodes
    max_nodes_ucs=0
    total_ucs_nodes=0

    initialize_file(out)
    c =[]
    gr.start = refactor(gr.start)
    heappush(c, Node(gr.start, None, 0, gr.estimate_h(gr.start)))
    max_nodes_ucs =1
    total_ucs_nodes=1
    start_time = time.time()
    now = time.time()
    while len(c)>0 and now-start_time<timeout:
        current_node=heappop(c)
        if gr.test_goal(current_node):
            out.write("Solution: <br>")
            current_node.output_path(out, time.time()-start_time, max_nodes_ucs, total_ucs_nodes, afisCost=True, afisLung=True)
            out.write("<br>----------------<br>")
            nr_sol -= 1
            if nr_sol == 0:
                out.write(".")
                return
        successors = gr.generate_successors(current_node)
        for s in successors:
            heappush(c, s)
        max_nodes_ucs=max(max_nodes_ucs, len(c) + len(successors))
        total_ucs_nodes+=len(successors)
        now = time.time()
        
    if now - start_time >= timeout:
        out.write("Timeout.<br>")
        print("Timeout")
    else:
        out.write("There are no more solutions.<br>")
    close_file(out)


def a_star(out,  gr, heuristic="simple heuristic", nr_sol=1, timeout = 60):
    global max_nodes_a_star, total_nodes_a_star
    max_nodes_a_star=0
    total_nodes_a_star=0

    initialize_file(out)
    c = []
    gr.start = refactor(gr.start)
    heappush(c, Node(gr.start, None, 0, gr.estimate_h(gr.start)))
    max_nodes_a_star=1
    total_nodes_a_star=1
    start_time = time.time()
    now = time.time()
    
    while len(c) > 0 and now-start_time < timeout:
        current_node = heappop(c)

        if gr.test_goal(current_node):
            out.write("Solution: <br>")
            current_node.output_path(out, time.time()-start_time, max_nodes_a_star, total_nodes_a_star, afisCost=True, afisLung=True)
            out.write("<br>----------------<br>")
            nr_sol -= 1
            if nr_sol == 0:
                out.write("Found all solutions we were looking for.<br>")
                return
        successors = gr.generate_successors(current_node, heuristic)
        total_nodes_a_star+=len(successors) + len(c)
        for s in successors:
            heappush(c, s)
        max_nodes_a_star=max(max_nodes_ucs, len(c)+len(successors))
        now = time.time()
        
    if now - start_time >= timeout:
        out.write("Timeout.<br>")
        print("Timeout")
    else:
        out.write("There are no more solutions.<br>")
    close_file(out)


def optimized_a_star(out,  gr, heuristic="simple heuristic", nr_sol=1, timeout = 60):
    global max_nodes_optimized_a_star, total_nodes_optimized_a_star
    max_nodes_optimized_a_star=0
    total_nodes_optimized_a_star=0

    initialize_file(out)
    gr.start = refactor(gr.start)

    startNode = Node(gr.start, None, 0, gr.estimate_h(gr.start))
    c = [startNode]
    heapify(c)
    max_nodes_optimized_a_star=1
    total_nodes_optimized_a_star=1

    closed = []

    start_time = time.time()
    now = time.time()
    while len(c) > 0 and now-start_time< timeout:
        current_node = heappop(c)

        closed.append(current_node)

        if gr.test_goal(current_node):
            out.write("Solution: <br>")
            current_node.output_path(out, time.time()-start_time, max_nodes_optimized_a_star, total_nodes_optimized_a_star, afisCost=True, afisLung=True)
            out.write("<br>----------------<br>")
            nr_sol -= 1
            if nr_sol == 0:
                out.write("Found all solutions we were looking for.<br>")
                return

        successors = gr.generate_successors(current_node, heuristic)
        max_nodes_optimized_a_star=max(max_nodes_optimized_a_star,
                                        len(successors) + len(closed) + len(c))
        total_nodes_optimized_a_star += len(successors)

        for s in successors:
            gasitC = False
            for nodC in c:
                nodC = nodC
                if s.info == nodC.info:
                    gasitC=True
                    if s.f >= nodC.f:
                        successors[:] = [x for x in successors if x!=s]
                    else:
                        c[:] = [x for x in c if x!=nodC]
            if not gasitC:
                for nodC in closed:
                    if s.info == nodC.info:
                        if s.f >= nodC.f:
                            successors[:] = [x for x in successors if x != s]
                        else:
                            closed[:] = [x for x in closed if x != nodC]
            heapify(c)
        for s in successors:
            heappush(c, s)
        now = time.time()

    if now-start_time>=timeout:
        out.write("Timeout.<br>")
        print("Timeout")
    else:
        out.write("There are no more solutions.<br>")
    close_file(out)


def ida_star(out,  gr, heuristic="simple heuristic", nr_sol=1, timeout = 1000000):
    global max_nodes_ida_star, max_nodes_ida_iteration, total_nodes_ida_star
    max_nodes_ida_star=0
    max_nodes_ida_iteration=0
    total_nodes_ida_star=0

    def build_path(gr, current_node, limit, nr_sol):
        global max_nodes_ida_star, max_nodes_ida_iteration, total_nodes_ida_star

        if current_node.f>limit:
            return nr_sol, current_node.f
        if gr.test_goal(current_node) and current_node.f == limit:
            out.write("Solution: <br>")
            current_node.output_path(out, time.time()-start_time, max_nodes_ida_star, total_nodes_ida_star, afisCost=True, afisLung=True)
            out.write(str(limit)+"<br>")
            out.write("<br>----------------<br>")
            nr_sol-=1
            if nr_sol==0:
                out.write("Found all solutions we were looking for.<br>")
                return 0, "done"

        successors = gr.generate_successors(current_node)
        total_nodes_ida_star += len(successors)
        max_nodes_ida_iteration += len(successors)
        max_nodes_ida_star=max(max_nodes_ida_star, max_nodes_ida_iteration)
        minim = float('inf')
        for s in successors:
            nr_sol, rez = build_path(gr, s, limit, nr_sol)
            if rez == "done":
                return 0, "done"
            if rez < minim:
                minim = rez
        return nr_sol, minim

    initialize_file(out)
    gr.start = refactor(gr.start)
    startNode = Node(gr.start, None, 0, gr.estimate_h(gr.start))
    total_nodes_ida_star=1
    limit = startNode.f
    start_time = time.time()
    now = time.time()

    while now-start_time < timeout:
        max_nodes_ida_iteration=0
        nr_sol, rez = build_path(gr, startNode, limit, nr_sol)
        if rez=="done":
            break
        if rez == float('inf'):
            out.write("There are no more solutions.")
            break
        limit = rez
        now = time.time()

    if now-start_time>=timeout:
        out.write("Timeout.<br>")
        print("Timeout")
    close_file(out)



if len(sys.argv) != 5:
    print('Usage: python m.py path_to_input_directory path_to_output_directory nr_sol timeout')
    print('Ex: python m.py Inputs Outputs 5 6')
    exit()

algorithms = [a_star, optimized_a_star, ida_star]
euristici = ["simple heuristic", "first heuristic", "second heuristic", "invalid"]


dir_input = sys.argv[1]
dir_output = sys.argv[2]
nr_sol = int(sys.argv[3])
timeout = int(sys.argv[4])

if not os.path.exists(sys.argv[2]):
    os.mkdir(sys.argv[2])


for file_name in os.listdir(dir_input):
    # if g.valid:  # Daca sunt ok datele de intrare
    print(f"Calling uniform_cost for {file_name}")
    output_file = "uniform_cost" + "_" + file_name[:-3] + ".html"
    stream = open(sys.argv[2] + "/" + output_file, "w")
    gr = Graph(dir_input + '/' + file_name, stream)
    uniform_cost(stream, gr, nr_sol, timeout)
    stream.close()
    for algorithm in algorithms:
        for heuristic in euristici:
            print(f"Calling {algorithm.__name__} with {heuristic} for {file_name}")
            output_file = algorithm.__name__ + "_" + heuristic + "_" + file_name[:-3] + ".html"
            stream = open(sys.argv[2] + "/" + output_file, "w")
            algorithm(stream, gr, heuristic, nr_sol, timeout)
            stream.close()
