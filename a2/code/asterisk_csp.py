#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects
representing the board. The returned list of lists is used to access the
solution.

For example, after these three lines of code

    csp, var_array = asterisk_csp_model_1(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the asterisk puzzle.

1. asterisk_csp_model_1 (worth 20/100 marks)
    - A model of an Asterisk grid built using only
      binary not-equal constraints

2. asterisk_csp_model_2 (worth 20/100 marks)
    - A model of an Asterisk grid built using only 9-ary
      all-different constraints

'''
from cspbase import *
import itertools
import os

def asterisk_csp_model_1(ast_grid):
    # create variables for each cell
    all_v = [] #contains variables with each element is a list of variables
    all_var_domain = [] # contains all the variables in the grid
    for i in range(len(ast_grid)):
        row_v = []
        for j in range(len(ast_grid[i])):
            cell = ast_grid[i][j]
            cell_domain = [1,2,3,4,5,6,7,8,9]
            if cell != None:
                cell_domain = [cell]
            var = Variable("v{}{}".format(i, j), cell_domain)
            row_v.append(var)
            all_var_domain.append(var)
        all_v.append(row_v)

    special_cons = [[2, 2], [4, 1], [6, 2], [6, 6], [7, 4], [4, 7], [4, 4],
                    [1, 4], [2, 6]]

    all_con = [] # all binary constraints
    # add binary constraints
    for i in range(0, 9): #row
        for j in range(0, 9): #col


            v1 = all_v[i][j] # initially v00

            for j_next in range(j + 1, 9):
                v2 = all_v[i][j_next]
                con = Constraint("C(V{}{}, V{}{})".format(i, j, i, j_next),
                                 [v1, v2])
                con.add_satisfying_tuples(create_sat_tuples([v1, v2]))
                all_con.append(con)


            for i_next in range(i + 1, 9):
                v2 = all_v[i_next][j]
                con = Constraint("C(V{}{}, V{}{})".format(i, j, i_next, j),
                                 [v1, v2])
                con.add_satisfying_tuples(create_sat_tuples([v1, v2]))
                all_con.append(con)



            for subcell_i in range(0, 3):
                for subcell_j in range(0, 3):
                    if (i % 3 == 2 or (subcell_i + (i // 3 * 3)) == i
                            or (subcell_j + (j //3 * 3)) == j or (i % 3) >
                            subcell_i):
                        continue
                    v2 = all_v[subcell_i + (i // 3 * 3)][subcell_j + (j // 3 * 3)]
                    con = Constraint("C(V{}{}, V{}{})".format(i, j, subcell_i + (i // 3 * 3), subcell_j + (j // 3 * 3)), [v1, v2])
                    con.add_satisfying_tuples(create_sat_tuples([v1, v2]))
                    all_con.append(con)

        v1 = all_v[special_cons[i][0]][special_cons[i][1]]
        for k in range(i + 1, 9):
            v2 = all_v[special_cons[k][0]][special_cons[k][1]]
            con = Constraint("C(V{}{}), V{}{}".format(special_cons[i][0],
                                                     special_cons[i][1], special_cons[k][0], special_cons[k][1]), [v1, v2])
            con.add_satisfying_tuples(create_sat_tuples([v1, v2]))
            all_con.append(con)

    csp = CSP("Binary_con_CSP", all_var_domain)
    for con in all_con:
        csp.add_constraint(con)


    return csp, all_v


def create_sat_tuples(l):
    # l is a list of the 2 variable that need to be check.
    sat_tuples = []
    for t in itertools.product(l[0].domain(), l[1].domain()):
        if t[0] != t[1]:
            sat_tuples.append(t)
    return sat_tuples


def asterisk_csp_model_2(ast_grid):
    all_v = []
    all_var_domain = []
    all_cons = []

    grid_length = len(ast_grid) # = 9, store the length so dont have to keep calling this

    special_cons = [[2, 2], [4, 1], [6, 2], [6, 6], [7, 4], [4, 7], [4, 4],
                    [1, 4], [2, 6]]

    col_dict = {} # store all the col variables and its domain and a list of list values with key represent the col#

    subcell_dict = {} # store all the subcell variables and its domain


    #create all variables and also create constraints for row
    for i in range(grid_length): #0-8
        row_v = []
        domain = []
        for j in range(grid_length):
            cell = ast_grid[i][j]
            cell_domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            if cell != None:
                cell_domain = [cell]
            var = Variable("v{}{}".format(i, j), cell_domain)
            row_v.append(var)
            all_var_domain.append(var)
            #adding domain for constraint tuple for row constraints
            domain.append(var.domain())

            #adding col variable and its domain
            add_var_to_dict(j, var, col_dict)

            #adding subcell variable and its domain
            add_subcell_var(i, j, var, subcell_dict)


        #create and add constraint for row
        con = Constraint("C(row{})".format(i + 1), row_v)
        con.add_satisfying_tuples(create_9_ary_sat_tuples(domain))
        all_cons.append(con)

        all_v.append(row_v)

    special_var = [[],[]]

    for i in range(grid_length):
        # add constraints for each col
        con = Constraint("C(col{})".format(i + 1), col_dict[i][0])
        con.add_satisfying_tuples(create_9_ary_sat_tuples(col_dict[i][1]))
        all_cons.append(con)

        # not sure if del will improve on space?
        del col_dict[i]

        # add all 9 constraints for subcell
        con = Constraint("C(subcell{})".format(i + 1), subcell_dict[i][0])
        con.add_satisfying_tuples(create_9_ary_sat_tuples(subcell_dict[i][1]))
        all_cons.append(con)
        del subcell_dict[i]


        # add 9 special variable for constraints
        sp_var = all_v[special_cons[i][0]][special_cons[i][1]]
        special_var[0].append(sp_var)
        special_var[1].append(sp_var.domain())

    # making special constraints
    con = Constraint("C(special)", special_var[0])
    con.add_satisfying_tuples(create_9_ary_sat_tuples(special_var[1]))
    all_cons.append(con)
    del special_var

    time = os.times()[0]
    csp = CSP("9_array_model_2_csp", all_var_domain)
    for con in all_cons:
        csp.add_constraint(con)
    return csp, all_v



def create_9_ary_sat_tuples(domain):
    sat_tuples = []


    #only generate possible constraints, so dont have to spend time iterate through
    #all product of domain
    set_var = {}
    for index, var_domain in enumerate(domain):
        if len(var_domain) == 1:
            set_var[index] = var_domain
    possible_var_domain  = []
    for i in range(1, 10):
        if [i] not in set_var.values():
            possible_var_domain.append(i)
    for t in itertools.permutations(possible_var_domain):
        l = list(t)
        for key, value in set_var.items():
            l.insert(key, value[0])
        sat_tuples.append(tuple(l))


    return sat_tuples


def add_var_to_dict(index, var, dic):
    if index not in dic:
        dic[index] = [[var], [var.domain()]]
    else:
        dic[index][0].append(var)
        dic[index][1].append(var.domain())

def add_subcell_var(i, j, var, subcell_dict):
    if j // 3 == 0:
        if i // 3 == 0:
            add_var_to_dict(0, var, subcell_dict)  # 0 represents top left
        elif i // 3 == 1:
            add_var_to_dict(1, var, subcell_dict)  # 1 represents left mid
        else:
            add_var_to_dict(2, var, subcell_dict)  # 2 represents bottom left
    elif j // 3 == 1:
        if i // 3 == 0:
            add_var_to_dict(3, var, subcell_dict)  # 3 represents top mid
        elif i // 3 == 1:
            add_var_to_dict(4, var, subcell_dict)  # 4 represents mid
        else:
            add_var_to_dict(5, var, subcell_dict)  # 5 represents bottom mid
    else:
        if i // 3 == 0:
            add_var_to_dict(6, var, subcell_dict)  # 6 represents top right
        elif i // 3 == 1:
            add_var_to_dict(7, var, subcell_dict)  # 7 represents right mid
        else:
            add_var_to_dict(8, var, subcell_dict)  # 8 represents bottom right




