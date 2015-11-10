# -*- coding: utf-8 -*-


def interpolate(pos1, pos2, step):
    diff_unit = (
            float(pos2[0] - pos1[0]) / step,
            float(pos2[1] - pos1[1]) / step
            )
    return [(int(pos1[0] + diff_unit[0] * i),
            int(pos1[1] + diff_unit[1] * i))
            for i in range(step + 1)]

