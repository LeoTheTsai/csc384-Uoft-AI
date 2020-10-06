#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method).
      bt_search NEEDS to know this in order to correctly restore these
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated
        constraints)
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.


var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no
    propagation at all. Just check fully instantiated constraints'''

    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0: ## 0 constraint?
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []

def FCCheck(c, x, prune):
    for d in x.cur_domain():
        if not c.has_support(x, d):
            x.prune_value(d)
            prune.append((x, d))
    if x.cur_domain_size() == 0:
        return False, prune
    return True, prune

def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with
       only one uninstantiated variable. Remember to keep
       track of all pruned variable,value pairs and return '''
    final = [] # keep track all the (pruned var, value)

    if not newVar:
        all_cons = csp.get_all_cons()
    else:
        all_cons = csp.get_cons_with_var(newVar)

    for c in all_cons:
        num_unassign = c.get_n_unasgn()
        if num_unassign == 1: ## exactly one constraint, unassigned variable X
            unassign_all_var = c.get_unasgn_vars()  # V := PickUnassignedVariable()
            for var in unassign_all_var:
                    #  for each constraint C over V such that C has only one
                    #   unassigned variable X in its scope:
                tf, final = FCCheck(c, var, final)
                if not tf:
                    return tf, final
    return True, final


def GAC_Enforce(csp, GAC_Q, prune): #GAC_Q list of constraints
    while GAC_Q:
        C = GAC_Q.pop(0)
        for V in C.get_scope():
            for d in V.cur_domain():
                if not C.has_support(V, d):
                    V.prune_value(d)
                    prune.append((V, d))

                    if V.cur_domain_size() == 0:
                        GAC_Q.clear()
                        return False, prune
                    else:
                        #  push all constraints C’ such that V ∈ scope(C’)
                        #  and C’ ̸∈ GACQueue on to GACQueue
                        [GAC_Q.append(con) for con
                         in csp.get_cons_with_var(V) if con not in GAC_Q and V in con.get_scope()]
                    break
    return True, prune


def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
    final = []


    if not newVar:
        GAC_Q = csp.get_all_cons()
    else:
        GAC_Q = csp.get_cons_with_var(newVar)

    tf, final = GAC_Enforce(csp, GAC_Q, final)

    return tf, final


def ord_mrv(csp):
    ''' return variable according to the Minimum Remaining Values heuristic '''
    all_unassigned_var = csp.get_all_unasgn_vars()
    if all_unassigned_var == []:
        return None
    min_var = all_unassigned_var[0]
    min_value = min_var.cur_domain_size()
    for v in all_unassigned_var[1:]:
        v_value = v.cur_domain_size()
        if v_value < min_value:
            min_var = v
            min_value = v_value
    return min_var

