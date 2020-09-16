import bpy

"""

This is the cleaned-up fn, which should just have the useful fns
All fns, including non-useful ones, are in animations_bloated.py
I should move bezier creation fns to their own file.

To possibly change later: Objs in Blender have material slots and you can 
switch/keyframe which one is the active material. 
These materials go into the list obj.material_slots. So if one material is ever used,
then the material referenced by obj.material_slots[0] is also the active material.
Below, my fns mainly use obj.material_slots[0], but maybe I should replace these
with obj.active_material, to allow for objs with multiple materials. 
Also, the fn to delete materials may want to iterate through the list, or it may be that
deleting the active material (whether by using active_material, or the active material 
happens to be material_slot[0]) does not in any way give a new active material, even if 
there are materials in the other slots. These may get cleaned up on a Blender save/reopen.
The details of this might not matter so much, but if the scripts fail once I start ading multiple
materials per object, then the facts here stated are the likely culprit. 

__________________OLD NOTES BELOW THIS LINE_______________________

Warning: when setting some objects to animate along a path using the these fns,
sometimes you need to select one of the objs, go to the Object Constraints tab
on the right side, and click Animate Path; this is particularly the case if the 
curve/path was just created, using the relevant fns below.

Animating along a path can prove very powerful. With they keyframing offset method of that one video,
these keyfrmes can even be copied over, (as long as the constraint is also on?)

No matter, the best fns for animation follow just below.

A great way to animate is what I originally wanted:

Animate an empty, copy its keyframes to the first object in a series of objs to be animated,
using the copy keyframes fn below.
Select other objs, then shift+select first obj with keyframes, then copy them all using the same fn,
but this time run the offset fn (with the proper offset) right afterward.

Now my text is super animatable!

Also below are fns to create curves and then add the curve constraint with a ramped up offset.
I use ramped up offsets all the time, since it is the best and least boring to look at!


"""


def CopyAnimDataSelectedtoSelected():
    """Ensure obj with animation data to be copied is selected last
    so that it's the active object.
    To offset the keyframes, just run the OffsetKeyframesSelected() fn after this fn.
    
    Note: copying material animations is a matter of copying the material.
    
    """
    
    active_name = bpy.context.active_object.name
    
    objs = [o for o in bpy.context.selected_objects if o.name != active_name]
            
    for obj in objs:
             
        if bpy.data.objects[active_name].animation_data:     
        
            if obj.animation_data:
            
                obj.animation_data.action = bpy.data.objects[active_name].animation_data.action.copy()
            
            else:
            
                obj.animation_data_create()
                obj.animation_data.action = bpy.data.objects[active_name].animation_data.action.copy()
                
    
def CopyMaterialsSelectedtoSelected():
    """Ensure the obj with the material to be copied is the active object"""

    active = bpy.context.active_object
    
    objs = [o for o in bpy.context.selected_objects if o != active]
    
    for obj in objs:        
                  
        bpy.data.objects[obj.name].active_material = active.active_material.copy()
                               

def FollowSelectedPathtoSelected():        
    """Keyframe the constraint's offset to animate."""
    
    objs = [o for o in bpy.context.selected_objects]
    
    for obj in objs: #find the path obj before constraining anything to it
        
        if obj.type == 'CURVE':
                       
            curve_obj = obj

    for obj in objs:
        
        if curve_obj.name == obj.name:
            
            continue
        
        obj.constraints.new(type='FOLLOW_PATH')
        obj.constraints["Follow Path"].target = curve_obj
        obj.constraints["Follow Path"].use_fixed_location = True
        obj.constraints["Follow Path"].offset_factor = 1
        
                
def DeleteAllAnimationDataSelected():
        
    objs = [o for o in bpy.context.selected_objects]
    
    for obj in objs:

        if obj.animation_data:
            
            obj.animation_data_clear()
            
        """Material keyframes"""

        if obj.active_material: #first check obj has a material
            
            material_name = obj.active_material.name
    
            if bpy.data.materials[material_name].animation_data:
                
                bpy.data.materials[material_name].animation_data_clear()
                
            if bpy.data.materials[material_name].node_tree.animation_data:
                
                bpy.data.materials[material_name].node_tree.animation_data_clear()

                
