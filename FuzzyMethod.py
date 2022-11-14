import numpy as np
import skfuzzy as fuzz
import math
import UR3


def fuzzy_mamdani(dist, dist_max):

    if dist < dist_max:
        x_dist = np.arange(0, dist_max + 1, 1)
        x_vel = np.arange(0, 101, 1)

        dist_vlo = fuzz.membership.trapmf(x_dist, [0, 0, 200, 300])
        dist_lo = fuzz.trimf(x_dist, [100, 300, 500])
        dist_md = fuzz.membership.trapmf(x_dist, [300, 400, 600, 700])
        dist_hi = fuzz.trimf(x_dist, [500, 700, 900])
        dist_vhi = fuzz.membership.trapmf(x_dist, [700, 800, 1000, 1000])
        vel_nu = fuzz.membership.trapmf(x_vel, [0, 0, 20, 30])
        vel_lo = fuzz.trimf(x_vel, [10, 30, 50])
        vel_md = fuzz.membership.trapmf(x_vel, [30, 40, 60, 70])
        vel_hi = fuzz.trimf(x_vel, [50, 70, 90])
        vel_ma = fuzz.membership.trapmf(x_vel, [70, 80, 100, 100])

        dist_level_vlo = fuzz.interp_membership(x_dist, dist_vlo, dist)
        dist_level_lo = fuzz.interp_membership(x_dist, dist_lo, dist)
        dist_level_md = fuzz.interp_membership(x_dist, dist_md, dist)
        dist_level_hi = fuzz.interp_membership(x_dist, dist_hi, dist)
        dist_level_vhi = fuzz.interp_membership(x_dist, dist_vhi, dist)

        vel_activation_nu = np.fmin(dist_level_vlo, vel_nu)
        vel_activation_lo = np.fmin(dist_level_lo, vel_lo)
        vel_activation_md = np.fmin(dist_level_md, vel_md)
        vel_activation_hi = np.fmin(dist_level_hi, vel_hi)
        vel_activation_ma = np.fmin(dist_level_vhi, vel_ma)

        aggregated = np.fmax(vel_activation_nu,
                             np.fmax(vel_activation_lo,
                                     np.fmax(vel_activation_md,
                                             np.fmax(vel_activation_hi, vel_activation_ma))))

        vel1 = fuzz.defuzz(x_vel, aggregated, 'centroid')
        # vel2 = fuzz.defuzz(x_vel, aggregated, 'bisector')
        # vel3 = fuzz.defuzz(x_vel, aggregated, 'mom')
        # vel4 = fuzz.defuzz(x_vel, aggregated, 'som')
        # vel5 = fuzz.defuzz(x_vel, aggregated, 'lom')

        vel1 = vel1 / 100
        UR3.sendVel(vel1)
    else:
        UR3.sendVel(1)
    return


def fuzzy_sugeno(dist, dist_max):

    if dist < dist_max:
        x_dist = np.arange(0, dist_max + 1, 1)

        dist_vlo = fuzz.membership.trapmf(x_dist, [0, 0, 200, 300])
        dist_lo = fuzz.trimf(x_dist, [100, 300, 500])
        dist_md = fuzz.membership.trapmf(x_dist, [300, 400, 600, 700])
        dist_hi = fuzz.trimf(x_dist, [500, 700, 900])
        dist_vhi = fuzz.membership.trapmf(x_dist, [700, 800, 1000, 1000])

        dist_level_vlo = fuzz.interp_membership(x_dist, dist_vlo, dist)
        dist_level_lo = fuzz.interp_membership(x_dist, dist_lo, dist)
        dist_level_md = fuzz.interp_membership(x_dist, dist_md, dist)
        dist_level_hi = fuzz.interp_membership(x_dist, dist_hi, dist)
        dist_level_vhi = fuzz.interp_membership(x_dist, dist_vhi, dist)

        vel_activation_nu = dist_level_vlo * 0
        vel_activation_lo = dist_level_lo * 25
        vel_activation_md = dist_level_md * 50
        vel_activation_hi = dist_level_hi * 75
        vel_activation_ma = dist_level_vhi * 100

        vel1 = (vel_activation_nu + vel_activation_lo + vel_activation_md + vel_activation_hi + vel_activation_ma) / (dist_level_vlo + dist_level_lo + dist_level_md + dist_level_hi + dist_level_vhi)
        # vel2 = fuzz.defuzz(x_vel, aggregated, 'bisector')
        # vel3 = fuzz.defuzz(x_vel, aggregated, 'mom')
        # vel4 = fuzz.defuzz(x_vel, aggregated, 'som')
        # vel5 = fuzz.defuzz(x_vel, aggregated, 'lom')

        vel1 = vel1 / 100
        UR3.sendVel(vel1)
    else:
        UR3.sendVel(1)
    return




