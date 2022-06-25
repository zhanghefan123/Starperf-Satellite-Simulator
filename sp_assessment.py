# -*- coding: UTF-8 -*-
import errno
import h3 # 进行uber的h3的导入
import os
from geopy import distance

import sp_topology
import sp_utils

light_of_speed_m_s = 299792458;  # m / s
attenuation_factor = 2 / 3;  # light travels in 2/3 speed of light in free-space 光在
light_of_speed_km_ms = light_of_speed_m_s / (10 ** 6) # 千米/毫秒
constellation_name = 'StarLink';


# constellation_name = 'OneWeb';


class lla_slot_cache_entry:
    def __init__(self):
        self.name = "";
        self.lines = "";


# reference: https://geopy.readthedocs.io/en/stable/#module-geopy.distance
def calculate_distance():
    # prepare the results dict
    distance_results = {}
    rtt_results = {}

    # prepare the data cache
    # 找到星座名称小写/slots/ 这个目录下面的所有时隙csv文件
    lla_location_file_lists_by_slots = sp_utils.sp_walkFile((constellation_name.lower() + "/slots/"))
    lla_data_cache = {}
    # load all lla data in memory cache.
    # 遍历所有的lla文件
    for lla_filename in lla_location_file_lists_by_slots:
        f = open(lla_filename, "r+")
        # 读取其中所有的行
        lines = f.readlines()
        f.close();
        # 将信息缓存到lla_data_cache之中，其中包含所有行和名称
        lla_data_cache[lla_filename] = lla_slot_cache_entry();
        lla_data_cache[lla_filename].name = lla_filename;
        lla_data_cache[lla_filename].lines = lines;

    # print(observation_point);
    # 打印地面站的长度
    print(len(sp_topology.ground_station_points));
    print("Start to calculate distance for each observation point.");

    # 遍历所有的地面观测站
    for ob in sp_topology.ground_station_points:
        # for each observation point, find the nearest satellite and distance in every slots
        # 对于每一个观测站，我们需要找到在每隔时隙内距离最近的卫星
        src_location = (ob.latitude, ob.longitude);
        distance_results[ob.id] = [];
        rtt_results[ob.id] = [];
        # save the results for the current observation point into file
        # 将观察点观察到的结果存入文件之中
        ob_result_filename = constellation_name.lower() + "/observation_point/" + str(ob.id) + ".csv";
        sp_utils.sp_create_file_if_not_exit(ob_result_filename);
        ob_result_csvfile = open(ob_result_filename, "w+");
        print("Calculating distance from %s." % ob.id);
        lla_location_file_lists_by_slots.sort()
        for lla_filename in lla_location_file_lists_by_slots:
            # f = open(lla_filename, "r+")
            # lines = f.readlines()
            # f.close();
            # 从一开始的缓存之中进行lla信息的读取
            lines = lla_data_cache[lla_filename].lines;
            # 将观测距离设置为正无限大
            ob_distance = float('inf')
            # 开始搜索距离自己最近的卫星
            print("Searching the nearest satellite in %s ..." % lla_filename)
            # 读取lla file 之中的每一行的信息;
            for lla_locations_in_current_slot in lines:
                lla = lla_locations_in_current_slot.split(',');
                # 当前时间
                daytime = lla[1]
                # 当前高度;
                altitude = lla[4]
                altitude = 550;  # negative value observed in TLE data, should we fix it to 550km?
                # lla[2,3] 保存的是经纬度
                dst_location = (lla[2], lla[3]);
                # 获取从source(地面观测站)到destination(卫星)的距离
                # distance.distance计算的是测地距离,即为球体表面两点间最短距离
                distance_sample = distance.distance(src_location, dst_location).km
                distance_sample = distance_sample + float(altitude)
                # ob_distance 保存的是当前的最短距离
                if (distance_sample <= ob_distance):
                    ob_distance = distance_sample;
            # 进行RTT的估算 = 2 * (最短观测距离/(2/3光速))
            estimated_RTT_ms = 2 * (ob_distance / light_of_speed_km_ms);
            distance_results[ob.id].append(ob_distance);
            rtt_results[ob.id].append(estimated_RTT_ms);
            print("Closest distance: %s km, estimated latency: %s ms." % (str(ob_distance), str(estimated_RTT_ms)))
            # record = str(ob.id) + "," + str(daytime) + "," + str(ob_distance) + "," + str(estimated_RTT_ms) + "\n"
            record = str(estimated_RTT_ms) + "\n"
            ob_result_csvfile.write(record)
        # save results to csv files
        ob_result_csvfile.flush()
        ob_result_csvfile.close()

    return distance


if __name__ == '__main__':
    print("StarPerf performance assessment.")
