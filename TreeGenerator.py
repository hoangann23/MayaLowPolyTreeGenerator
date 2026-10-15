import maya.cmds as cmds
import random

import sys
sys.path.append("/Users/ahluong/Documents/maya/projects/PersonalProjects/scripts")

import branch_functions
import trunk_functions
import importlib

importlib.reload(branch_functions)
importlib.reload(trunk_functions)


def create_tree(trunk_height, trunk_base, trunk_top, num_sect, axis_divs, 
                branch_size, branch_elevation_min, branch_elevation_max,
                max_num_leaves, min_leaf_radius, max_leaf_radius,
                num_intervals, recursion_depth_limit, layer_distribution_fn,
                length_distribution_fn, tree_name="default_tree", **kwargs):
    trunk = trunk_functions.create_trunk(trunk_height, trunk_base, trunk_top, num_sect, axis_divs, tree_name)

    interval_min = -trunk_height / 2 + 2
    interval_max = trunk_height / 2 - 0.2
    if num_intervals > 0:
        size = (interval_max - interval_min) / num_intervals
        max_num_branches = kwargs.get("max_num_branches", 3)
        concentration_min = kwargs.get("concentration_min", 0)
        concentration_max = kwargs.get("concentration_max", 1)
        for i in range(num_intervals):
            num_branches = layer_distribution_fn(maxValue=max_num_branches, total=num_intervals, 
                                                 concentration_min = concentration_min, concentration_max = concentration_max, 
                                                 x = i, roundToInt=True)
            if num_branches > 0:
                azimuth_interval_size = 360 / num_branches # for better distributed sampling
                for j in range(num_branches):
                    branch_height = random.uniform(interval_min + (size * i), interval_min + (size * (i+1)))

                    branch_length_min = trunk_functions.trunk_taper_function(trunk_height, trunk_base, trunk_top, branch_height)
                    # maximum is dependent on branch concentration
                    # Default: longest length at concentration_min, shortest_length at concentration max (for random layer distribution min->0, max->1)
                    bottom_branch_max = kwargs.get('bottom_length_max', 5)
                    top_branch_max = kwargs.get('top_length_max', 5)
                    distribution_height = branch_height + trunk_height / 2 # branch_height: [-trunk_height/2, trunk_height/2] --> convert to [0, trunk_height]
                    branch_length_max = branch_length_min + length_distribution_fn(initial_value=bottom_branch_max, end_value=top_branch_max,
                                                                                   concentration_min=concentration_min, concentration_max=concentration_max,
                                                                                   total=trunk_height, x=distribution_height)
                    branch_length = random.uniform(max(1, branch_length_min), max(1, branch_length_max))
                    azimuth_min = -180 + azimuth_interval_size * j
                    azimuth_max = -180 + azimuth_interval_size * (j + 1)
                    branch_functions.create_branch(trunk, trunk_height, branch_height, 
                                                   branch_size, branch_length, 
                                                   azimuth_min, azimuth_max, 
                                                   branch_elevation_min, branch_elevation_max, 
                                                   max_num_leaves, min_leaf_radius, max_leaf_radius,
                                                   recursion_depth_limit)