def DeleteMaterialsSelected():
    """
    If a non-selected object has the same material, then it will not be deleted from that object. 
    If no other objects have the material, the material will be unaccessible once the Blender project is
    saved and quit. If you might want the material in the future, then be sure to assign it 
    to some other object before saving and quitting.
    """
    
    objs = [o for o in bpy.context.selected_objects]
    
    for obj in objs:
        
        obj.active_material = None
        
        
def DeleteConstraintSelected():
    
    objs = [o for o in bpy.context.selected_objects]
    
    for obj in objs:
        
        obj.constraints.clear()


def ResetDefaultsSelected(scale=1, rotate=0, is_upright_text=False, has_opac_mat=False):
    
    """This is useful in cases of user error of deleting keyframes when on an interpolation frame,
    so that whatever the interpolation value reads on that frame is now the non-animated value.
    It also applies to my opacity material. If the name's prefix has been changed then pass its name 
    in opac_mat_name when calling the function.
    """
    
    objs = [o for o in bpy.context.selected_objects]
        
    for obj in objs:
        
        obj.scale = [scale, scale, scale]
        
        if is_upright_text:
                  
            obj.rotation_euler[0] = rotate + 1.5707999467849731 #x-rotation, 90 deg rotation in radians; Blender converts to this value when rounding to 1.5708, but might as well be exact on our end
        
        else:
            obj.rotation_euler[0] = rotate #x-rotation
            
        obj.rotation_euler[1] = rotate #y-rotation
        obj.rotation_euler[2] = rotate #z-rotation
        
        """Related to Opacity material"""
        
        if has_opac_mat:
        
            if obj.active_material: #first check obj has a material
            
                material_name = obj.active_material.name
            
                #if material_name[:7] == opac_mat_name:
                        
                mat = bpy.data.materials[material_name].node_tree.nodes.get('Mix Shader')
                    
                if mat:
                        
                    mat.inputs[0].default_value = 1
                    
                    #bpy.data.materials[material_name].node_tree.nodes["Mix Shader"].inputs[0].default_value = 1

          
                
def OffsetKeyframesSelected(offset=10, rampup=False, absolute=None):
    
    objs = [o for o in bpy.context.selected_objects]
    
    num_selected = len(objs)

    for i,obj in enumerate(objs):
        
        
        """Calculate delta"""
        
        if not absolute and len(objs) != 1: #Relative offset of all selected objects, where first object's keyframes aren't moved
                    
            if rampup:
            
                delta = offset * i
            
            else:
            
                delta = 0
            
                for num in range(0, i):
                
                    delta += offset - (offset * ((num+1)/num_selected))
                    
        else: #If just one obj is selected, then we always want an absolute offset
            
            delta = offset
                    
        
        """Object keyframes"""
                
        if obj.animation_data:
                
            action = obj.animation_data.action

            for fcurve in action.fcurves:
            
                for keyframe in fcurve.keyframe_points:
                
                    keyframe.co[0] += delta
                    keyframe.handle_left[0] += delta
                    keyframe.handle_right[0] += delta

        
        """Material keyframes"""
        
        if obj.active_material: #first check obj has a material
            
            material_name = obj.active_material.name
            
            #If there is any animation data this should always be true
            if bpy.data.materials[material_name].animation_data:
                
                action = bpy.data.materials[material_name].animation_data.action
                    
                for fcurve in action.fcurves:
            
                    for keyframe in fcurve.keyframe_points:
                        
                        keyframe.co[0] += delta
                        keyframe.handle_left[0] += delta
                        keyframe.handle_right[0] += delta
                        
            #If there is any animation data with Use Nodes enabled, this should also always be true
            #Even if Use Nodes is not enabled, the material will have a node_tree so no need to check for it
            if bpy.data.materials[material_name].node_tree.animation_data:
                    
                action = bpy.data.materials[material_name].node_tree.animation_data.action
                    
                for fcurve in action.fcurves:
            
                    for keyframe in fcurve.keyframe_points:
                        
                        keyframe.co[0] += delta
                        keyframe.handle_left[0] += delta
                        keyframe.handle_right[0] += delta


