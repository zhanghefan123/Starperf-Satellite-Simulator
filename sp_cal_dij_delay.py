import networkx as nx
import numpy
import random
import scipy.io as scio


def dij_delay(parameter,error_rate, dT):
    """calculate the area-to-area latency 进行区域i到区域j的延迟的计算
    :param parameter: two-dimensional list about parameter of constellations 星座参数的二维列表
    :param error_rate: float, probability of satellite failure 错误率-卫星发生失败的概率
    :param dT: int, accuracy of the results 步长,应该是指的是分辨率
    """
    constellation_num = len(parameter[0])
    for constellation_index in range(constellation_num):
        constellation_name = parameter[0][constellation_index]
        satellite_num = int(parameter[1][constellation_index])
        cycle = int(parameter[2][constellation_index])
        bound = parameter[5][constellation_index]
        city_num = 4
        dl = [[0 for i in range(int((cycle - 1)/dT) + 1)] for i in range(6)]
        error = [0 for i in range(6)]
        for time in range(1, cycle + 1, dT):
            print(time)
            G = nx.Graph()
            edge = []
            path = 'matlab_code\\' + constellation_name + '\\delay\\' + str(time) + '.mat'
            data = scio.loadmat(path)
            delay = data['delay']
            G.add_nodes_from(range(satellite_num + city_num))
            for i in range(satellite_num):
                for j in range(i + 1, satellite_num):
                    if delay[i][j] > 0:
                        edge.append((i, j, delay[i][j]))
                for j in range(satellite_num, satellite_num + city_num):
                    if delay[i][j] < bound:
                        edge.append((i, j, delay[i][j]))
            G.add_weighted_edges_from(edge)
            if error_rate > 0:
                for i in range(satellite_num):
                    destroy = random.randint(1,int(100 / error_rate))
                    if destroy == 1:
                        G.remove_node(i)
            count = 0
            for i in range(satellite_num, satellite_num + city_num - 1):        #city to city
                for j in range(i+1, satellite_num + city_num):
                    if nx.has_path(G, source=i, target=j):
                        dl[count][int((time - 1) / dT)] = nx.dijkstra_path_length(G, source=i, target=j)
                    else:       #GSL is broken down
                        error[count] += 1
                        dl[count][(time - 1) / dT] = 0.
                    count += 1
        numpy.savetxt(constellation_name + '.csv', dl, fmt='%f')



