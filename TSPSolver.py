#!/usr/bin/python3
import copy
import heapq
import threading

import BranchAndBoundSolver
from GreedySolver import GreedySolver
import State
from State import State
from which_pyqt import PYQT_VER

if PYQT_VER == 'PYQT5':
    from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT4':
    from PyQt4.QtCore import QLineF, QPointF
else:
    raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

import time
import numpy as np
from TSPClasses import *
from BranchAndBoundSolver import BrandAndBoundSolver
import heapq
import itertools


class TSPSolver:
    def __init__(self, gui_view):
        self._scenario = None

    def setupWithScenario(self, scenario):
        self._scenario = scenario

    ''' <summary>
        This is the entry point for the default solver
        which just finds a valid random tour.  Note this could be used to find your
        initial BSSF.
        </summary>
        <returns>results dictionary for GUI that contains three ints: cost of solution, 
        time spent to find solution, number of permutations tried during search, the 
        solution found, and three null values for fields not used for this 
        algorithm</returns> 
    '''

    def defaultRandomTour(self, time_allowance=60.0):
        results = {}
        cities = self._scenario.getCities()
        ncities = len(cities)
        foundTour = False
        count = 0
        bssf = None
        start_time = time.time()
        while not foundTour and time.time() - start_time < time_allowance:
            # create a random permutation
            perm = np.random.permutation(ncities)
            route = []
            # Now build the route using the random permutation
            for i in range(ncities):
                route.append(cities[perm[i]])
            bssf = TSPSolution(route)
            count += 1
            if bssf.cost < np.inf:
                # Found a valid route
                foundTour = True
        end_time = time.time()
        results['cost'] = bssf.cost if foundTour else math.inf
        results['time'] = end_time - start_time
        results['count'] = count
        results['soln'] = bssf
        results['max'] = None
        results['total'] = None
        results['pruned'] = None
        return results

    ''' <summary>
        This is the entry point for the greedy solver, which you must implement for 
        the group project (but it is probably a good idea to just do it for the branch-and
        bound project as a way to get your feet wet).  Note this could be used to find your
        initial BSSF.
        </summary>
        <returns>results dictionary for GUI that contains three ints: cost of best solution, 
        time spent to find best solution, total number of solutions found, the best
        solution found, and three null values for fields not used for this 
        algorithm</returns> 
    '''

    def greedy(self, time_allowance=60.0):
        results = {}
        solver: GreedySolver = GreedySolver()

        startTime = time.time()
        solution: TSPSolution = solver.solve(self._scenario)
        duration = time.time() - startTime

        results['cost'] = np.inf if solution is None else solution.cost
        results['time'] = duration
        results['count'] = 1 if solution is not None else 0
        results['soln'] = solution
        results['max'] = None
        results['total'] = None
        results['pruned'] = None
        return results

    ''' <summary>
        This is the entry point for the branch-and-bound algorithm that you will implement
        </summary>
        <returns>results dictionary for GUI that contains three ints: cost of best solution, 
        time spent to find best solution, total number solutions found during search (does
        not include the initial BSSF), the best solution found, and three more ints: 
        max queue size, total number of states created, and number of pruned states.</returns> 
    '''

    def branchAndBound(self, time_allowance=60.0):
        startTime = time.time()
        greedyRes = self.greedy(self._scenario)
        if greedyRes is None:
            return None

        results = {}
        solver: BrandAndBoundSolver = BrandAndBoundSolver()
        solver.bestCostSoFar = greedyRes['cost']

        solver.solve(self._scenario, time_allowance, startTime)
        cost = greedyRes['cost']
        solution = greedyRes['soln']

        if solver.solutionFound:
            listOfCities = []
            for cityIdx in solver.currBestState.path:
                listOfCities.append(self._scenario.getCities()[cityIdx])

            solution: TSPSolution = TSPSolution(listOfCities)
            cost = solution.cost

        results['cost'] = cost
        results['time'] = solver.timeElapsed
        results['count'] = solver.numSolutions
        results['soln'] = solution
        results['max'] = solver.maxQSize
        results['total'] = solver.totalStates
        results['pruned'] = solver.numPrunedStates
        return results

    # ''' <summary>
    # 	This is the entry point for the algorithm you'll write for your group project.
    # 	</summary>
    # 	<returns>results dictionary for GUI that contains three ints: cost of best solution,
    # 	time spent to find best solution, total number of solutions found during search, the
    # 	best solution found.  You may use the other three field however you like.
    # 	algorithm</returns>
    # '''

    def fancy(self, time_allowance=60.0):
        pass
