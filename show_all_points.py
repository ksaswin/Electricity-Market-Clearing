from tabulate import tabulate

HEADERS = ['x-coordinate', 'y-coordinate']

def show_marked_points(x, y):
    x_and_y = []
    for index, x_value in enumerate(x):
        x_and_y.append([x_value, y[index]])
    # x_list = [f'{float(value):.2f}' for value in x]
    # y_list = [f'{float(value):.2f}' for value in y]

    # print(tabulate([x_list, y_list], headers=HEADERS, tablefmt='orgtbl'))
    print(tabulate([*x_and_y], headers=HEADERS, tablefmt='orgtbl'))


# print(tabulate([['Alice', 24], ['Bob', 19]], headers=['Name', 'Age'], tablefmt='orgtbl'))