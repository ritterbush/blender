bl_info = {
    "name": "Animations",
    "author": "Paul Ritterbush",
    "version": (1, 0),
    "blender": (2, 80, 2),
    "location": "View3D > Sidebar > Animations Tab",
    "description": "My best animation helpers",
    "warning": "",
    "wiki_url": "",
    "category": "Object",
}

import bpy


#put fns to call here


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
        
        #assert (curve_obj.name is not None), "You need to select a path!"
        
        try:
            if curve_obj.name == obj.name:
            
                continue
            
            obj.constraints.new(type='FOLLOW_PATH')
            obj.constraints["Follow Path"].target = curve_obj
            obj.constraints["Follow Path"].use_fixed_location = True
            obj.constraints["Follow Path"].offset_factor = 1
        except:
            
            print('Error: Path object not found! Make sure to select a path object and try again.')

                
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
        
        
def DeleteFollowPathSelected():
    
    objs = [o for o in bpy.context.selected_objects]
    
    for obj in objs:
                        
        constraints = [con for con in obj.constraints if con.type == 'FOLLOW_PATH']

        for con in constraints:
                
            obj.constraints.remove(con) 
        
        
      

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
                mat = bpy.data.materials[material_name].node_tree.nodes.get('Mix Shader')
                    
                if mat:
                        
                    mat.inputs[0].default_value = 1
                    
          
                
def OffsetKeyframesSelected(offset=10, rampup=False, absolute=False):
    
    objs = [o for o in bpy.context.selected_objects]
    
    num_selected = len(objs)

    for i,obj in enumerate(objs):
        
        
        """Calculate delta"""
        
        if not absolute and len(objs) != 1: #Relative offset of all selected objects, where first object's keyframes aren't moved
                    
            if rampup:
            
                delta = 0
            
                for num in range(0, i):
                
                    delta += offset - (offset * ((num+1)/num_selected))
            
            
            else:
            
                delta = offset * i
                    
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
                        
                        
                
def OffsetSetKeyframesSelected(offset=10, rampup=False, absolute=False):
    
    objs_a = [o for o in bpy.context.selected_objects]
    
    """Get subset according to naming conventions"""
    
    i = 1
    objs = []
    #sub_objs = []
    
    while i < 1000:
        
        sub_objs = []
        
        for obj in objs_a:
        
    
            if '00' + str(i) in obj.name and i < 10:
            
                sub_objs += [obj]
            
        
            if '0' + str(i) in obj.name and i < 100 and i > 9:
            
                sub_objs += [obj]
            
            if str(i) in obj.name and i < 1000 and i > 99:
            
                sub_objs += [obj]
            
        if sub_objs:
            objs += [sub_objs]         
            
        i += 1
            
    
    print(objs, 'objs w subset')
    
    num_selected = len(objs)
    
    print('len objs', num_selected)
    

    for i,obj in enumerate(objs):
        
        
        """Calculate delta"""
        
        
        if not absolute and len(objs) != 1: #Relative offset of all selected objects, where first object's keyframes aren't moved
                    
            if rampup:
            

                delta = 0
            
                for num in range(0, i):
                
                    delta += offset - (offset * ((num+1)/num_selected))            
            else:
            
                delta = offset * i
                    
        else: #If just one obj is selected, then we always want an absolute offset
            
            delta = offset
                    
                    
        for sub_obj in obj:            
                    
        
            """Object keyframes"""
        

            
            
                
            if sub_obj.animation_data:
                
                action = sub_obj.animation_data.action

                for fcurve in action.fcurves:
            
                    for keyframe in fcurve.keyframe_points:
                
                        keyframe.co[0] += delta
                        keyframe.handle_left[0] += delta
                        keyframe.handle_right[0] += delta

        
            """Material keyframes"""
        
        

        
            if sub_obj.active_material: #first check obj has a material
            
                material_name = sub_obj.active_material.name
            
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



        
def hey():
    
    bpy.ops.mesh.primitive_sphere_add()

"""
CopyAnimDataSelectedtoSelected()
CopyMaterialsSelectedtoSelected()
FollowSelectedPathtoSelected()
DeleteAllAnimationDataSelected()
DeleteMaterialsSelected()
DeleteConstraintSelected()
ResetDefaultsSelected(scale=1, rotate=0, is_upright_text=False, opac_mat_name='Opacity')
OffsetKeyframesSelected(offset=-5, rampup=None, absolute=None)
AddBacklightToSelected(offset_behind=0.75, brightness=100, light_cutoff_distance=0.6)
"""


