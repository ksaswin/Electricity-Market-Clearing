from tabulate import tabulate

HEADERS = ['x-coordinate', 'y-coordinate']

def show_marked_points(x, y):
    x_and_y = []
    for index, x_value in enumerate(x):
        x_and_y.append([x_value, y[index]])

    print(tabulate([*x_and_y], headers=HEADERS, tablefmt='orgtbl'))
