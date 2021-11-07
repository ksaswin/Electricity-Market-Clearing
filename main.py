from sympy import symbols
import matplotlib.pyplot as plt
import math

import lines_intersection_check as intersect_checker
import point_of_intersection as poi
import show_all_points as print_points
import input_fetcher as fetcher

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
    valid_choice = 0
    func_or_points = '1'
    print('Would you like to give the inputs as functions or as x & y coordinates?')
    print('  (1)  Fuel cost functions\n  (2)  Data points\nPlease choose between 1 & 2.')
    while (not valid_choice):
        func_or_points = input('Enter your choice here: ')

        if func_or_points == '1' or func_or_points == '2':
            valid_choice = 1
        else:
            print(f'Sorry, {func_or_points} is not a valid choice.\nPlease enter either 1 or 2!\nTry again.\n\n')

    clr_screen()
    x_values = {'fuel': [], 'demand': []}
    y_values = {'fuel': [], 'demand': []}
    max_cost = 0

    if func_or_points == '1':
        plants = int(input('Enter the number of plants: '))

        fuel_cost_funcs, PLimits, incr_fuel_cost_funcs = fetcher.cost_functions_inputs(plants, 'g')

        loads = int(input('\nEnter the number of loads: '))

        demand_cost_funcs, DLimits, incr_load_cost_funcs = fetcher.cost_functions_inputs(loads, 'd')
        
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
    else:
        plants = int(input('Enter the number of plants: '))
        for i in range(plants):
            print(f'\nGeneration Company {i+1}')
            
            offers = int(input(f'Enter number of offers in GenCo{i+1}: '))
            price_list, power_list, max_cost = fetcher.plot_points_inputs(offers, 'g', max_cost)
            
            if 0 not in price_list:
                price_list.insert(0, 0)
                power_list.insert(0, power_list[0])
            
            power_list.append(power_list[-1])       # For the final max_cost value

            x_values['fuel'].append(power_list)
            y_values['fuel'].append(price_list)
        
        loads = int(input('\nEnter the number of loads: '))
        for i in range(loads):
            print(f'\nDistribution Company{i+1}')

            bids = int(input(f'Enter number of bids in DisCo{i+1}: '))
            price_list, power_list, max_cost = fetcher.plot_points_inputs(bids, 'd', max_cost)

            if 0 not in power_list:
                price_list.insert(0, max(price_list))
                power_list.insert(0, 0)

            x_values['demand'].append(power_list)
            y_values['demand'].append(price_list)
        
        clr_screen()
        

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
    
    if func_or_points == '2':
        print('All input values:')
        for i in range(plants):
            print(f'GenCo{i+1}')
            print_points.show_marked_points(x_values['fuel'][i], y_values['fuel'][i], ['Supply (MW)', 'Prices ($/MWh)'])
        
        for i in range(loads):
            print(f'DisCo{i+1}')
            print_points.show_marked_points(x_values['demand'][i], y_values['demand'][i], ['Demand (MW)', 'Prices ($/MWh)'])

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

    # Show the Market Equillibrium Point on the figure
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

    cleared_values = {'gen': {'x': [], 'y': []},
                      'dem': {'x': [], 'y': []}
                     }
    for i in range(plants):
        l = len(y_values['fuel'][i])
        for index, cost in enumerate(y_values['fuel'][i]):
            if (index + 1) < l:
                if y_values['fuel'][i][index] <= market_clearing_price <= y_values['fuel'][i][index+1]:
                    x_intercept = find_line_intercept(x_values['fuel'][i][index],
                                                      x_values['fuel'][i][index+1],
                                                      y_values['fuel'][i][index],
                                                      y_values['fuel'][i][index+1],
                                                      market_clearing_price
                                                     )
                    if not math.isnan(x_intercept):
                        cleared_values['gen']['x'].append(x_intercept)
                        cleared_values['gen']['y'].append(market_clearing_price)
                    break
            else:
                if y_values['fuel'][i][index-1] <= market_clearing_price <= y_values['fuel'][i][index]:
                    x_intercept = find_line_intercept(x_values['fuel'][i][index-1],
                                                      x_values['fuel'][i][index],
                                                      y_values['fuel'][i][index-1],
                                                      y_values['fuel'][i][index],
                                                      market_clearing_price
                                                     )
                    if not math.isnan(x_intercept):
                        cleared_values['gen']['x'].append(x_intercept)
                        cleared_values['gen']['y'].append(market_clearing_price)
                    break
    
    for i in range(loads):
        l = len(y_values['demand'][i])
        for index, cost in enumerate(y_values['demand'][i]):
            if (index + 1) < l:
                if y_values['demand'][i][index+1] <= market_clearing_price <= y_values['demand'][i][index]:
                    x_intercept = find_line_intercept(x_values['demand'][i][index],
                                                      x_values['demand'][i][index+1],
                                                      y_values['demand'][i][index],
                                                      y_values['demand'][i][index+1],
                                                      market_clearing_price
                                                     )
                    if not math.isnan(x_intercept):
                        cleared_values['dem']['x'].append(x_intercept)
                        cleared_values['dem']['y'].append(market_clearing_price)
                    break
            else:
                if y_values['demand'][i][index] <= market_clearing_price <= y_values['demand'][i][index-1]:
                    x_intercept = find_line_intercept(x_values['demand'][i][index-1],
                                                      x_values['demand'][i][index],
                                                      y_values['demand'][i][index-1],
                                                      y_values['demand'][i][index],
                                                      market_clearing_price
                                                     )
                    if not math.isnan(x_intercept):
                        cleared_values['dem']['x'].append(x_intercept)
                        cleared_values['dem']['y'].append(market_clearing_price)
                    break

    # for i in range(plants):
    #     plt.text(cleared_values['gen']['x'][i], cleared_values['gen']['y'][i]+0.5,
    #              f"({cleared_values['gen']['x'][i]:.1f}, {cleared_values['gen']['y'][i]:.1f})",
    #              weight='bold'
    #             )
    
    # for i in range(loads):
    #     plt.text(cleared_values['dem']['x'][i], cleared_values['dem']['y'][i]+0.5,
    #              f"({cleared_values['dem']['x'][i]:.1f}, {cleared_values['dem']['y'][i]:.1f})",
    #              weight='bold'
    #             )

    print('\n\nAll Market Cleared Values and Costs')
    print('Supply:')
    for i in range(plants):
        if func_or_points == '1':
            try:
                cost = fuel_cost_funcs[i].subs(x, cleared_values['gen']['x'][i])
            except AttributeError:
                cost = fuel_cost_funcs[i]
            print(f"    C{i+1} = {cost:.2f} $/h\n")
        print(f"    P{i+1} = {cleared_values['gen']['x'][i]:.2f} MW")

    print('Demand:')
    for i in range(loads):
        if func_or_points == '1':
            try:
                cost = demand_cost_funcs[i].subs(x, cleared_values['dem']['x'][i])
            except AttributeError:
                cost = fuel_cost_funcs[i]
            print(f"    D{i+1} = {cost:.2f} $/h\n")
        print(f"    P{i+1} = {cleared_values['dem']['x'][i]:.2f} MW")

    plt.xlabel('Power (MW)')
    plt.ylabel('Incremental Cost ($/MWh)')
    plt.show()


if __name__ == '__main__':
    clr_screen()
    main()