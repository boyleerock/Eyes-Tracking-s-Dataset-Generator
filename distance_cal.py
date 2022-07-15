import math

def cal(point_a, point_b):
    x = point_a[0] - point_b[0]
    y = point_a[1] - point_b[1]
    dis = math.sqrt((x**2)+(y**2))
    # print(dis)
    return dis

# pa = (0, 0)
# pb = (3, 4)
# distance = cal(pa, pb)
# print(distance)