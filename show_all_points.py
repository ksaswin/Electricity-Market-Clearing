from tabulate import tabulate


def show_marked_points(x, y, header_values = ['x-coordinate', 'y-coordinate']):
    x_and_y = []
    for index, x_value in enumerate(x):
        x_and_y.append([x_value, y[index]])

    print(tabulate([*x_and_y], headers=header_values, tablefmt='orgtbl'))
