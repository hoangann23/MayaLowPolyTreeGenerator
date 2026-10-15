import sys
sys.path.append("/Users/ahluong/Documents/maya/projects/PersonalProjects/scripts")

import TreeGenerator
import tree_globals
import tree_generator_ui
import distribution_functions
import importlib
importlib.reload(tree_globals)
importlib.reload(TreeGenerator)
importlib.reload(tree_generator_ui)
importlib.reload(distribution_functions)

TreeGenerator.create_tree(tree_globals.trunk_height, 
            tree_globals.trunk_base, 
            tree_globals.trunk_top, 
            tree_globals.num_sect,
            tree_globals.trunk_axis_divs, 
            tree_globals.branch_size, 
            tree_globals.branch_elevation_min,
            tree_globals.branch_elevation_max,
            5,
            0.05,
            0.25,
            tree_globals.num_intervals, 
            tree_globals.recursion_depth_limit,
            distribution_functions.randInt,
            distribution_functions.linear)
tree_generator_ui.show_ui()
