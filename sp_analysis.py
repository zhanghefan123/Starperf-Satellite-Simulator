import sp_cal_bandwidth
import sp_cal_betweenness
import sp_cal_coverage
import sp_cal_dij_delay


def get_parameters(path):
    """Get the parameters of mega-constellations 获取巨型星座的相关参数
    :param path: str, configuration file path of mega-constellations path是文件相关的参数
    :return parameter: two-dimensional list about parameter of constellations 返回值是关于星座的一个二维列表
    第一个参数为: 星座名称
    第二个参数为：星座卫星个数
    第三个参数为：星座周期
    第四个参数为：卫星俯角 the term of depression denotes the angle from the horizontal downward to an object
    第五个参数为：地面站仰角 the term of elevation denotes the angle from horizontal upward to an object
    第六个参数为：延迟阈值
    """
    f = open(path, "r")
    line = f.readline()
    line = line.strip('\n')
    values = line.split(',')
    parameter = [[0 for i in range(len(values))] for i in range(6)] # 在这里生成了一个包含6个一维列表，每个一维列表长度为len(values)的二维列表
    row = 0
    # 循环进行行的获取
    # -------------------------------------------------------------------
    while line:
        line = line.strip('\n')
        values = line.split(',') # 将一行之中的每个元素抽离出来放到values之中。
        for i in range(len(values)):
            # 将除了第一行以外的所有行理解为浮点数
            # ------------------------------------------------------------
            if row != 0:
                parameter[row][i] = (float)(values[i])
            else:
                parameter[row][i] = values[i]
            # ------------------------------------------------------------
        row += 1
        line = f.readline()
    # --------------------------------------------------------------------
    f.close()
    return parameter

def perform_benchmark():
    """
    进行基准测试
    """
    path = 'etc\parameter.txt' # 路径不对做出了修改
    constellation_parameter = get_parameters(path) # 获取参数
    sp_cal_dij_delay.dij_delay(constellation_parameter, error_rate=0, dT=1) # 计算延迟
    sp_cal_bandwidth.bandwidth(constellation_parameter,dT=60)
    sp_cal_coverage.coverage(constellation_parameter)
    sp_cal_betweenness.betweenness(constellation_parameter)

if __name__ == '__main__':
    perform_benchmark()
