import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

d = 650
v = 75
ap = 0.5

# Generate universe variables
#   * Quality and service on subjective ranges [0, 10]
#   * Tip has a range of [0, 25] in units of percentage points
x_dist = np.arange(0, 1001, 1)
x_robot_vel = np.arange(0, 101, 1)
x_aprox = np.arange(-1, 1, 0.001)
x_vel = np.arange(0, 101, 1)
x_vel2 = np.arange(0, 101, 1)

# Generate fuzzy membership functions
# dist_vlo = fuzz.membership.trapmf(x_dist, [0, 0, 150, 250])
# dist_lo = fuzz.membership.trapmf(x_dist, [150, 250, 350, 450])
# dist_md = fuzz.membership.trapmf(x_dist, [350, 450, 550, 650])
# dist_hi = fuzz.membership.trapmf(x_dist, [550, 650, 750, 850])
# dist_vhi = fuzz.membership.trapmf(x_dist, [750, 850, 1000, 1000])
# vel_nu = fuzz.membership.trapmf(x_vel, [0, 0, 15, 25])
# vel_lo = fuzz.membership.trapmf(x_vel, [15, 25, 35, 45])
# vel_md = fuzz.membership.trapmf(x_vel, [35, 45, 55, 65])
# vel_hi = fuzz.membership.trapmf(x_vel, [55, 65, 75, 85])
# vel_ma = fuzz.membership.trapmf(x_vel, [75, 85, 100, 100])

dist_vlo = fuzz.membership.trapmf(x_dist, [0, 0, 100, 300])
dist_lo = fuzz.trimf(x_dist, [100, 300, 500])
dist_md = fuzz.trimf(x_dist, [300, 500, 700])
dist_hi = fuzz.trimf(x_dist, [500, 700, 900])
dist_vhi = fuzz.membership.trapmf(x_dist, [700, 900, 1000, 1000])

robot_vlo = fuzz.membership.trapmf(x_robot_vel, [0, 0, 10, 30])
robot_lo = fuzz.trimf(x_robot_vel, [10, 30, 50])
robot_md = fuzz.trimf(x_robot_vel, [30, 50, 70])
robot_hi = fuzz.trimf(x_robot_vel, [50, 70, 90])
robot_vhi = fuzz.membership.trapmf(x_robot_vel, [70, 90, 100, 100])

afaz = fuzz.membership.trapmf(x_aprox, [-1, -1, 0, 0])
aprox = fuzz.membership.trapmf(x_aprox, [0, 0, 1, 1])

vel_nu = fuzz.trimf(x_vel, [0, 0, 25])
vel_lo = fuzz.trimf(x_vel, [0, 25, 50])
vel_md = fuzz.trimf(x_vel, [25, 50, 75])
vel_hi = fuzz.trimf(x_vel, [50, 75, 100])
vel_ma = fuzz.trimf(x_vel, [75, 100, 100])

# vel_nu2 = fuzz.trimf(x_vel2, [0, 0, 25])
# vel_lo2 = fuzz.trimf(x_vel2, [0, 25, 50])
# vel_md2 = fuzz.trimf(x_vel2, [25, 50, 75])
# vel_hi2 = fuzz.trimf(x_vel2, [50, 75, 100])
# vel_ma2 = fuzz.trimf(x_vel2, [75, 100, 100])
# print 'aa  ' + str(vel_ma)
# Visualize these universes and membership functions
fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(12, 10), gridspec_kw={'hspace': 0.7})

ax0.plot(x_dist, dist_vlo, 'b', linewidth=1.5, label='Very Close')
ax0.plot(x_dist, dist_lo, 'g', linewidth=1.5, label='Close')
ax0.plot(x_dist, dist_md, 'r', linewidth=1.5, label='Average')
ax0.plot(x_dist, dist_hi, 'y', linewidth=1.5, label='Far')
ax0.plot(x_dist, dist_vhi, 'm', linewidth=1.5, label='Very Far')
ax0.set_title('Distance', fontsize=16)
ax0.legend()



ax1.plot(x_robot_vel, robot_vlo, 'b', linewidth=1.5, label='Very Slow')
ax1.plot(x_robot_vel, robot_lo, 'g', linewidth=1.5, label='Slow')
ax1.plot(x_robot_vel, robot_md, 'r', linewidth=1.5, label='Average')
ax1.plot(x_robot_vel, robot_hi, 'y', linewidth=1.5, label='High')
ax1.plot(x_robot_vel, robot_vhi, 'm', linewidth=1.5, label='Very High')
ax1.set_title('Input Velocity', fontsize=16)
ax1.legend(loc=5)



