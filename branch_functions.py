import sys
sys.path.append("/Users/ahluong/Documents/maya/projects/PersonalProjects/scripts")

import maya.cmds as cmds
import maya.api.OpenMaya as om
import random
import math
import tree_globals
import leaves_functions
import importlib

importlib.reload(leaves_functions)

def midpoint(point1, point2):
    direction = point2 - point1
    return point1 + (0.5*direction)

def connect_two_points(point1, point2, base_size=tree_globals.branch_size, top_size=tree_globals.branch_size):
    if point1 == point2:
        cmds.warning("Cannot bridge the same point")
        return
        
    # create a cube and scale it in the y direction then rotate it to the correct orientation
    direction = point2 - point1
    length = direction.length()
    if length <= 0.0001:
        cmds.warning("Cannot bridge points that are too close together")
        return
    mid = midpoint(point1, point2)
    cube = cmds.polyCube(name="branch#")[0]
    
    # rotate the cube's y-axis to point along direction
    object_axis = om.MVector(0.0, 1.0, 0.0)
    rot_quat = om.MQuaternion(object_axis, direction) # quarternion rotation current direction and target
    euler_rot = rot_quat.asEulerRotation()
    rot_deg = [om.MAngle(euler_rot.x).asDegrees(), om.MAngle(euler_rot.y).asDegrees(), om.MAngle(euler_rot.z).asDegrees()]
    
    cmds.xform(cube, worldSpace=True, translation=(mid.x, mid.y, mid.z), scale=(base_size, length, base_size), rotation=rot_deg)
    
    
    # scale the faces at point1 and point2
    face = f"{cube}.f[1]"
    cmds.select(face)
    cmds.xform(absolute=True, scale=(top_size, top_size, top_size))
    return cube

# create a branch that starts at a specified height along the trunk
def create_base_branch(trunk, height, min_height,
                        branch_length, branch_size, 
                        azimuth_min, azimuth_max, 
                        elevation_min, elevation_max, 
                        max_num_leaves, min_leaf_radius, max_leaf_radius,
                        recursion_depth_limit):
    point1 = om.MVector(0, height, 0)
    azimuth = random.uniform(azimuth_min, azimuth_max) # the angle the branch is rotated around the trunk (degrees)
    elevation = random.uniform(elevation_min, elevation_max) # the angle of the branch's elevation (degrees)
    dir = om.MVector(
            math.cos(math.radians(elevation)) * math.cos(math.radians(azimuth)),
            math.sin(math.radians(elevation)),
            math.cos(math.radians(elevation)) * math.sin(math.radians(azimuth)))
    point2 = point1 + (branch_length * dir.normalize())
    if point2.y < min_height:
        point2.y = min_height
    # taper size should be determined by child starting position (if there is a child)
    # the closer to the base, the more tapered taper(0.3) = 0.25
    # the closer to the end, the less tapered taper(0.8) = 0.5
    t, child_point = get_child_base_point(point1, point2)
    taper_size = 0.25
    if recursion_depth_limit >= 1:
        taper_size = 0.10 + 0.5 * t
    branch = connect_two_points(point1, point2, branch_size, taper_size)
    leaves_functions.add_leaves(branch, point2, max_num_leaves, min_leaf_radius, max_leaf_radius)
    cmds.parent(branch, trunk)
    return point1, point2, child_point, branch, azimuth

def get_child_base_point(point1, point2):
    direction = point2 - point1
    t = random.uniform(0.3, 0.8)
    child_base_point = point1 + t * direction
    return t, child_base_point
    
# the recursive branching function
def create_child_branch(point1, point2, child_base_point, parent_branch, 
                        azimuth_min, azimuth_max, 
                        elevation_min, elevation_max, 
                        max_num_leaves, min_leaf_radius, max_leaf_radius,
                        base_size, depth = 1, depth_limit = 3):
    if depth > depth_limit:
        return
    parent_length = (point2 - point1).length()
    branch_length = random.uniform(0.3 * parent_length, 0.7 * parent_length)
    azimuth = random.uniform(azimuth_min, azimuth_max) # the angle the branch is rotated around the trunk (degrees)
    # the next branch should never point behaind the parent branch (maybe add the option to do this later)
    next_azimuth_min = azimuth - 90
    next_azimuth_max = azimuth + 90
    elevation = random.uniform(elevation_min, elevation_max) # the angle of the branch's elevation (degrees)
    dir = om.MVector(
            math.cos(math.radians(elevation)) * math.cos(math.radians(azimuth)),
            math.sin(math.radians(elevation)),
            math.cos(math.radians(elevation)) * math.sin(math.radians(azimuth)))
    child_end_point = child_base_point + (branch_length * dir.normalize())
    t, child_point = get_child_base_point(child_base_point, child_end_point)
    taper_size = 0.25
    if depth < depth_limit - 1:
        taper_size = 0.10 + 0.5 * t
    
    current_branch = connect_two_points(child_base_point, child_end_point, base_size, taper_size)
    leaves_functions.add_leaves(current_branch, child_end_point, max_num_leaves, min_leaf_radius, max_leaf_radius)
    cmds.parent(current_branch, parent_branch)
    create_child_branch(child_base_point, child_end_point, child_point, 
                        current_branch, next_azimuth_min, next_azimuth_max, 
                        elevation_min, elevation_max, 
                        max_num_leaves, min_leaf_radius, max_leaf_radius,
                        taper_size * base_size, depth + 1, depth_limit)

def create_branch(trunk, trunk_height, 
                  branch_height, branch_size, branch_length, 
                  azimuth_min, azimuth_max, 
                  elevation_min, elevation_max, 
                  max_num_leaves, min_leaf_radius, max_leaf_radius,
                  recursion_depth_limit = 3):
    point1, point2, child_point, base_branch, azimuth = create_base_branch(trunk, branch_height, -trunk_height/2 + 2, 
                                                                           branch_length, branch_size, 
                                                                           azimuth_min, azimuth_max, 
                                                                           elevation_min, elevation_max, 
                                                                           max_num_leaves, min_leaf_radius, max_leaf_radius,
                                                                           recursion_depth_limit)
    if recursion_depth_limit >= 1:
        create_child_branch(point1, point2, child_point, 
                            base_branch, azimuth - 90, azimuth + 90, 
                            elevation_min, elevation_max, 
                            max_num_leaves, min_leaf_radius, max_leaf_radius,
                            branch_size / 2, 1, recursion_depth_limit)