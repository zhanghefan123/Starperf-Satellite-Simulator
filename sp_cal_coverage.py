import math
import matplotlib.pyplot as plt
import numpy
import scipy.io as scio
import xlrd


def coverage(parameter):
    """Analysis the coverage capacity of each constellation 分析每个星座的覆盖范围
    :param parameter: two-dimensional list about parameter of constellations 星座参数
    """
    constellation_num = len(parameter[0]) # 星座个数
    constellation_name = parameter[0] # 星座名称
    satellite_num = [int(x) for x in parameter[1]] # 星座卫星数量
    cycle = [int(x) for x in parameter[2]] # 星座周期
    depression = parameter[3] # 卫星俯角
    elevation = parameter[4] # 地面站仰角
    central_angle = [0 for i in range(constellation_num)] # 中心角度
    for i in range(constellation_num):
        # central_angle[i] = 180 - 90 - elevation[i]
        central_angle[i] = 180 - 2 * (depression[i] + elevation[i])
    # 维度10度一等分，经度10度一等分。
    satellite_in_latitude = [[0 for i in range(18)] for i in range(constellation_num)]
    satellite_in_longitude = [[0 for i in range(36)] for i in range(constellation_num)]
    # 进行每一个星座的遍历
    for constellation_index in range(constellation_num):
        path = constellation_name[constellation_index] + '\\position.mat'
        # 读取matlab所产生的.mat文件
        data = scio.loadmat(path)
        position = data['position']
        # 遍历每一颗卫星
        for satellite_no in range(satellite_num[constellation_index]):
            # 遍历周期之中的每一秒
            for time in range(cycle[constellation_index]):
                # 获取每一颗卫星在此时刻中的纬度和经度
                latitude = position[satellite_no][0][0][time]
                longitude = position[satellite_no][0][1][time]
                # 卫星覆盖区域的下界
                latitude_lower_boundary = int(math.floor((latitude - central_angle[constellation_index] / 2) / 10))
                # 卫星覆盖区域的上界
                latitude_upper_boundary = int(math.floor((latitude + central_angle[constellation_index] / 2) / 10))
                # 总共纬度上划分为了18个区域   -9 -8 -7 -6 -5 -4 -3 -2 -1 0 1 2 3 4 5 6 7 8 
                # 由于是下取整,所以可能会出现
                if latitude_lower_boundary < -9:
                    latitude_lower_boundary = -9
                if latitude_upper_boundary > 8:
                    latitude_upper_boundary = 8
                # 将卫星所覆盖的区域中所能连接到的卫星数量+1
                for k in range(latitude_lower_boundary, latitude_upper_boundary + 1):
                    # 由于k可能为负数，但是索引不能为负数，所以+9，将其全部变为正数
                    satellite_in_latitude[constellation_index][k + 9] += 1
                longitude_lower_boundary = int(math.floor((longitude - central_angle[constellation_index] / 2) / 10))
                longitude_upper_boundary = int(math.floor((longitude + central_angle[constellation_index] / 2) / 10))
                if longitude_lower_boundary < -18:
                    longitude_lower_boundary = int(
                        math.floor((180 - (-180 - longitude + central_angle[constellation_index] / 2)) / 10))
                if longitude_upper_boundary > 17:
                    longitude_upper_boundary = int(
                        math.floor((-180 + longitude + central_angle[constellation_index] / 2 - 180) / 10))
                if longitude_lower_boundary > 0 and longitude_upper_boundary < 0:
                    for k in range(longitude_lower_boundary, 18):
                        satellite_in_longitude[constellation_index][k + 18] += 1
                    for k in range(-18, longitude_upper_boundary + 1):
                        satellite_in_longitude[constellation_index][k + 18] += 1
                else:
                    for k in range(longitude_lower_boundary, longitude_upper_boundary + 1):
                        satellite_in_longitude[constellation_index][k + 18] += 1
    print(satellite_in_latitude)
    print(satellite_in_longitude)
    
    for constellation_index in range(constellation_num):
        satellite_in_latitude[constellation_index] = [x / float(cycle[constellation_index]) for x in
                                                      satellite_in_latitude[constellation_index]]
        satellite_in_longitude[constellation_index] = [x / float(cycle[constellation_index]) for x in
                                                       satellite_in_longitude[constellation_index]]

    numpy.savetxt('lat.csv', satellite_in_latitude, fmt='%f')
    numpy.savetxt('long.csv', satellite_in_longitude, fmt='%f')

    # 使用操作excel的工具打开我们的随纬度变化的全球人口分布
    data = xlrd.open_workbook('global_population.xlsx')
    # 打开sheet 0,其中就是纬度对人口的映射
    table = data.sheets()[0]
    # 获取第一列纬度
    latitude = table.col_values(0)[1::]
    # 获取第二列人口
    population = table.col_values(1)[1::]
    # 同样将纬度每隔10度进行划分，成为18个格
    population_in_latitude_zone = [0 for i in range(18)]
    # 将人口进行分箱处理
    for i in range(len(latitude)):
        population_in_latitude_zone[int(math.floor(latitude[i] / 10)) + 9] += population[i]
    satellite_for_person = [[0 for i in range(18)] for i in range(constellation_num)]

    for constellation_index in range(constellation_num):
        for i in range(18):
            if population_in_latitude_zone[i] != 0:
                satellite_for_person[constellation_index][i] = satellite_in_latitude[constellation_index][i] / \
                                                               population_in_latitude_zone[i]
    numpy.savetxt('sat_per_million_lat.csv', satellite_for_person, fmt='%f')

    # 获取sheet 1，其中包含的是经度对人口的映射
    table = data.sheets()[1]
    longitude = table.col_values(0)[1::]
    population = table.col_values(1)[1::]
    population_in_longitude_zone = [0 for i in range(36)]
    for i in range(len(longitude)):
        population_in_longitude_zone[int(math.floor(longitude[i] / 10)) + 18] += population[i]
    satellite_for_person = [[0 for i in range(36)] for i in range(constellation_num)]

    for constellation_index in range(constellation_num):
        for i in range(36):
            if population_in_longitude_zone[i] != 0:
                satellite_for_person[constellation_index][i] = satellite_in_longitude[constellation_index][i] / \
                                                               population_in_longitude_zone[i]
    numpy.savetxt('sat_per_million_long.csv', satellite_for_person, fmt='%f')
