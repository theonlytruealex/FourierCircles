from svgpathtools import svg2paths
import numpy as np

def interpolate_points(path, point_count, path_length):
    points = []
    for i in range(point_count):
        distance = (i / (point_count - 1)) * path_length
        point = path.point(distance / path_length)
        points.append(point)
    return points

def svg_points(svg_file, point_count):
    if point_count % 2 == 0:
        print("point count must be odd for simpson integration")
    paths, attributes = svg2paths(svg_file)
    all_points = []
    draw_length = sum(p.length() for p in paths)

    # it works best with one path, multiple will be appended to eachother
    for path, _ in zip(paths, attributes):
        path_length = path.length()
        point_count_path = int((path_length / draw_length) * point_count)
        if point_count_path > 0:
            points_outer = interpolate_points(path, point_count_path, path_length)
            all_points.extend(points_outer)
    return all_points

def scale_array(points, screen_width, screen_height):
    min_x = min(point.real for point in points)
    max_x = max(point.real for point in points)
    min_y = min(point.imag for point in points)
    max_y = max(point.imag for point in points)
    width = max_x - min_x
    height = max_y - min_y

    # 0.8 is here to let the image have a bit of room around it
    scale_x = screen_width / width * 0.8
    scale_y = screen_height / height * 0.8
    scale = min(scale_x, scale_y)
    offset_x = (screen_width - width * scale) / 2
    offset_y = (screen_height - height * scale) / 2

    # we turn the complex numbers into the array used before
    scaled_points = np.zeros([2, len(points)])
    for i in range(len(points)):
        scaled_points[0][i] = (points[i].real - min_x) * scale + offset_x
        scaled_points[1][i] = (points[i].imag - min_y) * scale + offset_y
    return scaled_points

def get_point_array(point_count = 10001, svg_file = './images/sol_key.svg',\
                    screen_width = 1080, screen_height = 100):
    
    # it is easier to work with complex numbers at first
    points_complex = svg_points(svg_file, point_count)
    points = scale_array(points_complex, screen_width, screen_height)
    return points

