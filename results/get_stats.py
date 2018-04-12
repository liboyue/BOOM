import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import json
import sys
import os
import re

def threeD_plot(stats, ind1, ind2):
    dic = {"alphas": "alpha",
           "wcs": "Max Length (tokens)",
           "ks": "K"
    }
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(np.array(stats[ind1]), np.array(stats[ind2]), np.array(stats["scores"]))
    ax.set_xlabel(dic[ind1])
    ax.set_ylabel(dic[ind2])
    ax.set_zlabel("Average Rouge")
    plt.show()

def plot_hist(stats):
    plt.hist(stats["scores"], bins=100)
    plt.xlabel("Average Rouge")
    plt.show()

def scatter_plot(stats, ind_var):
    dic = {"alphas": "alpha",
           "wcs": "Max Length (tokens)",
           "ks": "K"
    }
    plt.scatter(stats[ind_var], stats["scores"])
    plt.xlabel(dic[ind_var])
    plt.ylabel("Average Rouge")
    plt.show()

def parse_params(file_name):
    rgx = re.compile("\{(.+?)\}")
    alpha, k, wc = None, None, None
    for m in rgx.findall(file_name):
        try:
            name, val = m.split(":")
            if name == '"alpha"':
                alpha = float(val)
            elif name == '"k"':
                k = float(val)
            elif name == '"word_limit"':
                wc = int(val)
            else:
                pass
        except:
            pass
    return alpha, k, wc

def get_score(direc, file_name):
    js = json.load(open(direc + file_name))
    return js["average"]

if len(sys.argv) != 2:
    print("ERROR: Must pass (only) path to file dump as argument.")
    sys.exit()

PATH = sys.argv[1]
alphas = []
ks = []
wcs = []
scores = []
for fi in os.listdir(PATH):
    if "rouge" in fi:
        alpha, k, wc = parse_params(fi)
        score = get_score(PATH, fi)
        alphas.append(alpha)
        ks.append(k)
        wcs.append(wc)
        scores.append(score)

stats = {"alphas": alphas, "ks": ks, "wcs": wcs, "scores": scores}

#plot_hist(stats)
scatter_plot(stats, "ks")
#threeD_plot(stats, "ks", "wcs")