class Animations_PT_Panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Animations"
    bl_idname = "OBJECT_PT_Animations"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    #bl_context = "object"
    bl_category = "Animations" #Name in UI Panel

    def draw(self, context):
        
        layout = self.layout
        #row = layout.row()
        #row.label(text="Add an object", icon='SPHERE')
        #row = layout.row()
        #row.operator("mesh.primitive_cube_add", icon='CUBE')
        #row = layout.row()
        #row.label(text="Add an object", icon='SPHERE')
        #row.operator("wm.hey", icon='CUBE')        
        row = layout.row()
        row.operator("wm.copyanimop") #From WM_OT_copyanimOP
        #col = row.column(align=True)
        #row = layout.row()
        #col.operator("wm.copyanimop", icon="RESTRICT_SELECT_OFF", text="")
        #row.operator("wm.copyanimop", icon="RESTRICT_SELECT_OFF", text="")
        row = layout.row()
        row.operator("wm.copymatop")
        #col = row.column(align=True)
        row = layout.row()
        row.operator("wm.followpathop")
        #col = row.column(align=True)
        row = layout.row()
        row.operator("wm.deleteanimop")
        row = layout.row()
        row.operator("wm.deletematop")
        row = layout.row()
        row.operator("wm.deletefollowpathop")
        row = layout.row()
        row.operator("wm.resetdefaultsop")
        row = layout.row()
        row.operator("wm.offsetanimop")
        row = layout.row()
        row.operator("wm.offsetsetanimop")
        
        
        
                
        
class WM_OT_CopyAnim(bpy.types.Operator):
    """Copies (non-mterial) animation keyframes to selected from active/last selected"""
    bl_label = "Copy Animations"
    bl_idname = "wm.copyanimop" 
    

    #text = bpy.props.StringProperty(name="Copy Animation Keyframes", default='')
    #radius = bpy.props.FloatProperty(name="Enter radius:", default=1)
    #amount = bpy.props.IntProperty(name="Enter amount:", default=1)
    

    """
    def invoke(self, context, event):
        #Popup a dialog the user can interact with.
        #wm = context.window_manager
        return context.window_manager.invoke_props_dialog(self)
    """
    
    """
    def draw(self,context):
        layout = self.layout
        layout.prop(self,"text", icon="QUESTION")
        #row = layout.row()
        layout.separator()
        layout.prop(self,"radius")
        layout.separator()
        layout.prop(self,"amount")
        box = layout.box() 
    """
        
    def execute(self, context):
        
        #radius = self.radius
        #amount = self.amount
        
        #bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, enter_editmode=False, location=(0, 0, 0))
        CopyAnimDataSelectedtoSelected()
        
        return {'FINISHED'}
    
        
class WM_OT_CopyMat(bpy.types.Operator):
    """Copies active materials to selected from active/last selected"""
    bl_label = "Copy Materials"
    bl_idname = "wm.copymatop" 
    

    #text = bpy.props.StringProperty(name="Copy Animation Keyframes", default='')
    #radius = bpy.props.FloatProperty(name="Enter radius:", default=1)
    #amount = bpy.props.IntProperty(name="Enter amount:", default=1)
    

    """
    def invoke(self, context, event):
        #Popup a dialog the user can interact with.
        #wm = context.window_manager
        return context.window_manager.invoke_props_dialog(self)
    
    """
    
    """
    def draw(self,context):
        layout = self.layout
        layout.prop(self,"text", icon="QUESTION")
        #row = layout.row()
        layout.separator()
        layout.prop(self,"radius")
        layout.separator()
        layout.prop(self,"amount")
        box = layout.box() 
    """
        
    def execute(self, context):
        
        #radius = self.radius
        #amount = self.amount
        
        #bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, enter_editmode=False, location=(0, 0, 0))
        CopyMaterialsSelectedtoSelected()
        
        return {'FINISHED'}
    
class WM_OT_FollowPath(bpy.types.Operator):
    """Selected follow the path that is selected"""
    
    bl_label = "Follow Path"
    bl_idname = "wm.followpathop" 
        
    def execute(self, context):

        FollowSelectedPathtoSelected()
        
        return {'FINISHED'}



class WM_OT_DeleteAnim(bpy.types.Operator):
    """Deletes all animation data from selected, including material animation data"""
    
    bl_label = "Delete Animations"
    bl_idname = "wm.deleteanimop" 
        
    def execute(self, context):

        DeleteAllAnimationDataSelected()
        
        return {'FINISHED'}
    
