from sympy import symbols
from sympy.parsing.sympy_parser import parse_expr
from sympy import diff
import matplotlib.pyplot as plt
import math

import lines_intersection_check as intersect_checker
import point_of_intersection as poi
import show_all_points as print_points

import subprocess
import platform
import os
import sys


PLOT_PAUSE_TIME = 1
x = symbols('x')
INFINITY = 1/x.subs(x, 0)
USER = platform.system()
def clr_screen():
    if USER == 'Linux':
        subprocess.call('clear')
    elif USER == 'Windows':
        r = os.system('cls')


def check_inf(num):             # An infinite value is not possible
    if num == INFINITY:
        print('Infinite value found! Terminating program.')
        sys.exit()


def find_line_intercept(x1, x2, y1, y2, y):
    if y2 == y1:
        return x2
    x = ((y-y1)*((x2-x1)/(y2-y1))) + x1
    return x


def main():
    plants = int(input('Enter the number of plants: '))

    fuel_cost_funcs = []
    PLimits = []
    incr_fuel_cost_funcs = []           # Incremental fuel cost functions
    P_max_value = 0

    print('\nEnter the Generator Cost Functions below.')
    print('Only use x as the variable!')
    print('Please enter all power limits in MW')
    for i in range(plants):
        c = input(f'\n    C{i+1} = ')
        c = parse_expr(c)
        fuel_cost_funcs.append(c)
        incr_fuel_cost_funcs.append(diff(c))
        print(f'  Enter Pmin & Pmax for P{i+1}')
        Pmin = float(input('    Pmin = '))
        Pmax = float(input('    Pmax = '))
        PLimits.append([Pmin, Pmax])
        if Pmax > P_max_value:
            P_max_value = Pmax

    demand_cost_funcs = []
    DLimits = []
    incr_load_cost_funcs = []          # Incremental load cost functions

    loads = int(input('\nEnter the number of loads: '))

    print('\nEnter the Load Cost Functions below.')
    print('Only use x as the variable')
    print('Please enter all power limits in MW')
    for i in range(loads):
        d = input(f'\n    D{i+1} = ')
        d = parse_expr(d)
        demand_cost_funcs.append(d)
        incr_load_cost_funcs.append(diff(d))
        print(f'  Enter the Lmin & Lmax for L{i+1}')
        Lmin = float(input('    Lmin = '))
        Lmax = float(input('    Lmax = '))
        DLimits.append([Lmin, Lmax])
    
    clr_screen()
    # print('Inputs provided')                  # Printing the inputs
    print('\nGenerator Cost Functions:')
    for i in range(plants):
        plant = f'P{i+1}'
        print(f"\n    C{i+1} = {str(fuel_cost_funcs[i]).replace('x', plant)}", end='  ;  ')
        print(f"{PLimits[i][0]:.1f} <= {plant} <= {PLimits[i][1]:.1f}")
        print(f"    dC{i+1}/d{plant} = {str(incr_fuel_cost_funcs[i]).replace('x', plant)}")
    print('\nLoad Cost Functions:')
    for i in range(loads):
        load = f'L{i+1}'
        print(f"\n    D{i+1} = {str(demand_cost_funcs[i]).replace('x', load)}", end='  ;  ')
        print(f"{DLimits[i][0]:.1f} <= {plant} <= {DLimits[i][1]:.1f}")
        print(f"    dD{i+1}/d{load} = {str(incr_load_cost_funcs[i]).replace('x', load)}")

    x_values = {'fuel': [], 'demand': []}
    y_values = {'fuel': [], 'demand': []}
    max_cost = 0

    # Finding data points for plotting the Incremental Fuel Costs for each plant
    for i in range(plants):
        x_values['fuel'].append([])
        y_values['fuel'].append([])

        x_values['fuel'][i].append(PLimits[i][0])          # For initial x value, y is zero
        x_values['fuel'][i].append(PLimits[i][0])
        x_values['fuel'][i].append(PLimits[i][1])
        x_values['fuel'][i].append(PLimits[i][1])          # For final x value, y is MAX $/MWh

        y_values['fuel'][i].append(0)

        try:
            cost = incr_fuel_cost_funcs[i].subs(x, x_values['fuel'][i][0])
        except AttributeError:
            cost = incr_fuel_cost_funcs[i]
        check_inf(cost)
        if cost > max_cost:
            max_cost = cost
        y_values['fuel'][i].append(cost)

        try:
            cost = incr_fuel_cost_funcs[i].subs(x, x_values['fuel'][i][2])
        except AttributeError:
            cost = incr_fuel_cost_funcs[i]
        check_inf(cost)
        if cost > max_cost:
            max_cost = cost
        y_values['fuel'][i].append(cost)
    
    # Finding data points for plotting the Incremental Load costs for each load
    for i in range(loads):
        x_values['demand'].append([])
        y_values['demand'].append([])
        
        x_values['demand'][i].append(DLimits[i][0])
        x_values['demand'][i].append(DLimits[i][1])
        x_values['demand'][i].append(DLimits[i][1])

        try:
            cost = incr_load_cost_funcs[i].subs(x, x_values['demand'][i][0])
        except AttributeError:
            cost = incr_load_cost_funcs[i]
        check_inf(cost)
        if cost > max_cost:
            max_cost = cost
        y_values['demand'][i].append(cost)

        try:
            cost = incr_load_cost_funcs[i].subs(x, x_values['demand'][i][1])
        except AttributeError:
            cost = incr_load_cost_funcs[i]
        check_inf(cost)
        if cost > max_cost:
            max_cost = cost
        y_values['demand'][i].append(cost)

        y_values['demand'][i].append(0)
    
    plot_manager = plt.get_current_fig_manager()
    plot_manager.resize(*plot_manager.window.maxsize())

    # Plotting each Incremental Fuel Cost
    for i in range(plants):
        y_values['fuel'][i].append(max_cost)
        plt.plot(x_values['fuel'][i], y_values['fuel'][i], linestyle='-.', label=f'Generator{i+1}')
        plt.legend(bbox_to_anchor=(0, 1.12), ncol=6, loc='upper left', prop={'size':10})
        plt.pause(PLOT_PAUSE_TIME)
    
    # Plotting each Incremental Load Cost
    for i in range(loads):
        plt.plot(x_values['demand'][i], y_values['demand'][i], linestyle='-.', label=f'Demand{i+1}')
        plt.legend(bbox_to_anchor=(0, 1.12), ncol=6, loc='upper left', prop={'size':10})
        plt.pause(PLOT_PAUSE_TIME)
    

    # Aggregate values
    generator_aggregate = {'x': [], 'y': []}
    demand_aggregate = {'x': [], 'y': []}

    # The generator aggregate curve
    breaking_points = []
    for i in range(plants):
        for cost in y_values['fuel'][i]:
            breaking_points.append(cost)
    breaking_points = list(set(breaking_points))
    breaking_points = sorted(breaking_points)

    for breaking_point in breaking_points:
        x_aggregator = 0
        for i in range(plants):
            l = len(y_values['fuel'][i])
            for index, cost in enumerate(y_values['fuel'][i]):
                if (index + 1) < l:
                    if y_values['fuel'][i][index] <= breaking_point <= y_values['fuel'][i][index+1]:
                        x_intercept = find_line_intercept(x_values['fuel'][i][index],
                                                          x_values['fuel'][i][index+1],
                                                          y_values['fuel'][i][index],
                                                          y_values['fuel'][i][index+1],
                                                          breaking_point
                                                         )
                        if not math.isnan(x_intercept):
                            x_aggregator += x_intercept
                        break
                else:
                    if y_values['fuel'][i][index-1] <= breaking_point <= y_values['fuel'][i][index]:
                        x_intercept = find_line_intercept(x_values['fuel'][i][index-1],
                                                          x_values['fuel'][i][index],
                                                          y_values['fuel'][i][index-1],
                                                          y_values['fuel'][i][index],
                                                          breaking_point
                                                         )
                        if not math.isnan(x_intercept):
                            x_aggregator += x_intercept
                        break
        
        generator_aggregate['x'].append(x_aggregator)
        generator_aggregate['y'].append(breaking_point)
        

    plt.plot(generator_aggregate['x'], generator_aggregate['y'], linestyle='-', label='Generator aggregate')
    plt.legend(bbox_to_anchor=(0, 1.12), ncol=6, loc='upper left', prop={'size':10})
    plt.pause(PLOT_PAUSE_TIME)
    
    # The demand aggregate curve
    breaking_points.clear()
    for i in range(loads):
        for cost in y_values['demand'][i]:
            breaking_points.append(cost)
    breaking_points = list(set(breaking_points))
    breaking_points = sorted(breaking_points, reverse=True)

    for breaking_point in breaking_points:
        x_aggregator = 0
        for i in range(loads):
            l = len(y_values['demand'][i])
            for index, cost in enumerate(y_values['demand'][i]):
                if (index + 1) < l:
                    if y_values['demand'][i][index+1] <= breaking_point <= y_values['demand'][i][index]:
                        x_intercept = find_line_intercept(x_values['demand'][i][index],
                                                          x_values['demand'][i][index+1],
                                                          y_values['demand'][i][index],
                                                          y_values['demand'][i][index+1],
                                                          breaking_point
                                                         )
                        if not math.isnan(x_intercept):
                            x_aggregator += x_intercept
                        break
                else:
                    if y_values['demand'][i][index] <= breaking_point <= y_values['demand'][i][index-1]:
                        x_intercept = find_line_intercept(x_values['demand'][i][index-1],
                                                          x_values['demand'][i][index],
                                                          y_values['demand'][i][index-1],
                                                          y_values['demand'][i][index],
                                                          breaking_point
                                                         )
                        if not math.isnan(x_intercept):
                            x_aggregator += x_intercept
                        break
        
        demand_aggregate['x'].append(x_aggregator)
        demand_aggregate['y'].append(breaking_point)
    
    if 0 not in demand_aggregate['x']:
        top_cost = demand_aggregate['y'][0]
        demand_aggregate['y'].insert(0, top_cost)
        demand_aggregate['x'].insert(0, 0)

    plt.plot(demand_aggregate['x'], demand_aggregate['y'], linestyle='-', label='Demand aggregate')
    plt.legend(bbox_to_anchor=(0, 1.12), ncol=6, loc='upper left', prop={'size':10})
    plt.pause(PLOT_PAUSE_TIME)

    g_agg_len = len(generator_aggregate['x'])
    g_agg_len -= 1
    d_agg_len = len(demand_aggregate['x'])
    d_agg_len -= 1
    # Reduced the length by 1. The following for loop takes elements
    # in the indices i and i+1. So, the loop only needs to iterated
    # from 0 to max_index-1
    line1 = []
    line2 = []
    market_equillibrium_point = []
    for index_g in range(g_agg_len):
        line1.clear()
        line1.append([])
        line1.append([])

        line1[0].append(generator_aggregate['x'][index_g])
        line1[0].append(generator_aggregate['y'][index_g])

        line1[1].append(generator_aggregate['x'][index_g+1])
        line1[1].append(generator_aggregate['y'][index_g+1])

        for index_d in range(d_agg_len):
            line2.clear()
            line2.append([])
            line2.append([])

            line2[0].append(demand_aggregate['x'][index_d])
            line2[0].append(demand_aggregate['y'][index_d])

            line2[1].append(demand_aggregate['x'][index_d+1])
            line2[1].append(demand_aggregate['y'][index_d+1])

            eq_x, eq_y = poi.intersection_coordinates(line1, line2)
            if eq_x != 'no':
                if intersect_checker.check_for_intersection(line1, line2, eq_x, eq_y):
                    market_equillibrium_point.append(eq_x)
                    market_equillibrium_point.append(eq_y)
        if market_equillibrium_point:
            break

    market_clearing_quantity = market_equillibrium_point[0]
    market_clearing_price = market_equillibrium_point[1]

    equillibrium_plotter = {'x': [], 'y': []}

    equillibrium_plotter['x'].append(0)
    equillibrium_plotter['y'].append(market_clearing_price)

    equillibrium_plotter['x'].append(market_clearing_quantity)
    equillibrium_plotter['y'].append(market_clearing_price)

    equillibrium_plotter['x'].append(market_clearing_quantity)
    equillibrium_plotter['y'].append(0)

    plt.plot(equillibrium_plotter['x'], equillibrium_plotter['y'], linestyle='--', label='Market Equillibrium')
    plt.legend(bbox_to_anchor=(0, 1.12), ncol=6, loc='upper left', prop={'size':10})
    plt.pause(PLOT_PAUSE_TIME)

    plt.text(market_clearing_quantity, market_clearing_price+0.5,
             f'({market_clearing_quantity:.1f}, {market_clearing_price:.1f})',
             weight='bold'
            )
    
    print('\n\nAll Plotted Points')
    for i in range(plants):
        print(f'\nG{i+1}')
        print_points.show_marked_points(x_values['fuel'][i], y_values['fuel'][i])
    for i in range(loads):
        print(f'\nD{i+1}')
        print_points.show_marked_points(x_values['demand'][i], y_values['demand'][i])
    g_agg_len += 1
    print('\nGenerator Aggregate')
    print_points.show_marked_points(generator_aggregate['x'], generator_aggregate['y'])
    d_agg_len += 1
    print('\nDemand Aggregate')
    print_points.show_marked_points(demand_aggregate['x'], demand_aggregate['y'])
    # Continue from here
    # TODO
    # Also find all the power of each plant and load corresponding to MCP
    # Finally, find the cost for each

    plt.xlabel('Power (MW)')
    plt.ylabel('Incremental Cost ($/MWh)')
    plt.show()


if __name__ == '__main__':
    clr_screen()
    main()