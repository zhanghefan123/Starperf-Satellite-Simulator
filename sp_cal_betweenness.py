import networkx as nx
import scipy.io as scio


def betweenness(parameter):
    """Calculate the betweenness of mega-constellations 进行巨型星座的介值中心性的计算
    :param parameter: two-dimensional list about parameter of constellations 输入的参数是二维列表
    """
    # 首先进行星座个数的获取
    constellation_num = len(parameter[0])
    # 进行每一个星座的遍历
    for constellation_index in range(constellation_num):
        # 获取星座名称
        constellation_name = parameter[0][constellation_index]
        # 获取卫星的个数
        satellite_num = int(parameter[1][constellation_index])
        # 进行一个空图的创建
        G = nx.Graph()
        # load matlab 之中的内容
        path = 'matlab_code\\' + constellation_name + '\\delay\\1.mat'
        data = scio.loadmat(path)
        delay = data['delay']
        # 进行图中的节点的添加
        G.add_nodes_from(range(satellite_num))
        # 进行每个节点的遍历
        for i in range(satellite_num):
            # 遍历除了本节点外的其余的节点
            for j in range(i + 1, satellite_num):
                # 如果延迟大于0，则进行节点间边的添加
                if delay[i][j] > 0:
                    G.add_edge(i, j)
        # 直接通过networkx计算介值中心性
        score = nx.betweenness_centrality(G)
        bet = []
        for item in score.keys():
            bet.append(score[item])
        # 将每隔节点的介值中心性值都存储在bet之中并打印
        print(bet)

