import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt

[min, max, step] = [0, 1000, 0.2]
[min2, max2] = [min, 100]
# Generate universe variables
#   * Quality and service on subjective ranges [0, 10]
#   * Tip has a range of [0, 25] in units of percentage points
x_dist = np.arange(min, max, step)
x_vel = np.arange(min2, max2, step)

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
vel_nu = fuzz.trimf(x_vel, [0, 0, 25])
vel_lo = fuzz.trimf(x_vel, [0, 25, 50])
vel_md = fuzz.trimf(x_vel, [25, 50, 75])
vel_hi = fuzz.trimf(x_vel, [50, 75, 100])
vel_ma = fuzz.trimf(x_vel, [75, 100, 100])

# We need the activation of our fuzzy membership functions at these values.
# The exact values 6.5 and 9.8 do not exist on our universes...
# This is what fuzz.interp_membership exists for!

n_steps = (max - min) / step
vel1 = np.zeros(int(n_steps))
vel2 = np.zeros(int(n_steps))
vel3 = np.zeros(int(n_steps))
vel4 = np.zeros(int(n_steps))
vel5 = np.zeros(int(n_steps))
vel6 = np.zeros(int(n_steps))

n = 0
for d in np.arange(min, max, step):
    dist_level_vlo = fuzz.interp_membership(x_dist, dist_vlo, d)
    dist_level_lo = fuzz.interp_membership(x_dist, dist_lo, d)
    dist_level_md = fuzz.interp_membership(x_dist, dist_md, d)
    dist_level_hi = fuzz.interp_membership(x_dist, dist_hi, d)
    dist_level_vhi = fuzz.interp_membership(x_dist, dist_vhi, d)

    vel_activation_nu_su = dist_level_vlo * 0
    vel_activation_lo_su = dist_level_lo * 25
    vel_activation_md_su = dist_level_md * 50
    vel_activation_hi_su = dist_level_hi * 75
    vel_activation_ma_su = dist_level_vhi * 100
    vel6[n] = (
                      vel_activation_nu_su + vel_activation_lo_su + vel_activation_md_su + vel_activation_hi_su + vel_activation_ma_su) / (
                      dist_level_vlo + dist_level_lo + dist_level_md + dist_level_hi + dist_level_vhi)

    vel_activation_nu = np.fmin(dist_level_vlo, vel_nu)
    vel_activation_lo = np.fmin(dist_level_lo, vel_lo)
    vel_activation_md = np.fmin(dist_level_md, vel_md)
    vel_activation_hi = np.fmin(dist_level_hi, vel_hi)
    vel_activation_ma = np.fmin(dist_level_vhi, vel_ma)
    if d == 1000:
        print 'aa  ' + str(vel_ma)
    # Aggregate all three output membership functions together
    aggregated = np.fmax(vel_activation_nu,
                         np.fmax(vel_activation_lo,
                                 np.fmax(vel_activation_md,
                                         np.fmax(vel_activation_hi, vel_activation_ma))))

    # Calculate defuzzified result
    vel1[n] = fuzz.defuzz(x_vel, aggregated, 'centroid')
    vel2[n] = fuzz.defuzz(x_vel, aggregated, 'bisector')
    vel3[n] = fuzz.defuzz(x_vel, aggregated, 'mom')
    vel4[n] = fuzz.defuzz(x_vel, aggregated, 'som')
    vel5[n] = fuzz.defuzz(x_vel, aggregated, 'lom')
    if d == 1000:
        print 'aa  ' + str(vel1[n])

    n += 1
print vel1[1000]
font1 = {'style': 'oblique', 'color': 'black', 'size': 13}

fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(9, 8), sharex=True, sharey=True, gridspec_kw={'hspace': 0.12, 'wspace': 0.05})

axs[0, 1].plot(x_dist, vel1, 'b', linewidth=1, label='centroid')
axs[0, 1].set_title('Centroid')

axs[1, 1].plot(x_dist, vel2, 'g', linewidth=1, label='bisector')
axs[1, 1].set_title('Bisector')
axs[1, 1].set_xlabel('Absolute Hand to Cobot distance (mm)', fontdict=font1)

axs[0, 2].plot(x_dist, vel3, 'r', linewidth=1, label='mom')
axs[0, 2].set_title('Meam of Maximum (MoM)')

axs[1, 2].plot(x_dist, vel4, 'y', linewidth=1, label='som')
axs[1, 2].set_title('Min of Maximum (SoM)')

axs[0, 0].plot(x_dist, vel5, 'm', linewidth=1, label='lom')
axs[0, 0].set_title('Max of Maximum (LoM)')
axs[0, 0].set_ylabel('Velocity (%)', fontdict=font1, y=0)

axs[1, 0].plot(x_dist, vel6, 'k', linewidth=1, label='Sugeno')
axs[1, 0].set_title('Sugeno')

for ax in axs.flat:
    ax.grid(visible=True, linestyle='-.', linewidth=0.4)
#
# for ax in axs.flat:
#     ax.label_outer()
    # ax.spines['top'].set_visible(False)
    # ax.spines['right'].set_visible(False)
    # ax.get_xaxis().tick_bottom()
    # ax.get_yaxis().tick_left()
fig.suptitle('Different types of defuzzification methods', fontsize=18, weight='bold')

plt.tight_layout()
# plt.savefig('diffMetodsDefuzzy.png', bbox_inches='tight')

font1 = {'color': 'black', 'size': 20}
font2 = {'style': 'oblique', 'color': 'black', 'size': 16}

fig, ax0 = plt.subplots(figsize=(9, 8))

ax0.plot(x_dist, vel1, 'b', linewidth=0.9, label='Centroid')
ax0.plot(x_dist, vel2, 'g', linewidth=0.9, label='Bisector')
ax0.plot(x_dist, vel3, 'r', linewidth=0.9, label='Mom')
ax0.plot(x_dist, vel4, 'y', linewidth=0.9, label='Som')
ax0.plot(x_dist, vel5, 'm', linewidth=0.9, label='Lom')
ax0.plot(x_dist, vel6, 'k', linewidth=0.9, label='Sugeno')
ax0.set_title('Velocity(%) x Distance(mm)', fontdict=font1, weight='bold')
ax0.legend()
plt.yticks(np.arange(0, 110, 10))

for ax in (ax0,):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()


plt.ylabel('Velocity (%)', fontdict=font2)
plt.xlabel('Absolute Hand to Cobot distance (mm)', fontdict=font2)
plt.grid(visible=True, linestyle='-.', linewidth=0.4)
plt.tight_layout()
# plt.savefig('allDefuzzy.png', bbox_inches='tight', transparent=True)
plt.show()


