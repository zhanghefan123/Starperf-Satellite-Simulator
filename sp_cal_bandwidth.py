import copy
import scipy.io as scio
import networkx as nx


def bandwidth(parameter, dT):
    """Calculate the area-to-area achievable throughput 计算区域到区域可达的吞吐量
    :param parameter: two-dimensional list about parameter of constellations 二维列表参数
    :param dT: int, accuracy of the results 步长
    """
    # 星座的个数
    constellation_num = len(parameter[0])
    # 遍历所有的星座
    for constellation_index in range(constellation_num):
        # 获取星座名称
        constellation_name = parameter[0][constellation_index]
        # 获取卫星数量
        satellite_num = int(parameter[1][constellation_index])
        # 获取卫星周期
        cycle = int(parameter[2][constellation_index])
        # 获取延迟阈值
        bound = parameter[5][constellation_index]
        # 城市数量
        city_num = 4
        # labellist = ['BJ-NY','BJ-LD','BJ-SN','NY-LD','NY-SN','LD-SN']
        # 每一对节点都有一系列快照
        path_num = [[0 for i in range((cycle - 1) / dT + 1)] for i in range(6)]
        # 遍历每一个快照
        for time in range(1, cycle + 1, dT):
            edge = [] # 创建边集
            G = nx.Graph() # 创建图
            path = constellation_name + '\\delay\\' + str(time) + '.mat' # matlab save 的 delay variable
            data = scio.loadmat(path) # 读取mat文件
            delay = data['delay']
            G.add_nodes_from(range(satellite_num + city_num)) # 添加卫星和地面节点
            
            for i in range(satellite_num):
                # 遍历所有的卫星对
                for j in range(i + 1, satellite_num):
                    # 如果delay大于0，则添加边
                    if delay[i][j] > 0:
                        edge.append((i, j, delay[i][j]))
                # 遍历所有的卫星城市对
                for j in range(satellite_num, satellite_num + city_num):
                    if delay[i][j] < bound:
                        edge.append((i, j, delay[i][j]))
            # 向图中添加边集
            G.add_weighted_edges_from(edge)
            count = 0
            # 遍历所有的城市对
            for i in range(satellite_num, satellite_num + city_num - 1):
                for j in range(i + 1, satellite_num + city_num):
                    # 如果从i到j存在路径
                    if nx.has_path(G, source=i, target=j):
                        # 使用dijkstra计算最短路径
                        shortest = nx.dijkstra_path_length(G, source=i, target=j)
                        # 进行图的备份，下面使用备份图而不是原图进行操作
                        tempG = copy.copy(G)
                        # 当现在图之中包含从i到j的路径
                        while nx.has_path(tempG, source=i, target=j):
                            # 当前最短路，如果当前的最短路都大于原先最短路的1.1倍，那么就退出，说明已经找到了所有的低延迟最短路
                            cur_shortet = nx.dijkstra_path_length(tempG, source=i, target=j)
                            if cur_shortet > shortest * 1.1:
                                break
                            path = nx.dijkstra_path(tempG, source=i, target=j)
                            # 低延迟最短路个数进行+1操作
                            path_num[count][(time - 1) / dT] += 1
                            # 移除这一条最短路上的所有边
                            for x in range(1, len(path) - 2):
                                tempG.remove_edge(path[x], path[x + 1])
                    count += 1
        # 接下来进行平均吞吐量的计算
        avg_bandwidth = [0 for i in range(6)]
        for i in range(6):
            sum = 0.
            # 对于每个城市对,遍历所有的snapshots
            for j in range((cycle - 1) / dT + 1):
                sum += (path_num[i][j] * 5) # capacity of ISL is set to 5Gpbs
            if sum == 0:
                avg_bandwidth[i] = -1
            else:
                avg_bandwidth[i] = sum / ((cycle - 1) / dT + 1) # avg_throughput is set to sum / snapshotCount
        print(avg_bandwidth)

