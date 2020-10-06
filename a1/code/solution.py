#   Look for #IMPLEMENT tags in this file. These tags indicate what has
#   to be implemented to complete the warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

import os #for time functions
from search import * #for search engines
from rushhour import * #for Rush Hour specific classes and problems


#RUSH HOUR GOAL TEST
def rushhour_goal_fn(state):
#IMPLEMENT
  '''Have we reached a goal state?'''
  board = state.get_board_properties()
  goal_entrance = board[1]
  goal_direction = board[2]
  vehicles = state.get_vehicle_statuses()
  for v in vehicles:
    if v[-1] == True:
      if v[3] == True:
        if goal_direction == 'W' and v[1] == goal_entrance:
          return True
        elif goal_direction == 'E' and goal_entrance == (v[1][0] + v[2], v[1][1]):
          return True
      else:
        if goal_direction == 'N' and v[1] == goal_entrance:
          return True
        elif goal_direction == 'S' and goal_entrance == (v[1][0], v[1][1] + v[2]):
          return True

  return False #replace this

#RUSH HOUR HEURISTICS
def heur_zero(state):
#IMPLEMENT
  '''Zero Heuristic can be used to make A* search perform uniform cost search'''
  return 0 #replace this

def heur_min_moves(state):
#IMPLEMENT
  '''basic rushhour heuristic'''
  #An admissible heuristic is nice to have. Getting to the goal may require
  #many moves and each moves the goal vehicle one tile of distance.
  #Since the board wraps around, there are two different
  #directions that lead to the goal.
  #NOTE that we want an estimate of the number of ADDITIONAL
  #     moves required from our current state
  #1. Proceeding in the first direction, let MOVES1 =
  #   number of moves required to get to the goal if it were unobstructed
  #2. Proceeding in the second direction, let MOVES2 =
  #   number of moves required to get to the goal if it were unobstructed
  #
  #Our heuristic value is the minimum of MOVES1 and MOVES2 over all goal vehicles.
  #You should implement this heuristic function exactly, even if it is
  #tempting to improve it.
  board = state.get_board_properties()
  board_size = board[0] # board_size[0] = row, board_size[1] = column
  goal_entrance = board[1] #the goal location in (x,y)
  goal_direction = board[2] # the goal orientation
  vehicle = state.get_vehicle_statuses()
  for v in vehicle:
    if v[-1] == True:
      goal_vehicle = v   # goal_vehicle = [name, loc, length, is_horizontal, is_goal]

  if goal_direction == 'N':
    MOVES1, MOVES2 = min_move_north(goal_entrance, goal_vehicle, board_size)
  elif goal_direction == 'S':
    MOVES1, MOVES2 = min_move_south(goal_entrance, goal_vehicle, board_size)
  elif goal_direction == 'W':
    MOVES1, MOVES2 = min_move_west(goal_entrance, goal_vehicle, board_size)
  else:
    MOVES1, MOVES2 = min_move_east(goal_entrance, goal_vehicle, board_size)

  return min(MOVES1, MOVES2)


def min_move_north(goal_entrance, goal_vehicle, board_size):
  """"Return both move for the North direction.
  MOVE1 moving North towards goal, and MOVE2 moving in other direction
  to the goal."""
  if goal_entrance[1] >= goal_vehicle[1][1]:
    MOVES1 = goal_vehicle[1][1] + (board_size[0] - goal_entrance[1])
    MOVES2 = goal_entrance[1] - goal_vehicle[1][1]
  else:
    MOVES1 = goal_vehicle[1][1] - goal_entrance[1]
    MOVES2 = goal_entrance[1] + (board_size[0] - goal_vehicle[1][1])
  return MOVES1, MOVES2


