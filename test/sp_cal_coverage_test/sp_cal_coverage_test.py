import pandas as pd
if __name__ == "__main__":
  constellation_num = 3
  satellite_in_latitude = [[0 for i in range(18)] for i in range(constellation_num)]
  satellite_in_longitude = [[0 for i in range(36)] for i in range(constellation_num)]
  satellite_in_latitude = pd.DataFrame(satellite_in_latitude)
  satellite_in_longitude = pd.DataFrame(satellite_in_longitude)
  print(satellite_in_latitude.shape)
  print(satellite_in_longitude.shape)