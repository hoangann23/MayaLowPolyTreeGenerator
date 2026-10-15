import maya.cmds as cmds
import TreeGenerator
import tree_globals
import distribution_functions

window_name = "Procedural Tree Generator"
def close_window_if_open():
    if cmds.window(window_name, exists=True):
            cmds.deleteUI(window_name)

def show_ui():
    close_window_if_open()

    window = cmds.window(window_name, title="Procedural Tree Generator", sizeable=True, widthHeight=(1500,600))

    cmds.columnLayout(adjustableColumn=True, rowSpacing=8)

    cmds.rowLayout(
         numberOfColumns=3,
         adjustableColumn=3,
         columnWidth3=(400,400,400),
         columnAttach=[(1, "both", 8),
                       (2, "both", 8),
                       (3, "both", 8)])
    
    cmds.columnLayout(adjustableColumn=True, rowSpacing=8)
    tree_name_prompt = cmds.textFieldGrp(label="Tree name: ", text = "default_tree")
    trunk_height_prompt = cmds.floatSliderGrp(label="Trunk Height", field=True, minValue=0.01, maxValue=100, value=tree_globals.trunk_height)
    trunk_base_size_prompt = cmds.floatSliderGrp(label="Trunk Base Size", field=True, minValue=0.01, maxValue=100, value=tree_globals.trunk_base)
    trunk_top_size_prompt = cmds.floatSliderGrp(label="Trunk Top Size", field=True, minValue=0.01, maxValue=100, value=tree_globals.trunk_top)
    trunk_axis_divs_prompt = cmds.intSliderGrp(label="Trunk Axis Subdivisions", field=True, minValue=3, maxValue=100, value=tree_globals.trunk_axis_divs)
    cmds.setParent("..")

    cmds.columnLayout(adjustableColumn=True, rowSpacing=8)
    branch_size_prompt = cmds.floatSliderGrp(label="Base Branch Thickness", field=True, minValue=0.01, maxValue=100, value=tree_globals.branch_size)
    branch_layers_prompt = cmds.intSliderGrp(label="Number of Branch Layers", field=True, minValue=0, maxValue=100, value=tree_globals.num_intervals)
    max_num_branches_prompt = cmds.intSliderGrp(label="Max Num Branches Per Layer", field=True, minValue = 0, maxValue=100, value=tree_globals.max_num_branches)
    branch_elevation_min_prompt = cmds.floatSliderGrp(label="Min Branch Elevation Angle", field=True, minValue = -180, maxValue = 180, value=tree_globals.branch_elevation_min)
    branch_elevation_max_prompt = cmds.floatSliderGrp(label="Max Branch Elevation Angle", field=True, minValue = -180, maxValue = 180, value=tree_globals.branch_elevation_max)
    recursion_limit_prompt = cmds.intSliderGrp(label="Branch Recursion Limit", field=True, minValue=0, maxValue=100, value=tree_globals.recursion_depth_limit)
    cmds.setParent("..")

    cmds.columnLayout(adjustableColumn=True, rowSpacing=8)
    bottom_length_max_prompt = cmds.floatSliderGrp(label="Max Bottom Branch Length", field=True, minValue=0, maxValue=100,value=5)
    top_length_max_prompt = cmds.floatSliderGrp(label="Max Top Branch Length", field=True, minValue=0, maxValue=100, value=5)
    num_leaves_prompt = cmds.intSliderGrp(label="Max Leaves Per Branch", field=True, minValue=0, maxValue=10, value=5)
    min_leaf_radius_prompt = cmds.floatSliderGrp(label="Min Leaf Radius", field=True, minValue=0.01, maxValue=1, value=0.05, step = 0.01)
    max_leaf_radius_prompt = cmds.floatSliderGrp(label="Max Leaf Radius", field=True, minValue=0.01, maxValue=1, value=0.25, step=0.01)
    distribution_options = ["Random", "Concentrated"]
    branch_distribution_menu = cmds.optionMenu(label="Branch Layer Distribution")
    for option in distribution_options:
         cmds.menuItem(label=option, parent=branch_distribution_menu)
    dist_functions = {"Random" : distribution_functions.randInt,
                      "Concentrated" : distribution_functions.sin}
    concentration_min_slider = cmds.floatSliderGrp(label="Min Concentration Height", field=True, minValue=-1, maxValue=1, value = 0.25, step = 0.01, visible=False)
    concentration_max_slider = cmds.floatSliderGrp(label="Max Concentration Height", field=True, minValue=0, maxValue=1, value = 0.5, step = 0.01, visible=False)
    cmds.setParent("..")

    cmds.setParent("..")
    
    

    def on_branch_distribution_change(*args):
        distribution = cmds.optionMenu(branch_distribution_menu, query=True, value=True)
        if distribution == "Concentrated":
            cmds.floatSliderGrp(concentration_min_slider, edit=True, visible=True)
            cmds.floatSliderGrp(concentration_max_slider, edit=True, visible=True)
        else:
            cmds.floatSliderGrp(concentration_min_slider, edit=True, visible=False, value=0.0)
            cmds.floatSliderGrp(concentration_max_slider, edit=True, visible=False, value=1.0)

    def on_click(*args):
         tree_name = cmds.textFieldGrp(tree_name_prompt, query=True, text=True)
         trunk_height = cmds.floatSliderGrp(trunk_height_prompt, query=True, value=True)
         trunk_base_size = cmds.floatSliderGrp(trunk_base_size_prompt, query=True, value=True)
         trunk_top_size = cmds.floatSliderGrp(trunk_top_size_prompt, query=True, value=True)
         trunk_axis_divs = cmds.intSliderGrp(trunk_axis_divs_prompt, query=True, value=True)
         branch_size = cmds.floatSliderGrp(branch_size_prompt, query=True, value=True)
         num_intervals = cmds.intSliderGrp(branch_layers_prompt, query=True, value=True)
         max_num_branches = cmds.intSliderGrp(max_num_branches_prompt, query=True, value=True)
         branch_elevation_min = cmds.floatSliderGrp(branch_elevation_min_prompt, query=True, value=True)
         branch_elevation_max = cmds.floatSliderGrp(branch_elevation_max_prompt, query=True, value=True)
         recursion_limit = cmds.intSliderGrp(recursion_limit_prompt, query=True, value=True)
         
         branch_distribution_option = cmds.optionMenu(branch_distribution_menu, query=True, value=True)
         branch_distribution_fn = dist_functions[branch_distribution_option]
         concentration_min = cmds.floatSliderGrp(concentration_min_slider, query=True, value=True)
         concentration_max = cmds.floatSliderGrp(concentration_max_slider, query=True, value=True)

         bottom_length_max = cmds.floatSliderGrp(bottom_length_max_prompt, query=True, value=True)
         top_length_max = cmds.floatSliderGrp(top_length_max_prompt, query=True, value=True)

         num_leaves = cmds.intSliderGrp(num_leaves_prompt, query=True, value=True)
         min_leaf_radius = cmds.floatSliderGrp(min_leaf_radius_prompt, query=True, value=True)
         max_leaf_radius = cmds.floatSliderGrp(max_leaf_radius_prompt, query=True, value=True)

         if branch_elevation_max < branch_elevation_min:
            cmds.warning("The maximum branch elevation must be greater than the minimum branch elevation")
            return
         if branch_distribution_option == "Concentrated" and concentration_max < concentration_min:
            cmds.warning("The concentration max must be greater than the concentration min")
            return

         TreeGenerator.create_tree(trunk_height, 
            trunk_base_size, 
            trunk_top_size,
            # since the taper is linear, num_sects is redundant (tapering two edge loops will give the same result as tapering 5 edge loops) - will still include for learnings
            tree_globals.num_sect, 
            trunk_axis_divs,
            branch_size,
            branch_elevation_min,
            branch_elevation_max,
            num_leaves,
            min_leaf_radius,
            max_leaf_radius,
            num_intervals,
            recursion_limit,
            branch_distribution_fn,
            distribution_functions.linear,
            tree_name,
            max_num_branches = max_num_branches,
            concentration_min = concentration_min,
            concentration_max = concentration_max,
            bottom_length_max = bottom_length_max,
            top_length_max = top_length_max)
    cmds.optionMenu(branch_distribution_menu, edit=True, changeCommand=on_branch_distribution_change)
    cmds.button(label="Generate Tree", command = on_click)

    cmds.showWindow()

    # Register a scriptJob to close this window when a new scene is opened
    # We use uiDeleted to clean up the scriptJob itself when the window closes manually
    job_num = cmds.scriptJob(
        event=["NewSceneOpened", close_window_if_open],
        killWithScene = True
    )


def clean_up_job(job_num):
    if cmds.scriptJob(exists=job_num):
        cmds.scriptJob(kill=job_num, force=True)