def min_move_south(goal_entrance, goal_vehicle, board_size):
  """"Return both move for the South direction.
  MOVE1 moving South towards goal, and MOVE2 moving in other direction."""
  if (goal_vehicle[1][1] + goal_vehicle[2] > board_size[0]):
    tail = goal_vehicle[1][1] + goal_vehicle[2] - board_size[0] - 1
    MOVES1 = goal_entrance[1] - tail
    MOVES2 = board_size[0] - goal_entrance[1] + tail
  elif goal_entrance[1] >= (goal_vehicle[1][1] + goal_vehicle[2]):
    MOVES1 = goal_entrance[1] - (goal_vehicle[1][1] + goal_vehicle[2] - 1)
    MOVES2 = board_size[0] - goal_entrance[1] + (
              goal_vehicle[1][1] + goal_vehicle[2] - 1)
  else:
    MOVES1 = board_size[0] - (goal_vehicle[1][1] + goal_vehicle[2] - 1) + \
             goal_entrance[1]
    MOVES2 = (goal_vehicle[1][1] + goal_vehicle[2] - 1) - goal_entrance[1]
  return MOVES1, MOVES2

def min_move_west(goal_entrance, goal_vehicle, board_size):
  """"Return both move for the West direction.
  MOVE1 moving West towards goal, and MOVE2 move in other direction."""
  if goal_vehicle[1][0] >= goal_entrance[0]:
    MOVES1 = goal_vehicle[1][0] - goal_entrance[0]
    MOVES2 = board_size[1] - goal_vehicle[1][0] + goal_entrance[0]
  else:
    MOVES1 = board_size[1] - goal_entrance[0] + goal_vehicle[1][0]
    MOVES2 = goal_entrance[0] - goal_vehicle[1][0]
  return MOVES1, MOVES2

def min_move_east(goal_entrance, goal_vehicle, board_size):
  """"Return both move for the East direction.
   MOVE1 moving East towards goal, and MOVE2 move in other direction."""
  if (goal_vehicle[1][0] + goal_vehicle[2] > board_size[1]):
    east_tail = goal_vehicle[1][0] + goal_vehicle[2] - board_size[1] - 1
    MOVES1 = goal_entrance[0] - east_tail
    MOVES2 = board_size[1] - goal_entrance[0] + east_tail
  elif (goal_vehicle[1][0] + goal_vehicle[2] >= goal_entrance[0]):
    MOVES1 = board_size[1] - (goal_vehicle[1][0] + goal_vehicle[2] - 1) + \
             goal_entrance[0]
    MOVES2 = goal_vehicle[1][0] + goal_vehicle[2] - 1 - goal_entrance[0]
  else:
    MOVES1 = goal_entrance[0] - (goal_vehicle[1][0] + goal_vehicle[2] - 1)
    MOVES2 = board_size[1] - goal_entrance[0] + (
              goal_vehicle[1][0] + goal_vehicle[2] - 1)
  return MOVES1, MOVES2


def heur_alternate(state):
#IMPLEMENT
  '''a better heuristic'''
  '''INPUT: a rush hour state'''
  '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
  #heur_min_moves has an obvious flaw.
  #Write a heuristic function that improves a little upon heur_min_moves to estimate distance between the current state and the goal.
  #Your function should return a numeric value for the estimate of the distance to the goal.

  #beside the move from both MOVE1 and MOVE2, add an additional cost if there's
  #another vehical encounter on both MOVE1 and MOVE2, then take the min of it.

  board = state.get_board_properties()
  board_size = board[0] # board_size[0] = row, board_size[1] = column
  goal_entrance = board[1] #the goal location in (x,y)
  goal_direction = board[2] # the goal orientation
  vehicle = state.get_vehicle_statuses()
  for v in vehicle:
    if v[-1] == True:
      goal_vehicle = v   # goal_vehicle = [name, loc, length, is_horizontal, is_goal]
      break

  if goal_direction == 'N':
    MOVE1, MOVE2 = min_move_north(goal_entrance, goal_vehicle, board_size)
    add_cost1, add_cost2 = num_object_on_the_way_N(vehicle, goal_entrance, goal_vehicle, board_size)
  elif goal_direction == 'S':
    MOVE1, MOVE2 = min_move_south(goal_entrance, goal_vehicle, board_size)
    add_cost1, add_cost2 = num_object_on_the_way_S(vehicle, goal_entrance, goal_vehicle, board_size)
  elif goal_direction == 'W':
    MOVE1, MOVE2 = min_move_west(goal_entrance, goal_vehicle, board_size)
    add_cost1, add_cost2 = num_object_on_the_way_W(vehicle, goal_entrance, goal_vehicle, board_size)
  else:
    MOVE1, MOVE2 = min_move_east(goal_entrance, goal_vehicle, board_size)
    add_cost1, add_cost2 = num_object_on_the_way_E(vehicle, goal_entrance, goal_vehicle, board_size)

  return min(MOVE1 + add_cost1, MOVE2 + add_cost2)