class WM_OT_DeleteMat(bpy.types.Operator):
    """Deletes materials from selected"""
    
    bl_label = "Delete Materials"
    bl_idname = "wm.deletematop" 
        
    def execute(self, context):

        DeleteMaterialsSelected()

        return {'FINISHED'}
    
class WM_OT_DeleteFollowPath(bpy.types.Operator):
    """Deletes all Follow Path constraints from selected."""
    
    bl_label = "Delete Follow Path"
    bl_idname = "wm.deletefollowpathop" 
        
    def execute(self, context):

        DeleteFollowPathSelected()
        
        return {'FINISHED'}
    
        
class WM_OT_ResetDefaults(bpy.types.Operator):
    """Resets the very selective defaults listed here\nTo do!!: Test Opacity material"""
    
    bl_label = "Reset Defaults"
    bl_idname = "wm.resetdefaultsop" 
    
    #text = bpy.props.StringProperty(name="Copy Animation Keyframes", default='')
    scale: bpy.props.FloatProperty(name="Enter Scale:", default=1)
    rotate: bpy.props.FloatProperty(name="Enter Rotation:", default=0)
    is_upright_text: bpy.props.BoolProperty(name="Is upright text", default=False)
    has_opac_mat: bpy.props.BoolProperty(name="Uses my Opacity material", default=False)   

    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)
    
    
    def execute(self, context):
        
        scale = self.scale
        rotate = self.rotate
        is_upright_text = self.is_upright_text
        has_opac_mat =  self.has_opac_mat

        ResetDefaultsSelected(scale, rotate, is_upright_text, has_opac_mat)
        
        return {'FINISHED'}       
    

class WM_OT_OffsetAnim(bpy.types.Operator):
    """Offsets all keyframes. Choose between absolute for each obj individually vs. relative to selected objects.\nRampup makes the speed of the animation ramp up toward the end. Negative values work too"""
    
    bl_label = "Offset Animations"
    bl_idname = "wm.offsetanimop" 
    
    #text = bpy.props.StringProperty(name="Copy Animation Keyframes", default='')
    #scale = bpy.props.FloatProperty(name="Enter Scale:", default=1)
    offset: bpy.props.IntProperty(name="Offset", default=10)
    rampup: bpy.props.BoolProperty(name="Use rampup", default=False)
    absolute: bpy.props.BoolProperty(name="Absolute", default=False)   

    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)
    
    
    def execute(self, context):
        
        offset = self.offset
        rampup = self.rampup
        absolute = self.absolute

        OffsetKeyframesSelected(offset, rampup, absolute)
        
        return {'FINISHED'}
           

class WM_OT_OffsetSetAnim(bpy.types.Operator):
    """Offsets all keyframes. Choose between absolute for each obj individually vs. relative to selected objects.\nRampup makes the speed of the animation ramp up toward the end. Negative values work too"""
    
    bl_label = "Offset Set Animations"
    bl_idname = "wm.offsetsetanimop" 
    
    #text = bpy.props.StringProperty(name="Copy Animation Keyframes", default='')
    #scale = bpy.props.FloatProperty(name="Enter Scale:", default=1)
    offset: bpy.props.IntProperty(name="Offset", default=10)
    rampup: bpy.props.BoolProperty(name="Use rampup", default=False)
    absolute: bpy.props.BoolProperty(name="Absolute", default=False)   

    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)
    
    
    def execute(self, context):
        
        offset = self.offset
        rampup = self.rampup
        absolute = self.absolute

        OffsetSetKeyframesSelected(offset, rampup, absolute)
        
        return {'FINISHED'}
               

classes = (
    Animations_PT_Panel, 
    WM_OT_CopyAnim, 
    WM_OT_CopyMat, 
    WM_OT_FollowPath, 
    WM_OT_DeleteAnim, 
    WM_OT_DeleteMat, 
    WM_OT_DeleteFollowPath, 
    WM_OT_ResetDefaults, 
    WM_OT_OffsetAnim, 
    WM_OT_OffsetSetAnim, 
    )
"""

def register():
    
    for cls in classes:
        
        bpy.utils.register_class(cls)


def unregister():
    
    for cls in classes:
        
        bpy.utils.unregister_class(cls)
"""
        
register, unregister = bpy.utils.register_classes_factory(classes)


if __name__ == "__main__":
    register()
    #bpy.ops.wm.animop('INVOKE_DEFAULT')