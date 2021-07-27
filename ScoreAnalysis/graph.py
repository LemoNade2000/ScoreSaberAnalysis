import os,sys,inspect
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'
from typing import AnyStr
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
import BaseClasses
import numpy as np
import networkx as nx
import json
import ntpath
from matplotlib import pyplot as plt

directory = r"E:\ABC\ScoreSaberAnalysis\JsonData\CorrMaps"

def graphGenerator():
    graph = nx.DiGraph()
    for filenames in os.listdir(directory):
        map = ntpath.basename(filenames)[:-5]
        graph.add_node(map)
        
    for filenames in os.listdir(directory):
        edges = []
        mapfile = open(directory + "\\" + filenames)
        json_data = json.load(mapfile)
        start = json_data['hash'] + json_data['diff']
        for i in range(0, 10):
            try:
                end = json_data['correlatedMaps'][i][0]
                corrRec = 1 / json_data['correlatedMaps'][i][1]
                edge = (start, end, corrRec)
                edges.append(edge)
            except:
                break
        graph.add_weighted_edges_from(edges)

    nx.write_gexf(graph, "Graph.gexf")