# ax3.plot(x_vel2, vel_nu2, 'b', linewidth=1.5, label='Null')
# ax3.plot(x_vel2, vel_lo2, 'g', linewidth=1.5, label='Slight')
# ax3.plot(x_vel2, vel_md2, 'r', linewidth=1.5, label='Average')
# ax3.plot(x_vel2, vel_hi2, 'y', linewidth=1.5, label='Big')
# ax3.plot(x_vel2, vel_ma2, 'm', linewidth=1.5, label='Max')
# ax3.set_title('Velocity', fontsize=16)
# ax3.legend(loc=5)

ax2.plot(x_aprox, afaz, 'b', linewidth=1.5, label='Separating')
ax2.plot(x_aprox, aprox, 'g', linewidth=1.5, label='Approaching')
ax2.set_title('Separating\\Approaching', fontsize=16)
ax2.legend(loc=5)

font1 = {'style': 'oblique', 'color': 'black', 'size': 11}
font3 = {'style': 'oblique', 'color': 'black', 'size': 9}
ax0.set_ylabel('Degree of Relevance', fontdict=font1)
ax0.set_xlabel('Absolute Hand to Cobot distance (mm)', fontdict=font1)

ax1.set_ylabel('Degree of Relevance', fontdict=font1)
ax1.set_xlabel('Robot Velocity (%)', fontdict=font1)

ax2.set_ylabel('Degree of Relevance', fontdict=font1)
ax2.set_xlabel('Difference of the previous Euclidean distance with the current one normalized between -1 and 1 (dimensionless)', fontdict=font3)
# ax1.set_ylabel('Degree of Relevance', fontdict=font1)
# ax1.set_xlabel('Velocity (%)', fontdict=font1)
# ax1.yticks(np.arange(0, 1.1, 0.1))
# Turn off top/right axes
for ax in (ax0, ax1, ax2):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()


fig.suptitle('Fuzzyfication of Input Variables', fontsize=18, weight='bold', y=0.97)
plt.tight_layout()
# plt.show()
plt.savefig('Fuzzyfication Input.png', bbox_inches = 'tight', transparent = True)

fig2, ax = plt.subplots(nrows=1, figsize=(12, 4))

ax.plot(x_vel, vel_nu, 'b', linewidth=1.5, label='Very Slow')
ax.plot(x_vel, vel_lo, 'g', linewidth=1.5, label='Slow')
ax.plot(x_vel, vel_md, 'r', linewidth=1.5, label='Average')
ax.plot(x_vel, vel_hi, 'y', linewidth=1.5, label='High')
ax.plot(x_vel, vel_ma, 'm', linewidth=1.5, label='Very High')
ax.set_title('Output Velocity', fontsize=16,y=0.97)
ax.legend(loc=5)

font2 = {'style': 'oblique', 'color': 'black', 'size': 13}
ax.set_ylabel('Degree of Relevance', fontdict=font2)
ax.set_xlabel('Robot Velocity (%)', fontdict=font2)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()

fig2.suptitle('Fuzzyfication of Output Variable', fontsize=18, weight='bold', y=1)
# plt.tight_layout()
plt.savefig('Fuzzyfication Output.png', bbox_inches = 'tight', transparent = True)
plt.show()



# degree of relevance

