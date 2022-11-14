import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import time


# Sparse universe makes calculations faster, without sacrifice accuracy.
# Only the critical points are included here; making it higher resolution is
# unnecessary.

def Fuzzyhard(defuzz, before_dist, distance, robotvel, step=1001):
    aprox = (before_dist - distance) / 1000

    x_dist = ctrl.Antecedent(np.arange(0, 1001, 1), 'dist')
    x_robot_vel = ctrl.Antecedent(np.arange(0, 101, 1), 'rvel')
    x_aprox = ctrl.Antecedent(np.arange(-1, 1, 0.001), 'aproxi')
    x_vel = ctrl.Consequent(np.arange(0, 101, 1), 'dvel', defuzzify_method=defuzz)
    # Create the three fuzzy variables - three inputs, two output

    x_dist['Vclose'] = fuzz.membership.trapmf(x_dist.universe, [0, 0, 100, 300])
    x_dist['Close'] = fuzz.trimf(x_dist.universe, [100, 300, 500])
    x_dist['Average'] = fuzz.trimf(x_dist.universe, [300, 500, 700])
    x_dist['Far'] = fuzz.trimf(x_dist.universe, [500, 700, 900])
    x_dist['Vfar'] = fuzz.membership.trapmf(x_dist.universe, [700, 900, 1000, 1000])

    x_robot_vel['Vlow'] = fuzz.membership.trapmf(x_robot_vel.universe, [0, 0, 10, 30])
    x_robot_vel['Low'] = fuzz.trimf(x_robot_vel.universe, [10, 30, 50])
    x_robot_vel['Average'] = fuzz.trimf(x_robot_vel.universe, [30, 50, 70])
    x_robot_vel['High'] = fuzz.trimf(x_robot_vel.universe, [50, 70, 90])
    x_robot_vel['Vhigh'] = fuzz.membership.trapmf(x_robot_vel.universe, [70, 90, 100, 100])

    # afaz: se distancia da mao
    x_aprox['afaz'] = fuzz.membership.trapmf(x_aprox.universe, [-1, -1, 0, 0])
    x_aprox['aprox'] = fuzz.membership.trapmf(x_aprox.universe, [0, 0, 1, 1])

    x_vel['Null'] = fuzz.trimf(x_vel.universe, [0, 0, 25])
    x_vel['Slight'] = fuzz.trimf(x_vel.universe, [0, 25, 50])
    x_vel['Average'] = fuzz.trimf(x_vel.universe, [25, 50, 75])
    x_vel['Big'] = fuzz.trimf(x_vel.universe, [50, 75, 100])
    x_vel['Max'] = fuzz.trimf(x_vel.universe, [75, 100, 100])

    # Decrease Rules

    rule0 = ctrl.Rule(antecedent=((x_aprox['aprox'] & x_dist['Vclose'] & x_robot_vel['Vhigh'])),
                      consequent=x_vel['Null'], label='Null')

    rule1 = ctrl.Rule(antecedent=((x_aprox['aprox'] & x_dist['Vclose'] & x_robot_vel['Vlow']) |
                                  (x_aprox['aprox'] & x_dist['Vclose'] & x_robot_vel['Low']) |
                                  (x_aprox['aprox'] & x_dist['Vclose'] & x_robot_vel['Average']) |
                                  (x_aprox['aprox'] & x_dist['Vclose'] & x_robot_vel['High']) |
                                  (x_aprox['aprox'] & x_dist['Close'] & x_robot_vel['High']) |
                                  (x_aprox['aprox'] & x_dist['Close'] & x_robot_vel['Vhigh'])),
                      consequent=x_vel['Slight'], label='Slight')

    rule2 = ctrl.Rule(antecedent=((x_aprox['aprox'] & x_dist['Close'] & x_robot_vel['Vlow']) |
                                  (x_aprox['aprox'] & x_dist['Close'] & x_robot_vel['Low']) |
                                  (x_aprox['aprox'] & x_dist['Close'] & x_robot_vel['Average']) |
                                  (x_aprox['aprox'] & x_dist['Average'] & x_robot_vel['High']) |
                                  (x_aprox['aprox'] & x_dist['Average'] & x_robot_vel['Vhigh']) |
                                  (x_aprox['afaz'] & x_dist['Vclose'] & x_robot_vel['Vlow']) |
                                  (x_aprox['afaz'] & x_dist['Vclose'] & x_robot_vel['Low']) |
                                  (x_aprox['afaz'] & x_dist['Vclose'] & x_robot_vel['Average']) |
                                  (x_aprox['afaz'] & x_dist['Vclose'] & x_robot_vel['High']) |
                                  (x_aprox['afaz'] & x_dist['Vclose'] & x_robot_vel['Vhigh'])),
                      consequent=x_vel['Average'], label='Average')

    rule3 = ctrl.Rule(antecedent=((x_aprox['aprox'] & x_dist['Average'] & x_robot_vel['Vlow']) |
                                  (x_aprox['aprox'] & x_dist['Average'] & x_robot_vel['Low']) |
                                  (x_aprox['aprox'] & x_dist['Average'] & x_robot_vel['Average']) |
                                  (x_aprox['afaz'] & x_dist['Close'] & x_robot_vel['Vlow']) |
                                  (x_aprox['afaz'] & x_dist['Close'] & x_robot_vel['Low']) |
                                  (x_aprox['afaz'] & x_dist['Close'] & x_robot_vel['Average']) |
                                  (x_aprox['afaz'] & x_dist['Close'] & x_robot_vel['High']) |
                                  (x_aprox['afaz'] & x_dist['Close'] & x_robot_vel['Vhigh'])),
                      consequent=x_vel['Big'], label='Big')

    rule4 = ctrl.Rule(antecedent=((x_aprox['aprox'] & x_dist['Far'] & x_robot_vel['Vlow']) |
                                  (x_aprox['aprox'] & x_dist['Far'] & x_robot_vel['Low']) |
                                  (x_aprox['aprox'] & x_dist['Far'] & x_robot_vel['Average']) |
                                  (x_aprox['aprox'] & x_dist['Far'] & x_robot_vel['High']) |
                                  (x_aprox['aprox'] & x_dist['Far'] & x_robot_vel['Vhigh']) |
                                  (x_aprox['aprox'] & x_dist['Vfar'] & x_robot_vel['Vlow']) |
                                  (x_aprox['aprox'] & x_dist['Vfar'] & x_robot_vel['Low']) |
                                  (x_aprox['aprox'] & x_dist['Vfar'] & x_robot_vel['Average']) |
                                  (x_aprox['aprox'] & x_dist['Vfar'] & x_robot_vel['High']) |
                                  (x_aprox['aprox'] & x_dist['Vfar'] & x_robot_vel['Vhigh']) |
                                  (x_aprox['afaz'] & x_dist['Average'] & x_robot_vel['Vlow']) |
                                  (x_aprox['afaz'] & x_dist['Average'] & x_robot_vel['Low']) |
                                  (x_aprox['afaz'] & x_dist['Average'] & x_robot_vel['Average']) |
                                  (x_aprox['afaz'] & x_dist['Average'] & x_robot_vel['High']) |
                                  (x_aprox['afaz'] & x_dist['Average'] & x_robot_vel['Vhigh']) |
                                  (x_aprox['afaz'] & x_dist['Far'] & x_robot_vel['Vlow']) |
                                  (x_aprox['afaz'] & x_dist['Far'] & x_robot_vel['Low']) |
                                  (x_aprox['afaz'] & x_dist['Far'] & x_robot_vel['Average']) |
                                  (x_aprox['afaz'] & x_dist['Far'] & x_robot_vel['High']) |
                                  (x_aprox['afaz'] & x_dist['Far'] & x_robot_vel['Vhigh']) |
                                  (x_aprox['afaz'] & x_dist['Vfar'] & x_robot_vel['Vlow']) |
                                  (x_aprox['afaz'] & x_dist['Vfar'] & x_robot_vel['Low']) |
                                  (x_aprox['afaz'] & x_dist['Vfar'] & x_robot_vel['Average']) |
                                  (x_aprox['afaz'] & x_dist['Vfar'] & x_robot_vel['High']) |
                                  (x_aprox['afaz'] & x_dist['Vfar'] & x_robot_vel['Vhigh'])),
                      consequent=x_vel['Max'], label='Max')

    # Increase Rules

    system = ctrl.ControlSystem(rules=[rule0, rule1, rule2, rule3, rule4])

    sim = ctrl.ControlSystemSimulation(system, flush_after_run=step * step + 1)

    sim.input['dist'] = distance
    sim.input['rvel'] = robotvel
    sim.input['aproxi'] = aprox
    sim.compute()
    # outputvel =
    # # vel = robotvel/100 + (robotvel*outputvel/10000)
    # if vel > 1:
    #     vel = 1
    # elif vel < 0:
    #     vel = 0
    return (sim.output['dvel']/100)


# def main():
#     defuzz = ['centroid', 'bisector', 'mom', 'som', 'lom']
#     for i in range(0, 5):
#         print(Fuzzyhard(defuzz[i], 200, 300, 40))
#
# if __name__ == "__main__":
#     main()
