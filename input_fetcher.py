from sympy import symbols
from sympy.parsing.sympy_parser import parse_expr
from sympy import diff


x = symbols('x')


# n is the number of plants or the number of loads
# g_d is to print what the input is for: Generator or Demand
def cost_functions_inputs(n, g_d):                          # Inputs taken as functions
    g_or_d = {'g': 'Generator', 'd': 'Demand'}
    c_or_d = {'g': 'C', 'd': 'D'}
    p_or_l = {'g': 'P', 'd': 'L'}

    cost_funcs = []
    PLimits = []                   # Generated or Load Power limits
    incr_cost_funcs = []           # Incremental cost functions

    print(f'\nEnter the {g_or_d[g_d]} Cost Functions below.')
    print('Only use x as the variable!')
    print('Please enter all power limits in MW.')
    for i in range(n):
        c = input(f'\n    {c_or_d[g_d]}{i+1} = ')
        c = c.replace('^', '**')
        c = parse_expr(c)
        cost_funcs.append(c)
        incr_cost_funcs.append(diff(c))
        print(f'  Enter {p_or_l[g_d]}min & Pmax for P{i+1}')
        Pmin = float(input(f'    {p_or_l[g_d]}min = '))
        Pmax = float(input(f'    {p_or_l[g_d]}max = '))
        PLimits.append([Pmin, Pmax])
    
    return cost_funcs, PLimits, incr_cost_funcs


# n is the number of offers/bids in a particular generator/distribution company
# g_d is to print what the input is for: Generator of Demand
# max_cost is the maximum cost. Used only for plotting purpose
def plot_points_inputs(n, g_d, max_cost):                          # Inputs taken as x and y co-ordinates
    g_or_d = {'g': ['offers', 'suppliers'], 'd': ['bids', 'buyers']}
    s_or_d = {'g': 'Supply', 'd':'Demand'}
    
    prices = []
    powers = []

    print(f'\nEnter the {g_or_d[g_d][0]} provided by the {g_or_d[g_d][1]}.')
    print('IMPORTANT: Please enter all coordinates in the ascending order of the x-values.')
    print(f'{s_or_d[g_d]} Power (MW) will be plotted on the x-axis.')
    print('Price ($/MWh) will be plotted on the y-axis.')
    for i in range(n):
        price = float(input(f'\n    Price ($/MWh) = '))
        power = float(input(f'    {s_or_d[g_d]} (MW) = '))
        
        prices.append(price)
        powers.append(power)
        if price > max_cost:
            max_cost = price
    
    return prices, powers, max_cost