def AddBacklightToSelected(offset_behind=0.75, brightness=100, light_cutoff_distance=0.6):
    """Adds powerful backlight just behind selected objects, sets its affective distance low,
    adds it to its own collection named after the first object and 'BLight'
    Tip: create an empty to control them as a group and lift them up slightly higher than the 
    objects they light to give a top light.
    
    """
        
    objs = [o for o in bpy.context.selected_objects]
        
    new_col = bpy.data.collections.new(name=objs[0].name + 'BLight') #create new collection in data
    bpy.context.scene.collection.children.link(new_col) #add new collection to the scene  
    
    for obj in objs:
        
        loc_x = obj.location[0]
        loc_y = obj.location[1] + offset_behind #Offset light from obj along y-axis
        loc_z = obj.location[2]
        
        new_name = obj.name + 'BLight'
        
        bpy.ops.object.light_add(type='POINT', location=(loc_x, loc_y, loc_z))
        
        
        bpy.context.active_object.name = new_name
        
        bpy.data.objects[new_name].data.energy = brightness
        bpy.data.objects[new_name].data.use_custom_distance = True
        bpy.data.objects[new_name].data.cutoff_distance = light_cutoff_distance
        
        obj_old_col = bpy.data.objects[new_name].users_collection #list of all collections the txt_obj is in, the main scene by default
        new_col.objects.link(bpy.data.objects[new_name]) #link txt_obj to new_col
        
        for ob in obj_old_col: #unlink from all previous collections
            
            ob.objects.unlink(bpy.data.objects[new_name])        


CopyAnimDataSelectedtoSelected()
CopyMaterialsSelectedtoSelected()
FollowSelectedPathtoSelected()


DeleteAllAnimationDataSelected()
DeleteMaterialsSelected()
DeleteConstraintSelected()



ResetDefaultsSelected(scale=1, rotate=0, opac_mat_name='Opacity')
OffsetKeyframesSelected(offset=-5, rampup=None, absolute=None)
AddBacklightToSelected(offset_behind=0.75, brightness=100, light_cutoff_distance=0.6)

                
"""With the above, I can now manually animate one character very well, even give it an animated material,
and then copy the material to the others using the copy materials fn above,
and then copy and appropriately offset its keyframes (including the ones of the material) to anything else!
"""          
       
"""
objects = bpy.data.objects
a = objects[obj.name]
b = objects[obj.name + 'BLight']
b.parent = a
"""

"""
    
bezier_obj = bpy.data.objects[bezier_name]
    
for ob in bpy.context.selected_objects: #Deselect any selected objects
            
    bpy.data.objects[ob.name].select_set(False)
            
bezier_obj.select_set(True) #Select bexier_obj                
bpy.context.view_layer.objects.active = bezier_obj #Sets the active object to be bezier_obj, needed below         
 

bpy.ops.curve.primitive_bezier_curve_add(radius=1, enter_editmode=False, location=(0, 0, 0))
bpy.context.active_object.name = bezier_name
"""

def OffsetKeyframes():
    """Original template I got online
    Works on selected. Offsets 2 frames. Not very useful as is, use fns above.
    """
    
    offset = 2 ## offset in frames
    noise = 0 ## add some offset variation (set to 0 to disable; 50 default)
    reset = False ## enable to align actions to frame 0


    #import bpy, random
    objs = [o for o in bpy.context.selected_objects if o.animation_data]


    for i,o in enumerate(objs):
        act = o.animation_data.action
        delta = offset * i
        delta += random.random() * noise
        if reset: delta = act.frame_range[0] * -1


        for fcu in act.fcurves:
            for k in fcu.keyframe_points:
                k.co[0] += delta
                k.handle_left[0] += delta
                k.handle_right[0] += delta


