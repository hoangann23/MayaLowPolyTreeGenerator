import maya.cmds as cmds
import maya.api.OpenMaya as om
import random

def add_leaves(branch, position, max_num_leaves=5, min_leaf_radius=0.05, max_leaf_radius=0.25):
    num_leaves = random.randint(0, max_num_leaves)
    for i in range(num_leaves):
        leaf_radius = random.uniform(min_leaf_radius, max_leaf_radius)
        leaf = cmds.polySphere(name="leaf#", radius=leaf_radius)[0]
        leaf_position = position + om.MVector(random.uniform(leaf_radius, leaf_radius + 0.005),
                                              random.uniform(leaf_radius, leaf_radius + 0.005),
                                              random.uniform(leaf_radius, leaf_radius + 0.005))
        cmds.xform(leaf, translation=(leaf_position.x, leaf_position.y, leaf_position.z))
        cmds.parent(leaf, branch)
