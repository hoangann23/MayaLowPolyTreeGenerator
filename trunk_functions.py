import maya.cmds as cmds

def create_trunk(trunk_height, base_thickness, top_thickness, num_sections, axis_divs, trunk_name="trunk"):
    if num_sections <= 0:
        cmds.warning("trunk needs at least 1 section")
        return
    # create a cylinder and subdivide its height with num_sections
    trunk = cmds.polyCylinder(name=trunk_name, sx=axis_divs, sy=num_sections, radius=base_thickness, height=trunk_height)[0]

    slope = (top_thickness - base_thickness) / num_sections # rate of change of the trunk thickness by section
    base_horizontal_index = 0

    # scale the top edge of each section linearly 
    for i in range(1, num_sections):
        edge_scale = base_thickness + (slope * i)
        # Calculate a single edge index that rests on the horizontal loop
        target_edge_index = base_horizontal_index + (i * axis_divs)
        single_edge = f"{trunk}.e[{target_edge_index}]"
        cmds.select(single_edge)
        cmds.polySelectSp(loop=True)
        cmds.xform(absolute=True, scale=(edge_scale,1,edge_scale))


    edge_scale = base_thickness + (slope * num_sections)
    # Calculate a single edge index that rests on the horizontal loop
    target_edge_index = base_horizontal_index + (num_sections * axis_divs)
    single_edge = f"{trunk}.e[{target_edge_index}:{target_edge_index+axis_divs-1}]"
    cmds.select(single_edge)
    cmds.xform(absolute=True, scale=(edge_scale,1,edge_scale))
    return trunk

# return the thickness of the trunk at specified height
def trunk_taper_function(trunk_height, base_thickness, top_thickness, height):
    slope = (top_thickness - base_thickness) / trunk_height
    intersect = (top_thickness + base_thickness) / 2
    scale = slope * height + intersect
    return scale