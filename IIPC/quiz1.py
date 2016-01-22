def cal(num):
    return -5 * num ** 5 + 69 * num ** 2 - 47

# for x in range(4):
#     print cal(x)

def future_value(present_value, annual_rate, periods_per_year, years):
    rate_per_period = annual_rate / periods_per_year
    periods = periods_per_year * years
    return present_value * pow((1 + rate_per_period), periods)


# print "$1000 at 2% compounded daily for 3 years yields $", future_value(500, .04, 10, 10)
import math
def area(n ,s):
    return (1 / 4.0) * n * s ** 2 / math.tan(math.pi / n)

# print area(7, 3)

def project_to_distance(point_x, point_y, distance):
    dist_to_origin = math.sqrt(point_x ** 2 + point_y ** 2)
    scale = distance / dist_to_origin
    print point_x * scale, point_y * scale

project_to_distance(2, 7, 4)
