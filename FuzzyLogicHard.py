import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import time
# Sparse universe makes calculations faster, without sacrifice accuracy.
# Only the critical points are included here; making it higher resolution is
# unnecessary.

def Fuzzyhard(defuzz):

    x_dist = ctrl.Antecedent(np.arange(0, 1001, 1), 'dist')
    x_robot_vel = ctrl.Antecedent(np.arange(0, 101, 1), 'rvel')
    x_aprox = ctrl.Antecedent(np.arange(-1, 1, 0.001), 'aproxi')
    x_vel = ctrl.Consequent(np.arange(0, 101, 1), 'dvel', defuzzify_method=defuzz)
    # x_vel2 = ctrl.Consequent(np.arange(0, 101, 1), 'ivel', defuzzify_method=defuzz)

    # Create the three fuzzy variables - two inputs, one output

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

    x_aprox['afaz']= fuzz.membership.trapmf(x_aprox.universe, [-1, -1, 0, 0])
    x_aprox['aprox'] = fuzz.membership.trapmf(x_aprox.universe, [0, 0, 1, 1])

    x_vel['Null'] = fuzz.trimf(x_vel.universe, [0, 0, 25])
    x_vel['Slight'] = fuzz.trimf(x_vel.universe, [0, 25, 50])
    x_vel['Average'] = fuzz.trimf(x_vel.universe, [25, 50, 75])
    x_vel['Big'] = fuzz.trimf(x_vel.universe, [50, 75, 100])
    x_vel['Max'] = fuzz.trimf(x_vel.universe, [75, 100, 100])
    #
    # x_vel2['Null'] = fuzz.trimf(x_vel2.universe, [0, 0, 25])
    # x_vel2['Slight'] = fuzz.trimf(x_vel2.universe, [0, 25, 50])
    # x_vel2['Average'] = fuzz.trimf(x_vel2.universe, [25, 50, 75])
    # x_vel2['Big'] = fuzz.trimf(x_vel2.universe, [50, 75, 100])
    # x_vel2['Max'] = fuzz.trimf(x_vel2.universe, [75, 100, 100])

    # Decrease Rules
    rule0 = ctrl.Rule(antecedent=((x_aprox['aprox'] & x_dist['Vclose'] & x_robot_vel['Vhigh'])),
                      consequent=x_vel['Null'], label='Null')

    rule1 = ctrl.Rule(antecedent=((x_aprox['aprox'] & x_dist['Vclose'] & x_robot_vel['Vlow']) |
                                  (x_aprox['aprox'] & x_dist['Vclose'] & x_robot_vel['Low']) |
                                  (x_aprox['aprox'] & x_dist['Vclose'] & x_robot_vel['Average']) |
                                  (x_aprox['aprox'] & x_dist['Vclose'] & x_robot_vel['High']) |
                                  (x_aprox['aprox'] & x_dist['Close'] & x_robot_vel['High']) |
                                  (x_aprox['aprox'] & x_dist['Close'] & x_robot_vel['Vhigh']) |
                                  (x_aprox['afaz'] & x_dist['Vclose'] & x_robot_vel['High']) |
                                  (x_aprox['afaz'] & x_dist['Vclose'] & x_robot_vel['Vhigh'])),
                      consequent=x_vel['Slight'], label='Slight')

    rule2 = ctrl.Rule(antecedent=((x_aprox['aprox'] & x_dist['Close'] & x_robot_vel['Vlow']) |
                                  (x_aprox['aprox'] & x_dist['Close'] & x_robot_vel['Low']) |
                                  (x_aprox['aprox'] & x_dist['Close'] & x_robot_vel['Average']) |
                                  (x_aprox['aprox'] & x_dist['Average'] & x_robot_vel['High']) |
                                  (x_aprox['aprox'] & x_dist['Average'] & x_robot_vel['Vhigh']) |
                                  (x_aprox['afaz'] & x_dist['Close'] & x_robot_vel['Vhigh']) |
                                  (x_aprox['afaz'] & x_dist['Vclose'] & x_robot_vel['Vlow']) |
                                  (x_aprox['afaz'] & x_dist['Vclose'] & x_robot_vel['Low']) |
                                  (x_aprox['afaz'] & x_dist['Vclose'] & x_robot_vel['Average'])),
                      consequent=x_vel['Average'], label='Average')

    rule3 = ctrl.Rule(antecedent=((x_aprox['aprox'] & x_dist['Average'] & x_robot_vel['Vlow']) |
                                  (x_aprox['aprox'] & x_dist['Average'] & x_robot_vel['Low']) |
                                  (x_aprox['aprox'] & x_dist['Average'] & x_robot_vel['Average']) |
                                  (x_aprox['afaz'] & x_dist['Close'] & x_robot_vel['Vlow']) |
                                  (x_aprox['afaz'] & x_dist['Close'] & x_robot_vel['Low']) |
                                  (x_aprox['afaz'] & x_dist['Close'] & x_robot_vel['Average']) |
                                  (x_aprox['afaz'] & x_dist['Close'] & x_robot_vel['High']) |
                                  (x_aprox['afaz'] & x_dist['Average'] & x_robot_vel['Vhigh'])),
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

    system = ctrl.ControlSystem(rules=[rule0, rule1, rule2, rule3, rule4])

    # rule0 = ctrl.Rule(antecedent=((x_aprox['aprox'] & x_robot_vel['Vlow'] & x_dist['Average']) |
    #                               (x_aprox['aprox'] & x_robot_vel['Vlow'] & x_dist['Far']) |
    #                               (x_aprox['aprox'] & x_robot_vel['Vlow'] & x_dist['Vfar']) |
    #                               (x_aprox['aprox'] & x_robot_vel['Low'] & x_dist['Average']) |
    #                               (x_aprox['aprox'] & x_robot_vel['Low'] & x_dist['Far']) |
    #                               (x_aprox['aprox'] & x_robot_vel['Low'] & x_dist['Vfar']) |
    #                               (x_aprox['aprox'] & x_robot_vel['Average'] & x_dist['Far']) |
    #                               (x_aprox['aprox'] & x_robot_vel['Average'] & x_dist['Vfar']) |
    #                               (x_aprox['aprox'] & x_robot_vel['High'] & x_dist['Far']) |
    #                               (x_aprox['aprox'] & x_robot_vel['High'] & x_dist['Vfar']) |
    #                               (x_aprox['aprox'] & x_robot_vel['Vhigh'] & x_dist['Vfar']) |
    #                               (x_aprox['afaz'] & x_robot_vel['Vlow'] & x_dist['Vclose']) |
    #                               (x_aprox['afaz'] & x_robot_vel['Vlow'] & x_dist['Close']) |
    #                               (x_aprox['afaz'] & x_robot_vel['Vlow'] & x_dist['Average']) |
    #                               (x_aprox['afaz'] & x_robot_vel['Vlow'] & x_dist['Far']) |
    #                               (x_aprox['afaz'] & x_robot_vel['Vlow'] & x_dist['Vfar']) |
    #                               (x_aprox['afaz'] & x_robot_vel['Low'] & x_dist['Vclose']) |
    #                               (x_aprox['afaz'] & x_robot_vel['Low'] & x_dist['Close']) |
    #                               (x_aprox['afaz'] & x_robot_vel['Low'] & x_dist['Average']) |
    #                               (x_aprox['afaz'] & x_robot_vel['Low'] & x_dist['Far']) |
    #                               (x_aprox['afaz'] & x_robot_vel['Low'] & x_dist['Vfar']) |
    #                               (x_aprox['afaz'] & x_robot_vel['Average'] & x_dist['Vclose']) |
    #                               (x_aprox['afaz'] & x_robot_vel['Average'] & x_dist['Close']) |
    #                               (x_aprox['afaz'] & x_robot_vel['Average'] & x_dist['Average']) |
    #                               (x_aprox['afaz'] & x_robot_vel['Average'] & x_dist['Far']) |
    #                               (x_aprox['afaz'] & x_robot_vel['Average'] & x_dist['Vfar']) |
    #                               (x_aprox['afaz'] & x_robot_vel['High'] & x_dist['Vclose']) |
    #                               (x_aprox['afaz'] & x_robot_vel['High'] & x_dist['Close']) |
    #                               (x_aprox['afaz'] & x_robot_vel['High'] & x_dist['Average']) |
    #                               (x_aprox['afaz'] & x_robot_vel['High'] & x_dist['Far']) |
    #                               (x_aprox['afaz'] & x_robot_vel['High'] & x_dist['Vfar']) |
    #                               (x_aprox['afaz'] & x_robot_vel['Vhigh'] & x_dist['Vclose']) |
    #                               (x_aprox['afaz'] & x_robot_vel['Vhigh'] & x_dist['Close']) |
    #                               (x_aprox['afaz'] & x_robot_vel['Vhigh'] & x_dist['Average']) |
    #                               (x_aprox['afaz'] & x_robot_vel['Vhigh'] & x_dist['Far']) |
    #                               (x_aprox['afaz'] & x_robot_vel['Vhigh'] & x_dist['Vfar'])),
    #                   consequent=x_vel['Null'], label='Null')
    #
    #
    # rule1 = ctrl.Rule(antecedent=((x_aprox['aprox'] & x_robot_vel['Vlow'] & x_dist['Close']) |
    #                               (x_aprox['aprox'] & x_robot_vel['Low'] & x_dist['Close']) |
    #                               (x_aprox['aprox'] & x_robot_vel['Average'] & x_dist['Average']) |
    #                               (x_aprox['aprox'] & x_robot_vel['High'] & x_dist['Average']) |
    #                               (x_aprox['aprox'] & x_robot_vel['Vhigh'] & x_dist['Far'])),
    #                   consequent=x_vel['Slight'], label='Slight')
    #
    # rule2 = ctrl.Rule(antecedent=((x_aprox['aprox'] & x_robot_vel['Average'] & x_dist['Close']) |
    #                               (x_aprox['aprox'] & x_robot_vel['Vhigh'] & x_dist['Average'])),
    #                   consequent=x_vel['Average'], label='Average')
    #
    # rule3 = ctrl.Rule(antecedent=((x_aprox['aprox'] & x_robot_vel['High'] & x_dist['Close']) |
    #                               (x_aprox['aprox'] & x_robot_vel['Vhigh'] & x_dist['Close'])),
    #                   consequent=x_vel['Big'], label='Big')
    #
    # rule4 = ctrl.Rule(antecedent=((x_aprox['aprox'] & x_robot_vel['Vlow'] & x_dist['Vclose']) |
    #                               (x_aprox['aprox'] & x_robot_vel['Low'] & x_dist['Vclose']) |
    #                               (x_aprox['aprox'] & x_robot_vel['Average'] & x_dist['Vclose']) |
    #                               (x_aprox['aprox'] & x_robot_vel['High'] & x_dist['Vclose']) |
    #                               (x_aprox['aprox'] & x_robot_vel['Vhigh'] & x_dist['Vclose'])),
    #                   consequent=x_vel['Max'], label='Max')
    #
    # # Increase Rules
    #
    # rule5 = ctrl.Rule(antecedent=((x_aprox['afaz'] & x_robot_vel['Average'] & x_dist['Vclose']) |
    #                               (x_aprox['afaz'] & x_robot_vel['High'] & x_dist['Vclose']) |
    #                               (x_aprox['afaz'] & x_robot_vel['Vhigh'] & x_dist['Vclose']) |
    #                               (x_aprox['afaz'] & x_robot_vel['Vhigh'] & x_dist['Close']) |
    #                               (x_aprox['aprox'] & x_robot_vel['Vlow'] & x_dist['Vclose']) |
    #                               (x_aprox['aprox'] & x_robot_vel['Vlow'] & x_dist['Close']) |
    #                               (x_aprox['aprox'] & x_robot_vel['Vlow'] & x_dist['Average']) |
    #                               (x_aprox['aprox'] & x_robot_vel['Vlow'] & x_dist['Far']) |
    #                               (x_aprox['aprox'] & x_robot_vel['Vlow'] & x_dist['Vfar']) |
    #                               (x_aprox['aprox'] & x_robot_vel['Low'] & x_dist['Vclose']) |
    #                               (x_aprox['aprox'] & x_robot_vel['Low'] & x_dist['Close']) |
    #                               (x_aprox['aprox'] & x_robot_vel['Low'] & x_dist['Average']) |
    #                               (x_aprox['aprox'] & x_robot_vel['Low'] & x_dist['Far']) |
    #                               (x_aprox['aprox'] & x_robot_vel['Low'] & x_dist['Vfar']) |
    #                               (x_aprox['aprox'] & x_robot_vel['Average'] & x_dist['Vclose']) |
    #                               (x_aprox['aprox'] & x_robot_vel['Average'] & x_dist['Close']) |
    #                               (x_aprox['aprox'] & x_robot_vel['Average'] & x_dist['Average']) |
    #                               (x_aprox['aprox'] & x_robot_vel['Average'] & x_dist['Far']) |
    #                               (x_aprox['aprox'] & x_robot_vel['Average'] & x_dist['Vfar']) |
    #                               (x_aprox['aprox'] & x_robot_vel['High'] & x_dist['Vclose']) |
    #                               (x_aprox['aprox'] & x_robot_vel['High'] & x_dist['Close']) |
    #                               (x_aprox['aprox'] & x_robot_vel['High'] & x_dist['Average']) |
    #                               (x_aprox['aprox'] & x_robot_vel['High'] & x_dist['Far']) |
    #                               (x_aprox['aprox'] & x_robot_vel['High'] & x_dist['Vfar']) |
    #                               (x_aprox['aprox'] & x_robot_vel['Vhigh'] & x_dist['Vclose']) |
    #                               (x_aprox['aprox'] & x_robot_vel['Vhigh'] & x_dist['Close']) |
    #                               (x_aprox['aprox'] & x_robot_vel['Vhigh'] & x_dist['Average']) |
    #                               (x_aprox['aprox'] & x_robot_vel['Vhigh'] & x_dist['Far']) |
    #                               (x_aprox['aprox'] & x_robot_vel['Vhigh'] & x_dist['Vfar'])),
    #                   consequent=x_vel2['Null'], label='Null2')
    #
    # rule6 = ctrl.Rule(antecedent=((x_aprox['afaz'] & x_robot_vel['Vlow'] & x_dist['Vclose']) |
    #                               (x_aprox['afaz'] & x_robot_vel['Low'] & x_dist['Vclose']) |
    #                               (x_aprox['afaz'] & x_robot_vel['Average'] & x_dist['Close']) |
    #                               (x_aprox['afaz'] & x_robot_vel['High'] & x_dist['Close'])),
    #                   consequent=x_vel2['Slight'], label='Slight2')
    #
    # rule7 = ctrl.Rule(antecedent=(x_aprox['afaz'] & x_robot_vel['Low'] & x_dist['Close']),
    #                   consequent=x_vel2['Average'], label='Average2')
    #
    # rule8 = ctrl.Rule(antecedent=(x_aprox['afaz'] & x_robot_vel['Vlow'] & x_dist['Close']),
    #                   consequent=x_vel2['Big'], label='Big2')
    #
    # rule9 = ctrl.Rule(antecedent=((x_aprox['afaz'] & x_robot_vel['Vlow'] & x_dist['Average']) |
    #                               (x_aprox['afaz'] & x_robot_vel['Vlow'] & x_dist['Far']) |
    #                               (x_aprox['afaz'] & x_robot_vel['Vlow'] & x_dist['Vfar']) |
    #                               (x_aprox['afaz'] & x_robot_vel['Low'] & x_dist['Average']) |
    #                               (x_aprox['afaz'] & x_robot_vel['Low'] & x_dist['Far']) |
    #                               (x_aprox['afaz'] & x_robot_vel['Low'] & x_dist['Vfar']) |
    #                               (x_aprox['afaz'] & x_robot_vel['Average'] & x_dist['Average']) |
    #                               (x_aprox['afaz'] & x_robot_vel['Average'] & x_dist['Far']) |
    #                               (x_aprox['afaz'] & x_robot_vel['Average'] & x_dist['Vfar']) |
    #                               (x_aprox['afaz'] & x_robot_vel['High'] & x_dist['Average']) |
    #                               (x_aprox['afaz'] & x_robot_vel['High'] & x_dist['Far']) |
    #                               (x_aprox['afaz'] & x_robot_vel['High'] & x_dist['Vfar']) |
    #                               (x_aprox['afaz'] & x_robot_vel['Vhigh'] & x_dist['Average']) |
    #                               (x_aprox['afaz'] & x_robot_vel['Vhigh'] & x_dist['Far']) |
    #                               (x_aprox['afaz'] & x_robot_vel['Vhigh'] & x_dist['Vfar'])),
    #                   consequent=x_vel2['Max'], label='Max2')
    #
    # system = ctrl.ControlSystem(rules=[rule0, rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])

    # Later we intend to run this system with a 21*21 set of inputs, so we allow
    # that many plus one unique runs before results are flushed.
    # Subsequent runs would return in 1/8 the time!
    step = 101
    sim = ctrl.ControlSystemSimulation(system, flush_after_run=step * step + 1)

    # sim.input['dist'] = 0
    # sim.input['rvel'] = 0
    # sim.input['aproxi'] = 0.5
    #
    # sim.compute()
    #
    # # print sim.print_state()
    # print '\n' + defuzz
    # print sim.output['dvel']
    # print sim.output['ivel']
    # print sim.output['ivel'] - sim.output['dvel']

    # We can simulate at higher resolution with full accuracy
    x_space = np.linspace(0, 1001, step)
    y_space = np.linspace(0, 101, step)
    x, y = np.meshgrid(x_space, y_space)
    z = np.zeros_like(x)
    # z2 = np.zeros_like(x)
    # print str(x) + ' \n a:' + str(y) + '\n b: ' + str(z)
    # print len(x)
    # print len(y)
    # print len(z)

    # Loop through the system 21*21 times to collect the control surface

    for i in range(step):
        for j in range(step):
            sim.input['dist'] = x[i, j]
            sim.input['rvel'] = y[i, j]
            sim.input['aproxi'] = 0.5
            sim.compute()
            z[i, j] = sim.output['dvel']
            # z2[i, j] = sim.output['ivel']




    # Plot the result in pretty 3D with alpha blending

    import matplotlib.pyplot as plt
    import matplotlib as mpl
    from mpl_toolkits.mplot3d import Axes3D  # Required for 3D plotting

    fig = plt.figure(figsize=(15, 6))
    ax = fig.add_subplot(121, projection='3d')

    surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap='viridis',vmin=0, vmax=100,
                           linewidth=0.4, antialiased=True)

    cset = ax.contourf(x, y, z, zdir='z', offset=-2.5, cmap='viridis',vmin=0, vmax=100, alpha=0.5)
    # cset = ax.contourf(x, y, z, zdir='x', offset=-100, cmap='viridis', alpha=0.5)
    cset = ax.contourf(x, y, z, zdir='y', offset=-7.5, cmap='viridis',vmin=0, vmax=100, alpha=0.5)

    font1 = {'color': 'black', 'size': 14}
    font2 = {'style': 'oblique', 'color': 'black', 'size': 12}

    ax.set_title('Resulting Speed in Approach', fontdict=font1, y=1.05)
    ax.set_xlabel('Distance (mm)', fontdict=font2)
    ax.set_ylabel('Input Velocity (%)', fontdict=font2)
    ax.set_zlabel('Output Velocity (%)', fontdict=font2)
    ax.set_zlim3d(0, 100)
    ax.view_init(30, 135)
    # plt.colorbar(mappable=surf, ticks=range(0, 101, 5), label='Velocity (%)', pad=0.1)
    # plt.savefig('RSA' + defuzz + '.png', bbox_inches = 'tight', transparent = True)

    # fig = plt.figure(figsize=(8, 8))
    # ax = fig.add_subplot(111, projection='3d')
    #
    # surf = ax.plot_surface(x, y, z2, rstride=1, cstride=1, cmap='viridis',
    #                        linewidth=0.4, antialiased=True)
    #
    # ax.set_title('Speed Increase in Approach', fontdict=font1, weight='bold', y=1.05)
    # ax.set_xlabel('Distance (mm)', fontdict=font2)
    # ax.set_ylabel('Velocity (%)', fontdict=font2)
    # ax.set_zlabel('Velocity Decrease (%)', fontdict=font2)
    # cset = ax.contourf(x, y, z2, zdir='z', offset=-2.5, cmap='viridis', alpha=0.5)
    # cset = ax.contourf(x, y, z2, zdir='x', offset=-100, cmap='viridis', alpha=0.5)
    # cset = ax.contourf(x, y, z2, zdir='y', offset=110, cmap='viridis', alpha=0.5)
    #
    # ax.set_zlim3d(0, 100)
    # ax.view_init(40, 315)
    # plt.savefig('SIA' + defuzz + '.png')

    for i in range(step):
        for j in range(step):
            sim.input['dist'] = x[i, j]
            sim.input['rvel'] = y[i, j]
            sim.input['aproxi'] = -0.5
            sim.compute()
            z[i, j] = sim.output['dvel']
            # z2[i, j] = sim.output['ivel']

    # fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(122, projection='3d')


    surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap='viridis',vmin=0, vmax=100,
                           linewidth=0.4, antialiased=True)

    cset = ax.contourf(x, y, z, zdir='z', offset=-2.5, cmap='viridis',vmin=0, vmax=100, alpha=0.5)
    # cset = ax.contourf(x, y, z, zdir='x', offset=1100, cmap='viridis', alpha=0.5)
    cset = ax.contourf(x, y, z, zdir='y', offset=-7.5, cmap='viridis',vmin=0, vmax=100, alpha=0.5)

    ax.set_title('Resulting Speed in Separation', fontdict=font1, y=1.05)
    ax.set_xlabel('Distance (mm)', fontdict=font2)
    ax.set_ylabel('Input Velocity (%)', fontdict=font2)
    ax.set_zlabel('Output Velocity (%)', fontdict=font2)
    ax.set_zlim3d(0, 100)
    ax.view_init(30, 135)
    cbaxes = fig.add_axes([0.93, 0.1, 0.02, 0.8])
    plt.colorbar(mappable=surf,cax=cbaxes, ticks=range(0, 101, 5), label='Velocity (%)')
    fig.suptitle('Defuzzification by ' + defuzz, fontsize=18, weight='bold', y=0.97)

    plt.savefig('RS' + defuzz + '.png', bbox_inches = 'tight', transparent = True)
    # plt.show()
    # fig2 = plt.figure(figsize=(8, 8))
    # ax2 = fig2.add_subplot(111, projection='3d')
    #
    # surf = ax2.plot_surface(x, y, z2, rstride=1, cstride=1, cmap='viridis',
    #                        linewidth=0.4, antialiased=True)
    #
    # cset = ax2.contourf(x, y, z2, zdir='z', offset=-2.5, cmap='viridis', alpha=0.5)
    # cset = ax2.contourf(x, y, z2, zdir='x', offset=1150, cmap='viridis', alpha=0)
    # cset = ax2.contourf(x, y, z2, zdir='y', offset=-5, cmap='viridis', alpha=0.5)
    #
    # ax2.set_title('Speed Increase in Separation', fontdict=font1, weight='bold', y=1.05)
    # ax2.set_xlabel('Distance (mm)', fontdict=font2)
    # ax2.set_ylabel('Velocity (%)', fontdict=font2)
    # ax2.set_zlabel('Velocity Decrease (%)', fontdict=font2)
    # ax2.set_zlim3d(0, 100)
    # ax2.view_init(30, 150)
    # plt.savefig('SIS' + defuzz + '.png')

    # for i in range(step):
    #     for j in range(step):
    #         sim.input['dist'] = x[i, j]
    #         sim.input['rvel'] = y[i, j]
    #         sim.input['aproxi'] = 0.5
    #         sim.compute()
    #         z[i, j] = abs(sim.output['ivel'] - sim.output['dvel'])

    # for i in range(step):
    #     for j in range(step):
    #         sim.input['dist'] = x[i, j]
    #         sim.input['rvel'] = y[i, j]
    #         sim.input['aproxi'] = -0.5
    #         sim.compute()
    #         z2[i, j] = sim.output['ivel'] - sim.output['dvel']

    # fig = plt.figure(figsize=(8, 8))
    # ax = fig.add_subplot(111, projection='3d')
    #
    # surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap='viridis',
    #                        linewidth=0.4, antialiased=True)
    #
    # cset = ax.contourf(x, y, z, zdir='z', offset=-2.5, cmap='viridis', alpha=0.5)
    # cset = ax.contourf(x, y, z, zdir='x', offset=-100, cmap='viridis', alpha=0.5)
    # cset = ax.contourf(x, y, z, zdir='y', offset=110, cmap='viridis', alpha=0.5)
    #
    # ax.set_title('Resulting Speed on Approach', fontdict=font1, weight='bold', y=1.05)
    # ax.set_xlabel('Distance (mm)', fontdict=font2)
    # ax.set_ylabel('Velocity (%)', fontdict=font2)
    # ax.set_zlabel('Velocity Decrease (%)', fontdict=font2)
    # ax.set_zlim3d(0, 100)
    # ax.view_init(30, 325)
    # # plt.savefig('RSA' + defuzz + '.png')
    #
    # fig2 = plt.figure(figsize=(8, 8))
    # ax2 = fig2.add_subplot(111, projection='3d')
    #
    # surf = ax2.plot_surface(x, y, z2, rstride=1, cstride=1, cmap='viridis',
    #                         linewidth=0.4, antialiased=True)
    #
    # cset = ax2.contourf(x, y, z2, zdir='z', offset=-2.5, cmap='viridis', alpha=0.5)
    # cset = ax2.contourf(x, y, z2, zdir='x', offset=1150, cmap='viridis', alpha=0)
    # cset = ax2.contourf(x, y, z2, zdir='y', offset=-5, cmap='viridis', alpha=0.5)
    #
    # ax2.set_title('Resulting Speed on Separation', fontdict=font1, weight='bold', y=1.05)
    # ax2.set_xlabel('Distance (mm)', fontdict=font2)
    # ax2.set_ylabel('Velocity (%)', fontdict=font2)
    # ax2.set_zlabel('Velocity Decrease (%)', fontdict=font2)
    # ax2.set_zlim3d(0, 100)
    # ax2.view_init(30, 150)
    # # plt.savefig('RSS' + defuzz + '.png')

    # plt.show()
    plt.close('all')
    return

def main():
    defuzz = ['Centroid', 'Bisector', 'Mom', 'Som', 'Lom']
    for i in range(0, 5):
        Fuzzyhard(defuzz[i])




if __name__ == "__main__":
    main()