"""

print('NEW')

for action in bpy.data.actions:
    
    #name = action.name
    #action = bpy.data.actions["action_id"]
    for fcu in action.fcurves:
        print(fcu.data_path + " channel " + str(fcu.array_index))
        for keyframe in fcu.keyframe_points:
            print(keyframe.co) #coordinates x,y

"""


def RandomHelpfulBits():
    

    for action in bpy.data.actions:
        for fcurve in action.fcurves:
            for point in fcurve.keyframe_points:
                point.co.x -= 3.96
                
    # move everything to new position
    for action in bpy.data.actions:
        for fcurve in action.fcurves:
            for point in fcurve.keyframe_points:
                point.co.x -= theOffset
                # don't forget the keyframe's handles:
                point.handle_left.x -= theOffset
                point.handle_right.x -= theOffset
                    

    #import bpy, random
    objs = [o for o in bpy.context.selected_objects if o.animation_data]


    for i,o in enumerate(objs):
        act = o.animation_data.action
        delta = offset * i
        delta += random.random() * noise
        if reset: delta = act.frame_range[0] * -1


        for fcu in act.fcurves:
            for k in fcu.keyframe_points:
                k.co[0] += delta
                k.handle_left[0] += delta
                k.handle_right[0] += delta


"""


***************************************************************************************
The below fns were just trying to auomatically generate some good animations related to
scaling and rotation, but the main issue is the lack of ability to tweak animations without 
first deleting the keyframes, and then running the below fns again with new argument values. 

Much better is to just keyframe one lead very well and then copy those over to any other object 
with or without desired offsets, with help from the above fns. 

Basically,

IGNORE THE BELOW FNS!

I keep them in case I want a reference for more Blender API scripting.

***************************************************************************************


"""


def ScaleAnimationSelected(start_frame, end_frame, offset=10, bounce_perc=100, rampup=None):
    
    counter = 0
    
    num_selected = len(bpy.context.selected_objects)
    
    print('RESETTING******')
       
    for obj in bpy.context.selected_objects:
        
        if obj.type == 'CURVE':

            continue        
    
        for ob in bpy.context.selected_objects: #Deselect any selected objects
            
            bpy.data.objects[ob.name].select_set(False)
            
        if rampup == None:
            
            new_offset = offset * counter
            
        if rampup != None:
                        
            new_offset = offset
                        
            for num in range(0, counter):
                
                print('nump1', num+1, 'num_selected', num_selected, (num+1)/num_selected)                
                new_offset += offset - (offset * ((num+1)/num_selected))
                
            print('new_offset pre int', new_offset)
            new_offset = int(new_offset) #Int() needed since floats are not allowed as frame values
            print('new_offset', new_offset)
                
            
        obj.select_set(True) #Select obj                
        bpy.context.view_layer.objects.active = obj #Sets the active object to be obj, needed below         
      
        bpy.context.scene.frame_set(start_frame + new_offset)#Move to start_frame

        bpy.context.object.scale[0] = 0.01
        bpy.context.object.scale[1] = 0.01
        bpy.context.object.scale[2] = 0.01
    
        bpy.ops.anim.keyframe_insert_menu(type='Scaling')
                        
        """Put bounce at 95% of end_frame"""
        bounce_frame = int(end_frame * 0.95) #Int() needed since floats are not allowed as frame values
        bpy.context.scene.frame_set(bounce_frame + new_offset)#Move to bounce_frame
        
        bounce = bounce_perc/100
        
        bpy.context.object.scale[0] = bounce
        bpy.context.object.scale[1] = bounce
        bpy.context.object.scale[2] = bounce
        
        bpy.ops.anim.keyframe_insert_menu(type='Scaling')
        
        """End frame"""
        bpy.context.scene.frame_set(end_frame + new_offset)#Move to start_frame

        bpy.context.object.scale[0] = 1
        bpy.context.object.scale[1] = 1
        bpy.context.object.scale[2] = 1
        
        bpy.ops.anim.keyframe_insert_menu(type='Scaling')
        
        counter += 1


