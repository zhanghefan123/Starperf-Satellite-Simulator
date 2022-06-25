import sp_analysis

def test_get_parameters():
  """
  进行sp_analysis_test.py之中的get_parameters的测试
  
  parameters.txt之中的内容如下:
  
  StarLink,OneWeb,polar_Telesat,inclined_Telesat
  1584,720,72,50
  5731,6557,6298,6557
  44.85,28.8596,54.3122,52.2558
  40,55,20,20
  2.71,4.71,7.07,8.19
  
  输出结果如下:
  
  第一行被解析为字符串,其余行被解析为浮点数
  
  [
    ['StarLink', 'OneWeb', 'polar_Telesat', 'inclined_Telesat'], 
    [1584.0, 720.0, 72.0, 50.0], 
    [5731.0, 6557.0, 6298.0, 6557.0], 
    [44.85, 28.8596, 54.3122, 52.2558], 
    [40.0, 55.0, 20.0, 20.0], 
    [2.71, 4.71, 7.07, 8.19]
  ]
  
  """
  path = "test\sp_analysis_test\parameters.txt"
  result = sp_analysis.get_parameters(path)
  print(result)

if __name__ == "__main__":
  test_get_parameters()