# We need the activation of our fuzzy membership functions at these values.
# The exact values 6.5 and 9.8 do not exist on our universes...
# This is what fuzz.interp_membership exists for!
# dist_level_vlo = fuzz.interp_membership(x_dist, dist_vlo, d)
# dist_level_lo = fuzz.interp_membership(x_dist, dist_lo, d)
# dist_level_md = fuzz.interp_membership(x_dist, dist_md, d)
# dist_level_hi = fuzz.interp_membership(x_dist, dist_hi, d)
# dist_level_vhi = fuzz.interp_membership(x_dist, dist_vhi, d)
#
# robot_level_vlo = fuzz.interp_membership(x_robot_vel, robot_vlo, v)
# robot_level_lo = fuzz.interp_membership(x_robot_vel, robot_lo, v)
# robot_level_md = fuzz.interp_membership(x_robot_vel, robot_md, v)
# robot_level_hi = fuzz.interp_membership(x_robot_vel, robot_hi, v)
# robot_level_vhi = fuzz.interp_membership(x_robot_vel, robot_vhi, v)
#
# afaz_level = fuzz.interp_membership(x_aprox, afaz, ap)
# aprox_level = fuzz.interp_membership(x_aprox, aprox, ap)
#
# # print  str(dist_level_vlo) + ' ' + str(dist_level_lo) + ' ' + str(dist_level_md) + ' ' + str(dist_level_hi) + ' ' + str(dist_level_vhi)
#
# # rule 1 null decrease: separating OR very far OR Far AND Vlow,Low,Avarage,high OR Avarege AND Low OR Avarege AND Vlow
# rule1 = np.fmax(afaz_level,
#                 np.fmax(dist_level_vhi,
#                         np.fmax(np.fmin(dist_level_lo, robot_level_vlo),
#                                 np.fmax(np.fmin(dist_level_lo, robot_level_lo),
#                                         np.fmax(np.fmin(dist_level_lo, robot_level_md),
#                                                 np.fmax(np.fmin(dist_level_lo, robot_level_hi),
#                                                         np.fmax(np.fmin(dist_level_md, robot_level_vlo),
#                                                                 np.fmax(np.fmin(dist_level_md, robot_level_lo)))))))))
#
# vel_activation_nu = np.fmin(rule1, vel_nu)
#
# # rule 2 slight decrease: Close AND Vlow,low OR Avarege AND Avarege,High OR Far AND Vhigh
#
# rule2 = np.fmax(np.fmin(dist_level_lo, robot_level_vlo),
#                 np.fmax(np.fmin(dist_level_lo, robot_level_lo),
#                         np.fmax(np.fmin(dist_level_md, robot_level_md),
#                                 np.fmax(np.fmin(dist_level_md, robot_level_hi),
#                                         np.fmax(np.fmin(dist_level_hi, robot_level_vhi))))))
#
# vel_activation_lo = np.fmin(rule2, vel_lo)
#
# # rule 3 avarege decrease: Close AND Avarage OR Avarage AND Vhigh
#
# rule3 = np.fmax(np.fmin(dist_level_lo, robot_level_md),
#                 np.fmax(np.fmin(dist_level_md, robot_level_vhi)))
#
#
# vel_activation_md = np.fmin(rule3, vel_md)
#
# # rule 4 big decrease: Close AND High,Vhigh
# rule4 = np.fmax(np.fmin(dist_level_lo,robot_level_hi),
#                 np.fmax(np.fmin(dist_level_lo,robot_level_vhi)))
#
# vel_activation_hi = np.fmin(rule4, vel_hi)
#
# # rule 4 max decrease: Close AND High,Vhigh
# rule4 = np.fmax(np.fmin(dist_level_lo,robot_level_hi),
#                 np.fmax(np.fmin(dist_level_lo,robot_level_vhi)))
# vel_activation_ma = np.fmin(dist_level_vhi, vel_ma)
#
#
#
#
#
#
# vel0 = np.zeros_like(x_vel)
#
# # Visualize this
# fig, ax0 = plt.subplots(figsize=(8, 3))
#
# ax0.fill_between(x_vel, vel0, vel_activation_nu, facecolor='b', alpha=0.7)
# ax0.plot(x_vel, vel_nu, 'b', linewidth=0.5, linestyle='--', )
# ax0.fill_between(x_vel, vel0, vel_activation_lo, facecolor='g', alpha=0.7)
# ax0.plot(x_vel, vel_lo, 'g', linewidth=0.5, linestyle='--')
# # ax0.fill_between(x_vel, vel0, vel_activation_md, facecolor='r', alpha=0.7)
# # ax0.plot(x_vel, vel_md, 'r', linewidth=0.5, linestyle='--')
# ax0.fill_between(x_vel, vel0, vel_activation_hi, facecolor='b', alpha=0.7)
# ax0.plot(x_vel, vel_hi, 'y', linewidth=0.5, linestyle='--', )
# ax0.fill_between(x_vel, vel0, vel_activation_ma, facecolor='b', alpha=0.7)
# ax0.plot(x_vel, vel_ma, 'm', linewidth=0.5, linestyle='--', )
# ax0.set_title('Output membership activity')
#
# # Turn off top/right axes
# for ax in (ax0,):
#     ax.spines['top'].set_visible(False)
#     ax.spines['right'].set_visible(False)
#     ax.get_xaxis().tick_bottom()
#     ax.get_yaxis().tick_left()
#
# plt.tight_layout()
#
# """
# .. image:: PLOT2RST.current_figure
#
# Rule aggregation
# ----------------
#
# With the *activity* of each output membership function known, all output
# membership functions must be combined. This is typically done using a
# maximum operator. This step is also known as *aggregation*.
#
# Defuzzification
# ---------------
# Finally, to get a real world answer, we return to *crisp* logic from the
# world of fuzzy membership functions. For the purposes of this example
# the centroid method will be used.
#
# The result is a tip of **20.2%**.
# ---------------------------------
# """
#
# # Aggregate all three output membership functions together
# aggregated = np.fmax(vel_activation_nu,
#                      np.fmax(vel_activation_lo,
#                              np.fmax(vel_activation_md,
#                                      np.fmax(vel_activation_hi, vel_activation_ma))))
#
# # Calculate defuzzified result
# vel1 = fuzz.defuzz(x_vel, aggregated, 'centroid')
# vel2 = fuzz.defuzz(x_vel, aggregated, 'bisector')
# vel3 = fuzz.defuzz(x_vel, aggregated, 'mom')
# vel4 = fuzz.defuzz(x_vel, aggregated, 'som')
# vel5 = fuzz.defuzz(x_vel, aggregated, 'lom')
# # print(vel1)
# # print("")
# # print(vel2)
# # print("")
# # print(vel3)
# # print("")
# # print(vel4)
# # print("")
# # print(vel5)
# vel_activation1 = fuzz.interp_membership(x_vel, aggregated, vel1)
# vel_activation2 = fuzz.interp_membership(x_vel, aggregated, vel2)
# vel_activation3 = fuzz.interp_membership(x_vel, aggregated, vel3)
# vel_activation4 = fuzz.interp_membership(x_vel, aggregated, vel4)
# vel_activation5 = fuzz.interp_membership(x_vel, aggregated, vel5)
#
# # Visualize this
# fig, ax0 = plt.subplots(figsize=(10, 5))
#
# ax0.plot(x_vel, vel_nu, 'k', linewidth=0.2, linestyle='--')
# ax0.plot(x_vel, vel_lo, 'k', linewidth=0.2, linestyle='--')
# ax0.plot(x_vel, vel_md, 'k', linewidth=0.2, linestyle='--')
# ax0.plot(x_vel, vel_hi, 'k', linewidth=0.2, linestyle='--')
# ax0.plot(x_vel, vel_ma, 'k', linewidth=0.2, linestyle='--')
# ax0.fill_between(x_vel, vel0, aggregated, facecolor='Orange', alpha=0.7)
# ax0.plot([vel1, vel1], [0, vel_activation1], 'b', linewidth=1.5, alpha=0.9, label='Centroid')
# ax0.plot([vel2, vel2], [0, vel_activation2], 'g', linewidth=1.5, alpha=0.9, label='Bisector')
# ax0.plot([vel3, vel3], [0, vel_activation3], 'r', linewidth=1.5, alpha=0.9, label='Mean of Maximum')
# ax0.plot([vel4, vel4], [0, vel_activation4], 'y', linewidth=1.5, alpha=0.9, label='Min of Maximum')
# ax0.plot([vel5, vel5], [0, vel_activation5], 'm', linewidth=1.5, alpha=0.9, label='Max of Maximum')
# ax0.set_title('Aggregated membership and result (line)',fontsize=18, weight='bold')
# ax0.legend(loc=2)
#
#
# # Turn off top/right axes
# for ax in (ax0,):
#     ax.spines['top'].set_visible(False)
#     ax.spines['right'].set_visible(False)
#     ax.get_xaxis().tick_bottom()
#     ax.get_yaxis().tick_left()
#
# # plt.ylabel('Velocity (%)')
# # font1 = {'color': 'black', 'size': 20}
# # font2 = {'style': 'oblique', 'color': 'black', 'size': 16}
# plt.ylabel('Degree of Relevance', fontdict=font1)
# plt.xlabel('Velocity (%)', fontdict=font1)
# plt.grid(visible=True, linestyle='-.', linewidth=0.4)
# plt.tight_layout()
# plt.savefig('OutputMenbership.png', bbox_inches='tight')
# plt.show()
# """
# .. image:: PLOT2RST.current_figure
#
# Final thoughts
# --------------
#
# The power of fuzzy systems is allowing complicated, intuitive behavior based
# on a sparse system of rules with minimal overhead. Note our membership
# function universes were coarse, only defined at the integers, but
# ``fuzz.interp_membership`` allowed the effective resolution to increase on
# demand. This system can respond to arbitrarily small changes in inputs,
# and the processing burden is minimal.
#
# """