def ScaleAnimationSelectedImp(start_frame, start_hs_locs, end_frame, end_hs_locs, offset=10, rampup=None):
    """ScaleAnimationSelectedImp(start_frame, [lhandle[-30, 0.01], rhandle[30, 0.01]], endframe, 
    [lhandle[-7, 2.0],rhandle[7, 0.0]], offset, True)
    """
    
    counter = 0
    
    num_selected = len(bpy.context.selected_objects)
    
    x_startkey_offsetl = start_hs_locs[0][0]   
    x_startkey_offsetr = start_hs_locs[1][0]
    x_endkey_offsetl = end_hs_locs[0][0]
    x_endkey_offsetr = end_hs_locs[1][0]
      
    print('RESETTING******')
       
    for obj in bpy.context.selected_objects:
        
        if obj.type == 'CURVE':

            continue        
    
        for ob in bpy.context.selected_objects: #Deselect any selected objects
            
            bpy.data.objects[ob.name].select_set(False)
            
        if rampup == None:
            
            new_offset = offset * counter
            
        if rampup != None:
                        
            new_offset = 0 #Changed from offset
                        
            for num in range(0, counter):
                               
                new_offset += offset - (offset * ((num+1)/num_selected))
            
            new_offset = int(new_offset) #Int() needed since floats are not allowed as frame values
                            
        obj.select_set(True) #Select obj                
        bpy.context.view_layer.objects.active = obj #Sets the active object to be obj, needed below         
      
        bpy.context.scene.frame_set(start_frame + new_offset)#Move to start_frame

        bpy.context.object.scale[0] = 0.01
        bpy.context.object.scale[1] = 0.01
        bpy.context.object.scale[2] = 0.01
    
        bpy.ops.anim.keyframe_insert_menu(type='Scaling')
        
        #bpy.ops.graph.handle_type(type='FREE')

        
        final_fc_index = len(obj.animation_data.action.fcurves) - 1
        final_kf_index = len(obj.animation_data.action.fcurves[final_fc_index].keyframe_points) - 1
        

        start_hs_locs[0][0] = x_startkey_offsetl + start_frame + new_offset
        start_hs_locs[1][0] = x_startkey_offsetr + start_frame + new_offset
   
        
        for fcu in obj.animation_data.action.fcurves:
            
            if fcu.data_path != 'scale':
                
                print('cont1')
                
                continue
            
            for keyf in fcu.keyframe_points:
                
                if keyf.co[0] != start_frame + new_offset or keyf.co[1] != bpy.context.object.scale[0]: #Exact data needed because often the number entered becomes an approxiamte float
                    
                    print('cont2', keyf.co[0], keyf.co[1])
                    
                    continue
                
                keyf.handle_left_type = 'FREE'
                keyf.handle_right_type = 'FREE'                
                keyf.handle_left = start_hs_locs[0]
                keyf.handle_right = start_hs_locs[1]
                           
        """End frame"""
        bpy.context.scene.frame_set(end_frame + new_offset)#Move to start_frame

        bpy.context.object.scale[0] = 1
        bpy.context.object.scale[1] = 1
        bpy.context.object.scale[2] = 1
        
        bpy.ops.anim.keyframe_insert_menu(type='Scaling')
        
        #bpy.ops.graph.handle_type(type='FREE')

        final_fc_index = len(obj.animation_data.action.fcurves) - 1
        final_kf_index = len(obj.animation_data.action.fcurves[final_fc_index].keyframe_points) - 1
        

        end_hs_locs[0][0] = x_startkey_offsetl + end_frame + new_offset
        end_hs_locs[1][0] = x_startkey_offsetr + end_frame + new_offset
        
        for fcu in obj.animation_data.action.fcurves:
            
            if fcu.data_path != 'scale':
                
                continue
            
            for keyf in fcu.keyframe_points:
                
                if keyf.co[0] != end_frame + new_offset or keyf.co[1] != bpy.context.object.scale[0]: #Exact data needed because often the number entered becomes an approxiamte float
                    
                    continue
                
                keyf.handle_left_type = 'FREE'
                keyf.handle_right_type = 'FREE'                
                keyf.handle_left = end_hs_locs[0]
                keyf.handle_right = end_hs_locs[1]
                
                   
        
        """
        OLD
        for index in range(0, final_kf_index + 1):
            
            obj.animation_data.action.fcurves[final_fc_index].keyframe_points[final_kf_index].handle_left_type = 'FREE'
            obj.animation_data.action.fcurves[final_fc_index].keyframe_points[final_kf_index].handle_right_type = 'FREE'
        
            obj.animation_data.action.fcurves[final_fc_index].keyframe_points[index].handle_left = end_hs_locs[0]
            obj.animation_data.action.fcurves[final_fc_index].keyframe_points[index].handle_right = end_hs_locs[1]
        """
        
        counter += 1



