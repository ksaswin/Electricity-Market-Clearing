def check_for_intersection(line1_points, line2_points, eq_x, eq_y):
    min_x = min(line1_points[0][0], line1_points[1][0])
    max_x = max(line1_points[0][0], line1_points[1][0])
    if not (min_x <= eq_x <= max_x):
        return False

    min_x = min(line2_points[0][0], line2_points[1][0])
    max_x = max(line2_points[0][0], line2_points[1][0])
    if not (min_x <= eq_x <= max_x):
        return False
    
    min_y = min(line1_points[0][1], line1_points[1][1])
    max_y = max(line1_points[0][1], line1_points[1][1])
    if not (min_y <= eq_y <= max_y):
        return False
    
    min_y = min(line2_points[0][1], line2_points[1][1])
    max_y = max(line2_points[0][1], line2_points[1][1])
    if not (min_y <= eq_y <= max_y):
        return False

    return True