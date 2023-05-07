from types import SimpleNamespace

import numpy as np
from scipy import optimize

import pandas as pd 
import matplotlib.pyplot as plt

class investment_model:

    def __init__(self):
        """ setup model """

        # a. create namespaces
        par = self.par = SimpleNamespace()
        sol = self.sol = SimpleNamespace()

        # b. preferences
        par.PH = 5
        par.P = 2
        par.A = 1
        par.beta = 0.9

    def profit(self,I):
        """ calculate utility """

        par = self.par
        sol = self.sol
     
        return par.PH*I - par.P*(I/par.A)**(1/par.beta)
    
    def solve(self,do_print=False):
        """ solve model continously """

        opt = SimpleNamespace()

        def choice(x):
            LM, HM, LF, HF = x
            return -self.calc_utility(LM,HM,LF,HF)
        
        cons = [{'type':'ineq', 'fun': lambda x: 24-x[0]-x[1]},
                {'type':'ineq', 'fun': lambda x: 24-x[2]-x[3]}]
        bounds = ((0,24),(0,24),(0,24),(0,24))

        # c. call solver
        initial_guess = [6,6,6,6]
        sol = optimize.minimize(choice,initial_guess,
                                method='Nelder-Mead',bounds=bounds,constraints=cons)

        # c. unpack solution

        opt.LM = sol.x[0]
        opt.HM = sol.x[1]
        opt.LF = sol.x[2]
        opt.HF = sol.x[3]

        return opt
    

    result = optimize.minimize_scalar(lambda x: -profit(x,PH,P,A,beta), method='golden')
I = result.x
pi = profit(I,PH,P,A,beta)
print(I)
print(pi)