def RotateAnimationSelected(rotate_times, start_frame, start_hs_locs, end_frame, end_hs_locs, offset=10, rampup=None):
    """ScaleAnimationSelectedImp(start_frame, [lhandle[-30, 0.01], rhandle[30, 0.01]], endframe, 
    [lhandle[-7, 2.0],rhandle[7, 0.0]], offset, True)
    """
    
    counter = 0
    
    num_selected = len(bpy.context.selected_objects)
    
    x_startkey_offsetl = start_hs_locs[0][0]   
    x_startkey_offsetr = start_hs_locs[1][0]
    x_endkey_offsetl = end_hs_locs[0][0]
    x_endkey_offsetr = end_hs_locs[1][0]
    
   
    
    """Euler conversions"""
    
    pi = 3.141592653589793
    rotate_times_euler = (pi * 2) * rotate_times
    
    #370 = (x / (2 * pi)) * 360
    
    #370/360 = x / (2 * pi)
    
    #370/360 * 2 * pi = x
    
    y_start_lhandle_euler = (start_hs_locs[0][1] / 360) * 2 * pi
    y_start_rhandle_euler = (start_hs_locs[1][1] / 360) * 2 * pi
    
    y_end_lhandle_euler = (end_hs_locs[0][1] / 360) * 2 * pi
    y_end_rhandle_euler = (end_hs_locs[1][1] / 360) * 2 * pi
    
    
    #degrees = (euler) / (2 * pi) ) * 360
    
    
      
    print('RESETTING******')
       
    for obj in bpy.context.selected_objects:
        
        if obj.type == 'CURVE':

            continue        
    
        for ob in bpy.context.selected_objects: #Deselect any selected objects
            
            bpy.data.objects[ob.name].select_set(False)
            
        if rampup == None:
            
            new_offset = offset * counter
            
        if rampup != None:
                        
            new_offset = 0 #Changed from offset
                        
            for num in range(0, counter):
                               
                new_offset += offset - (offset * ((num+1)/num_selected))
            
            new_offset = int(new_offset) #Int() needed since floats are not allowed as frame values
                            
        obj.select_set(True) #Select obj                
        bpy.context.view_layer.objects.active = obj #Sets the active object to be obj, needed below         
      
        bpy.context.scene.frame_set(start_frame + new_offset)#Move to start_frame
        
               
        bpy.context.object.rotation_euler[2] = 0    
        bpy.ops.anim.keyframe_insert_menu(type='Rotation')
        
        
        final_fc_index = len(obj.animation_data.action.fcurves) - 1
        final_kf_index = len(obj.animation_data.action.fcurves[final_fc_index].keyframe_points) - 1
        

        start_hs_locs[0][0] = x_startkey_offsetl + start_frame + new_offset
        start_hs_locs[1][0] = x_startkey_offsetr + start_frame + new_offset
   
        
        for fcu in obj.animation_data.action.fcurves:
            
            if fcu.data_path != 'rotation_euler':
                
                print('cont1')
                
                continue
            
            for keyf in fcu.keyframe_points:
                
                print(keyf.co, 'keyf.co cords')
                
                if keyf.co[0] != start_frame + new_offset or keyf.co[1] != bpy.context.object.rotation_euler[2]: #Exact data needed because often the number entered becomes an approxiamte float
                    
                    print('cont2', keyf.co[0], keyf.co[1])
                    
                    continue
                
                keyf.handle_left_type = 'FREE'
                keyf.handle_right_type = 'FREE'                
                keyf.handle_left = [start_hs_locs[0][0], y_start_lhandle_euler]
                keyf.handle_right = [start_hs_locs[1][0], y_start_rhandle_euler]
                
                print('lr handles 1', keyf.handle_left, keyf.handle_right)
                
                           
        """End frame"""
        bpy.context.scene.frame_set(end_frame + new_offset)#Move to start_frame
        
        print('endframe', end_frame + new_offset)

        """
        bpy.context.object.scale[0] = 1
        bpy.context.object.scale[1] = 1
        bpy.context.object.scale[2] = 1
        """
        #bpy.context.object.rotation_euler[2] = 360 * rotate_times
        
        #pi = 3.141592653589793
        #degrees = (euler) / (2 * pi) ) * 360
        #157.079632679
        bpy.context.object.rotation_euler[2] = rotate_times_euler
        bpy.ops.anim.keyframe_insert_menu(type='Rotation')
        
        print( 'result val', bpy.context.object.rotation_euler[2], 'rotate times', rotate_times, 'times 360', 360 * rotate_times)
        
        #bpy.ops.graph.handle_type(type='FREE')

        final_fc_index = len(obj.animation_data.action.fcurves) - 1
        final_kf_index = len(obj.animation_data.action.fcurves[final_fc_index].keyframe_points) - 1
        
        end_hs_locs[0][0] = x_endkey_offsetl + end_frame + new_offset
        end_hs_locs[1][0] = x_endkey_offsetr + end_frame + new_offset
        
        
        for fcu in obj.animation_data.action.fcurves:
            
            if fcu.data_path != 'rotation_euler':
                
                continue
            
            for keyf in fcu.keyframe_points:
                
                if keyf.co[0] != end_frame + new_offset or keyf.co[1] != bpy.context.object.rotation_euler[2]: #Exact data needed because often the number entered becomes an approxiamte float
                    
                    print('cont2', bpy.context.object.rotation_euler[2])
                    
                    continue
                
                print('made it', bpy.context.object.rotation_euler[2])
                
                keyf.handle_left_type = 'FREE'
                keyf.handle_right_type = 'FREE'                
                keyf.handle_left = [end_hs_locs[0][0], y_end_lhandle_euler] #Wow! SO handles are placed acording to euler to degrees conversions from backend to frontend!
                #keyf.handle_left = [end_hs_locs[0][0], (pi * 2) * rotate_times] #Wow! SO handles are placed acording to euler to degrees conversions from backend to frontend!
                keyf.handle_right = [end_hs_locs[1][0], y_end_rhandle_euler]
                
                print('lr handles 2', keyf.handle_left, keyf.handle_right)
                
                
        print('final val', bpy.context.object.rotation_euler[2], 'for ', obj.name)
        
        """
        OLD
        for index in range(0, final_kf_index + 1):
            
            obj.animation_data.action.fcurves[final_fc_index].keyframe_points[final_kf_index].handle_left_type = 'FREE'
            obj.animation_data.action.fcurves[final_fc_index].keyframe_points[final_kf_index].handle_right_type = 'FREE'
        
            obj.animation_data.action.fcurves[final_fc_index].keyframe_points[index].handle_left = end_hs_locs[0]
            obj.animation_data.action.fcurves[final_fc_index].keyframe_points[index].handle_right = end_hs_locs[1]
        """
        
        counter += 1



#ScaleAnimationSelectedImp(start_frame, [lhandle[-30, 0.01], rhandle[30, 0.01]], endframe, [lhandle[-7, 2.0],rhandle[7, 0.0]], offset, True)
#ScaleAnimationSelectedImp(1, [[-30, 0.01], [120, 0]], 90, [[-20, 4.0],[7, 0.0]], 10, True)#This should approx match the below
#ScaleAnimationSelected(1, 90, 10, 125, True)


#RotateAnimationSelected(25, 1, [[-30, 0], [60, 0]], 90, [[-10, (360 * 25) + 25],[30, (360 * 25)]], 10, True)
#ChangeSelectedPathtoFollowSelectedPath(10, True)
#DeleteConstraintSelected()



                