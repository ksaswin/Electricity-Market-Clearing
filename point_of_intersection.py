def intersection_coordinates(line1_points, line2_points):
    difference_x = []
    difference_y = []

    difference_x.append(line1_points[0][0] - line1_points[1][0])
    difference_x.append(line2_points[0][0] - line2_points[1][0])

    difference_y.append(line1_points[0][1] - line1_points[1][1])
    difference_y.append(line2_points[0][1] - line2_points[1][1])
    
    def determinant(a, b):
        return a[0] * b[1] - a[1] * b[0]
    
    denominator = determinant(difference_x, difference_y)
    if denominator == 0:        # Denominator 0 means lines donot intersect
        return ['no', 'no']
    
    d = [determinant(*line1_points), determinant(*line2_points)]
    poi_x = determinant(d, difference_x) / denominator
    poi_y = determinant(d, difference_y) / denominator
    
    return [poi_x, poi_y]