def num_object_on_the_way_N(vehicles, goal_entrance, goal_vehicle, board_size):
  COST1, COST2 = 0, 0
  if goal_entrance[1] >= goal_vehicle[1][1]:
    COST1_bound = list(range(0, goal_vehicle[1][1])) # space between goal loc to bound 0
    COST1_bound.extend(list(range(goal_entrance[1], board_size[0]))) # total intersection to check
    COST2_bound = list(range(goal_vehicle[1][1], goal_entrance[1]))
  else:
    COST1_bound = list(range(goal_entrance[1], goal_vehicle[1][1]))
    COST2_bound = list(range(0, goal_entrance[1]))
    COST2_bound.extend(list(range(goal_vehicle[1][1], board_size[0])))
  for v in vehicles:
    if v != goal_vehicle and v[3] != False and \
            (v[1][0] <= goal_vehicle[1][0] or (
                    v[1][0] + v[2] - board_size[1] - 1) >= goal_vehicle[1][0]):
      if v[1][0] == goal_vehicle[1][0]:
        if v[1][1] in COST1_bound:
          COST1 += 1
        elif v[1][1] in COST2_bound:
          COST2 += 1
      elif v[1][0] < goal_vehicle[1][0] and (v[1][0] + v[2] - 1) >= \
              goal_vehicle[1][0]:
        if v[1][1] in COST1_bound:
          COST1 += 1
        elif v[1][1] in COST2_bound:
          COST2 += 1
      elif v[1][0] > goal_vehicle[1][0] and (
              v[1][0] + v[2] - board_size[1] - 1) >= goal_vehicle[1][0]:
        if v[1][1] in COST1_bound:
          COST1 += 1
        elif v[1][1] in COST2_bound:
          COST2 += 1

  return COST1, COST2

def num_object_on_the_way_S(vehicles, goal_entrance, goal_vehicle, board_size):
  COST1, COST2 = 0, 0

  if (goal_vehicle[1][1] + goal_vehicle[2] > board_size[0]):
    tail = goal_vehicle[1][1] + goal_vehicle[2] - board_size[0] - 1
    COST1_bound = list(range(tail, goal_entrance[1]))
    COST2_bound = list(range(goal_entrance[1], goal_vehicle[1][1]))

  elif goal_entrance[1] >= (goal_vehicle[1][1] + goal_vehicle[2]):
    COST1_bound = list(range(goal_vehicle[1][1] + goal_vehicle[2], goal_entrance[1]))
    COST2_bound = list(range(0, goal_vehicle[1][1]))
    COST2_bound.extend(list(range(goal_entrance[1], board_size[0])))

  else:
    COST1_bound = list(range(0, goal_entrance[1]))
    COST1_bound.extend(list(range(goal_vehicle[1][1] + goal_vehicle[2], board_size[0])))
    COST2_bound = list(range(goal_entrance[1], goal_vehicle[1][1]))

  for v in vehicles:
    if v != goal_vehicle and v[3] != False and \
            (v[1][0] <= goal_vehicle[1][0] or (
                    v[1][0] + v[2] - board_size[1] - 1) >= goal_vehicle[1][0]):
      if v[1][0] == goal_vehicle[1][0]:
        if v[1][1] in COST1_bound:
          COST1 += 1
        elif v[1][1] in COST2_bound:
          COST2 += 1
      elif v[1][0] < goal_vehicle[1][0] and (v[1][0] + v[2] - 1) >= goal_vehicle[1][0]:
        if v[1][1] in COST1_bound:
          COST1 += 1
        elif v[1][1] in COST2_bound:
          COST2 += 1
      elif v[1][0] > goal_vehicle[1][0] and (v[1][0] + v[2] - board_size[1] - 1) >= goal_vehicle[1][0]:
        if v[1][1] in COST1_bound:
          COST1 += 1
        elif v[1][1] in COST2_bound:
          COST2 += 1

  return COST1, COST2

