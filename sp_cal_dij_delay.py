import networkx as nx
import numpy
import random
import scipy.io as scio


def dij_delay(parameter,error_rate, dT):
    """calculate the area-to-area latency 进行区域i到区域j的延迟的计算
    :param parameter: two-dimensional list about parameter of constellations 星座参数的二维列表
    :param error_rate: float, probability of satellite failure 故障率-卫星发生失败的概率
    :param dT: int, accuracy of the results 步长,应该是指每一个时隙的长度
    """
    constellation_num = len(parameter[0]) # 获取星座的个数
    for constellation_index in range(constellation_num): # 遍历每个星座
        constellation_name = parameter[0][constellation_index] # 获取星座名称
        satellite_num = int(parameter[1][constellation_index]) # 获取当前星座卫星个数
        cycle = int(parameter[2][constellation_index]) # 获取当前星座周期
        bound = parameter[5][constellation_index] # 获取延迟阈值
        city_num = 4 # 获取城市个数
        dl = [[0 for i in range(int((cycle - 1)/dT) + 1)] for i in range(6)] # delay数组
        error = [0 for i in range(6)] # 故障率
        for time in range(1, cycle + 1, dT): # 进行每一个时隙的遍历
            print(time) # 打印当前时间
            G = nx.Graph() # 创建图
            edge = [] # 创建边集
            path = 'matlab_code\\' + constellation_name + '\\delay\\' + str(time) + '.mat' # matlab生成的延迟文件
            data = scio.loadmat(path) # 读取.mat文件
            delay = data['delay'] # 获取其中保存的delay变量
            G.add_nodes_from(range(satellite_num + city_num)) # 添加所有卫星节点和所有地面节点
            
            for i in range(satellite_num):
                # 遍历所有的卫星节点对
                for j in range(i + 1, satellite_num):
                    # 如果delay > 0,即在matlab之中建立了这两点间的连接
                    if delay[i][j] > 0:
                        # 那么我们添加这一条这边
                        edge.append((i, j, delay[i][j]))
                # 遍历所有的卫星地面节点对
                for j in range(satellite_num, satellite_num + city_num):
                    if delay[i][j] < bound:
                        edge.append((i, j, delay[i][j]))
            # 将edge放在G图之中
            G.add_weighted_edges_from(edge)
            # 如果故障率大于0
            if error_rate > 0:
                # 遍历所有的卫星节点
                for i in range(satellite_num):
                    # error_rate range from 0 ~ 100
                    destroy = random.randint(1,int(100 / error_rate))
                    # if destroy == 1 remove the node from graph
                    if destroy == 1:
                        G.remove_node(i)
            
            count = 0
            # 遍历所有的城市对，4座城市，总共存在6对
            for i in range(satellite_num, satellite_num + city_num - 1):
                for j in range(i+1, satellite_num + city_num):
                    # 调用nx的has_path进行判断是否存在一条从source到target的路径
                    if nx.has_path(G, source=i, target=j):
                        # 使用nx的dijkstra_path计算从i到j的延迟
                        dl[count][int((time - 1) / dT)] = nx.dijkstra_path_length(G, source=i, target=j)
                    # 如果不存在
                    else:       
                        error[count] += 1
                        dl[count][(time - 1) / dT] = 0.
                    count += 1
        numpy.savetxt(constellation_name + '.csv', dl, fmt='%f')



