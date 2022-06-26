import random
if __name__ == "__main__":
  satellite_num = 3
  for i in range(satellite_num):
      for j in range(i + 1, satellite_num):
        print(i,j)
  error_rate = 50
  destroy = random.randint(1,int(100 / error_rate))
  print(destroy)