def num_object_on_the_way_W(vehicles, goal_entrance, goal_vehicle, board_size):
  COST1, COST2 = 0, 0
  if goal_vehicle[1][0] >= goal_entrance[0]:
    COST1_bound = list(range(goal_entrance[0], goal_vehicle[1][0]))
    COST2_bound = list(range(0, goal_entrance[0]))
    COST2_bound.extend(list(range(goal_vehicle[1][0], board_size[1])))
  else:
    COST1_bound = list(range(0, goal_vehicle[1][0]))
    COST1_bound.extend(list(range(goal_entrance[0], board_size[1])))
    COST2_bound = list(range(goal_vehicle[1][0], goal_entrance[0]))
  for v in vehicles:
    if v != goal_vehicle and v[3] != True and \
            (v[1][1] <= goal_vehicle[1][1] or (
                    v[1][1] + v[2] - board_size[0] - 1) >= goal_vehicle[1][1]):
      #check if its goal car or horizontal == False since its facing EAST
      #Also check if v's y coord is less than goal car
      #if it's greater then it's cannot intersect unless large length.
      if v[1][1] == goal_vehicle[1][1]:
        if v[1][0] in COST1_bound:
          COST1 += 1
        elif v[1][0] in COST2_bound:
          COST2 += 1
      elif v[1][1] < goal_vehicle[1][1] and (v[1][1] + v[2] - 1) >= goal_vehicle[1][1]:
        if v[1][0] in COST1_bound:
          COST1 += 1
        elif v[1][0] in COST2_bound:
          COST2 += 1
      elif v[1][1] > goal_vehicle[1][1] and (v[1][1] + v[2] - board_size[0] - 1) >= goal_vehicle[1][1]:
        if v[1][0] in COST1_bound:
          COST1 += 1
        elif v[1][0] in COST2_bound:
          COST2 += 1

  return COST1, COST2

def num_object_on_the_way_E(vehicles, goal_entrance, goal_vehicle, board_size):
  COST1, COST2 = 0, 0

  if (goal_vehicle[1][0] + goal_vehicle[2] > board_size[1]):
    east_tail = goal_vehicle[1][0] + goal_vehicle[2] - board_size[1] - 1
    COST1_bound = list(range(east_tail, goal_entrance[0]))
    COST2_bound = list(range(goal_entrance[0], goal_vehicle[1][0]))

  elif (goal_vehicle[1][0] + goal_vehicle[2] >= goal_entrance[0]):
    COST1_bound = list(range(0, goal_entrance[0]))
    COST1_bound.extend(list(range(goal_vehicle[1][0] + goal_vehicle[2], board_size[1])))
    COST2_bound = list(range(goal_entrance[0], goal_vehicle[1][0]))

  else:
    COST1_bound = list(range(goal_vehicle[1][0] + goal_vehicle[2], goal_entrance[0]))
    COST2_bound = list(range(0, goal_vehicle[1][0]))
    COST2_bound.extend(list(range(goal_entrance[0], board_size[1])))

  for v in vehicles:
    if v != goal_vehicle and v[3] != True and \
            (v[1][1] <= goal_vehicle[1][1] or (
                    v[1][1] + v[2] - board_size[0] - 1) >= goal_vehicle[1][1]):
      #check if its goal car or horizontal == False since its facing EAST
      #Also check if v's y coord is less than goal car
      #if it's greater then it's cannot intersect unless large length.
      if v[1][1] == goal_vehicle[1][1]:
        if v[1][0] in COST1_bound:
          COST1 += 1
        elif v[1][0] in COST2_bound:
          COST2 += 1
      elif v[1][1] < goal_vehicle[1][1] and (v[1][1] + v[2] - 1) >= goal_vehicle[1][1]:
        if v[1][0] in COST1_bound:
          COST1 += 1
        elif v[1][0] in COST2_bound:
          COST2 += 1
      elif v[1][1] > goal_vehicle[1][1] and (v[1][1] + v[2] - board_size[0] - 1) >= goal_vehicle[1][1]:
        if v[1][0] in COST1_bound:
          COST1 += 1
        elif v[1][0] in COST2_bound:
          COST2 += 1

  return COST1, COST2



def fval_function(sN, weight):
#IMPLEMENT
  """
  Provide a custom formula for f-value computation for Anytime Weighted A star.
  Returns the fval of the state contained in the sNode.

  @param sNode sN: A search node (containing a rush hour state)
  @param float weight: Weight given by Anytime Weighted A star
  @rtype: float
  """

  #Many searches will explore nodes (or states) that are ordered by their f-value.
  #For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
  #You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
  #The function must return a numeric f-value.
  #The value will determine your state's position on the Frontier list during a 'custom' search.
  #You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.
  return sN.gval + weight * sN.hval #replace this

def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound = 10):
#IMPLEMENT
  '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
  '''INPUT: a rush hour state that represents the start state and a timebound (number of seconds)'''
  '''OUTPUT: A goal state (if a goal is found), else False'''
  '''implementation of weighted astar algorithm'''


  se = SearchEngine("custom", "full")
  wrapped_fval_function = (lambda sN: fval_function(sN, weight))
  se.init_search(initial_state, rushhour_goal_fn, heur_fn, wrapped_fval_function)
  current_time = os.times()[0]
  search = se.search(timebound)  # return either false or goal_node.state, a StateSpace object
  costbound = (float("inf"), float("inf"), float("inf"))

  while current_time < timebound:
    if search == False:
      return False
    else:
      if (search.gval + search.hval < costbound[
        2]):  # since search is a StateSpace Object, can access gval, hval property
        costbound = (float("inf"), float("inf"), search.gval + heur_fn(search))
      current_time = os.times()[0]
      search = se.search(timebound - current_time, costbound)
      if weight > 1:
        weight -= 0.1

  return search  # replace this




def anytime_gbfs(initial_state, heur_fn, timebound = 10):
#IMPLEMENT
  '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
  '''INPUT: a rush hour state that represents the start state and a timebound (number of seconds)'''
  '''OUTPUT: A goal state (if a goal is found), else False'''
  '''implementation of anytime greedybfs algorithm'''

  se = SearchEngine("best_first", "full")
  se.init_search(initial_state, rushhour_goal_fn, heur_fn)
  current_time = os.times()[0]
  search = se.search(timebound) #return either false or goal_node.state, a StateSpace object
  costbound = (float("inf"), float("inf"), float("inf"))

  while current_time < timebound:
    if search == False:
      return search
    else:
      if (search.gval < costbound[0]):  #since search is a StateSpace Object, can access gval property
        costbound = (search.gval, float("inf"), float("inf"))
      current_time = os.times()[0]
      search = se.search(timebound - current_time, costbound)

  return search #replace this




