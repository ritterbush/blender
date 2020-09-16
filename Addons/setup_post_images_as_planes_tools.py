bl_info = {
    "name": "Images",
    "author": "Paul Ritterbush",
    "version": (1, 0),
    "blender": (2, 80, 2),
    "location": "View3D > Sidebar > Images Tab",
    "description": "Uses the popular Add Images As Planes (if Installed) and includes my favorite post AIAP tools",
    "warning": "",
    "wiki_url": "",
    "category": "Objects",
}


import bpy


"""Good shaders/ ideas:
    
Black/White abstract RGB to BW -> Brightness Contrast (Main Controls are both) -> [Not needed, actually: Bump (Color to Normal)]

Above is good for making whites very bright

Black and monochrome: add Color Ramp and set factor to be a color (yellow is retro/60's looking);
adjust handles untill a good black/color contrast is made   
    
"""


def SetSelectedMaterials():
            
    objs = [o for o in bpy.context.selected_objects]
    
    #This assumes my scripts will all be run in order going down the line
    y_axis_counter = 0
        
    for obj in objs:
        
        
        
        obj.location[2] += 0.5 #Lifts the image out of the murky depths
                           
        material = obj.active_material
        
        material.node_tree.nodes["Principled BSDF"].inputs[4].default_value = 1 #Metallic
        
        obj.location[1] += y_axis_counter
        
        y_axis_counter = y_axis_counter + (obj.dimensions[1] * 6)
        


    
def MakeMonoChromesSelected(axis=1, custom=False): 
    """ 
    """
    
    if custom:
        
        custom_axis = axis
    
    #y-axis is acording to width, processed per obj in the for loop
    if axis == 1: 
        
        offset = 1
    
    #z-axis
    elif axis == 2:
        
        offset = 1
        
    #x-axis
    else:
        
        offset = -0.5
        
    
    objs = [o for o in bpy.context.selected_objects]
    
    #Track new monochromes to select at end
    monochromes = []
            
    
    for obj in objs:
        
        #Process the y-axis value based on obj's width
        if axis == 1: 
            
            greatest_vert_loc = 0
            least_vert_loc = 0
            
            for vert in obj.data.vertices:
                                
                #vert.co[0] marks the y-axis location if it were not rotated 90 degs
                if vert.co[0] > greatest_vert_loc:
                    
                    greatest_vert_loc = vert.co[0]
                
                if vert.co[0] < least_vert_loc:
                    
                    least_vert_loc = vert.co[0]
            
                    
            offset = least_vert_loc * -1 + greatest_vert_loc
        
        if custom:
            
            axis = custom_axis
                         
        for ob in bpy.context.selected_objects: #Deselect any selected objects
                
            bpy.data.objects[ob.name].select_set(False)
                
        obj.select_set(True) #Select obj                
        
        bpy.context.view_layer.objects.active = obj #Set obj to be active object
        
        
        name = obj.name
        
        new_name = name + 'Black Mono'
        
        bpy.ops.object.duplicate() 
        
        monochromes += [bpy.context.active_object]
        
        bpy.context.active_object.name = new_name

        
        #Fixes issue of being unable rerun script on source and make multiple monochrome copies
        new_name = bpy.context.active_object.name
        
        bpy.data.objects[new_name].active_material = bpy.data.objects[name].active_material.copy()
        
        bpy.data.objects[new_name].active_material.name = new_name
        
        #Fixes issue of being unable rerun script on source and make multiple monochrome copies
        material = bpy.data.objects[new_name].active_material
        
        print(axis, 'val')
        
        bpy.data.objects[new_name].location[axis] += offset
        #bpy.data.objects[new_name].location[1] += 1
        
        image_texture = material.node_tree.nodes.get('Image Texture')
        image_texture.location = (-600, 0)          
        principled_bsdf = material.node_tree.nodes.get('Principled BSDF')
        principled_bsdf.location = (0, 0)      
        material_output = material.node_tree.nodes.get('Material Output')
        material_output.location = (400, 0)
                
        
        """Create Black Monochrome Color Ramp"""   

        # create node in group
        color_rmp = material.node_tree.nodes.new("ShaderNodeValToRGB")
        color_rmp.location = (-300, 0)
        color_rmp.color_ramp.elements[0].color = (0,0,0,1) #Black
        color_rmp.color_ramp.elements[1].color = (1,1,1,1)
        color_rmp.color_ramp.elements[0].position = 0.1 
        color_rmp.color_ramp.elements[1].position = 0.11
        
        material.node_tree.links.new(image_texture.outputs[0], color_rmp.inputs[0])
        material.node_tree.links.new(color_rmp.outputs[0], principled_bsdf.inputs[0])
        material.node_tree.links.new(principled_bsdf.outputs[0], material_output.inputs[0])
        
        
        new_name = name + 'Red Mono'
        
        bpy.ops.object.duplicate()
        
        monochromes += [bpy.context.active_object]
        
        bpy.context.active_object.name = new_name
        
        #Fixes issue of being unable rerun script on source and make multiple monochrome copies
        new_name = bpy.context.active_object.name
        
        bpy.data.objects[new_name].active_material = bpy.data.objects[name].active_material.copy()
        
        bpy.data.objects[new_name].active_material.name = new_name
        
        #Fixes issue of being unable rerun script on source and make multiple monochrome copies
        material = bpy.data.objects[new_name].active_material
        
        bpy.data.objects[new_name].location[axis] += offset
        
        
        image_texture = material.node_tree.nodes.get('Image Texture')
        image_texture.location = (-600, 0)          
        principled_bsdf = material.node_tree.nodes.get('Principled BSDF')
        principled_bsdf.location = (0, 0)      
        material_output = material.node_tree.nodes.get('Material Output')
        material_output.location = (400, 0)
                
        
        """Create Red Monochrome Color Ramp"""   

        # create node in group
        color_rmp = material.node_tree.nodes.new("ShaderNodeValToRGB")
        color_rmp.location = (-300, 0)
        color_rmp.color_ramp.elements[0].color = (1,0,0,1) #Red
        color_rmp.color_ramp.elements[1].color = (1,1,1,1)
        color_rmp.color_ramp.elements[0].position = 0.1 
        color_rmp.color_ramp.elements[1].position = 0.11
        
        material.node_tree.links.new(image_texture.outputs[0], color_rmp.inputs[0])
        material.node_tree.links.new(color_rmp.outputs[0], principled_bsdf.inputs[0])
        material.node_tree.links.new(principled_bsdf.outputs[0], material_output.inputs[0])

        
        
        new_name = name + 'Green Mono'
        
        bpy.ops.object.duplicate()
        
        monochromes += [bpy.context.active_object]
        
        bpy.context.active_object.name = new_name
        
        #Fixes issue of being unable rerun script on source and make multiple monochrome copies
        new_name = bpy.context.active_object.name
        
        bpy.data.objects[new_name].active_material = bpy.data.objects[name].active_material.copy()
        
        bpy.data.objects[new_name].active_material.name = new_name
        
        #Fixes issue of being unable rerun script on source and make multiple monochrome copies
        material = bpy.data.objects[new_name].active_material
        
        bpy.data.objects[new_name].location[axis] += offset
        
        
        image_texture = material.node_tree.nodes.get('Image Texture')
        image_texture.location = (-600, 0)          
        principled_bsdf = material.node_tree.nodes.get('Principled BSDF')
        principled_bsdf.location = (0, 0)      
        material_output = material.node_tree.nodes.get('Material Output')
        material_output.location = (400, 0)
                
        
        """Create Green Monochrome Color Ramp"""   

        # create node in group
        color_rmp = material.node_tree.nodes.new("ShaderNodeValToRGB")
        color_rmp.location = (-300, 0)
        color_rmp.color_ramp.elements[0].color = (0,1,0,1) #Green
        color_rmp.color_ramp.elements[1].color = (1,1,1,1)
        color_rmp.color_ramp.elements[0].position = 0.1 
        color_rmp.color_ramp.elements[1].position = 0.11
        
        material.node_tree.links.new(image_texture.outputs[0], color_rmp.inputs[0])
        material.node_tree.links.new(color_rmp.outputs[0], principled_bsdf.inputs[0])
        material.node_tree.links.new(principled_bsdf.outputs[0], material_output.inputs[0])

        
        new_name = name + 'Blue Mono'
        
        bpy.ops.object.duplicate()
        
        monochromes += [bpy.context.active_object]
        
        bpy.context.active_object.name = new_name
        
        #Fixes issue of being unable rerun script on source and make multiple monochrome copies
        new_name = bpy.context.active_object.name
        
        bpy.data.objects[new_name].active_material = bpy.data.objects[name].active_material.copy()
        
        bpy.data.objects[new_name].active_material.name = new_name
        
        #Fixes issue of being unable rerun script on source and make multiple monochrome copies
        material = bpy.data.objects[new_name].active_material
        
        bpy.data.objects[new_name].location[axis] += offset
        
        
        image_texture = material.node_tree.nodes.get('Image Texture')
        image_texture.location = (-600, 0)          
        principled_bsdf = material.node_tree.nodes.get('Principled BSDF')
        principled_bsdf.location = (0, 0)      
        material_output = material.node_tree.nodes.get('Material Output')
        material_output.location = (400, 0)
                
        
        """Create Blue Monochrome Color Ramp"""   

        # create node in group
        color_rmp = material.node_tree.nodes.new("ShaderNodeValToRGB")
        color_rmp.location = (-300, 0)
        color_rmp.color_ramp.elements[0].color = (0,0,1,1) #Blue
        color_rmp.color_ramp.elements[1].color = (1,1,1,1)
        color_rmp.color_ramp.elements[0].position = 0.1 
        color_rmp.color_ramp.elements[1].position = 0.11
        
        material.node_tree.links.new(image_texture.outputs[0], color_rmp.inputs[0])
        material.node_tree.links.new(color_rmp.outputs[0], principled_bsdf.inputs[0])
        material.node_tree.links.new(principled_bsdf.outputs[0], material_output.inputs[0])
                
        new_name = name + 'Yellow Mono'
        
        bpy.ops.object.duplicate()
        
        monochromes += [bpy.context.active_object]
        
        bpy.context.active_object.name = new_name
        
        #Fixes issue of being unable rerun script on source and make multiple monochrome copies
        new_name = bpy.context.active_object.name
        
        bpy.data.objects[new_name].active_material = bpy.data.objects[name].active_material.copy()
        
        bpy.data.objects[new_name].active_material.name = new_name
        
        #Fixes issue of being unable rerun script on source and make multiple monochrome copies
        material = bpy.data.objects[new_name].active_material
        
        bpy.data.objects[new_name].location[axis] += offset
        
        
        image_texture = material.node_tree.nodes.get('Image Texture')
        image_texture.location = (-600, 0)          
        principled_bsdf = material.node_tree.nodes.get('Principled BSDF')
        principled_bsdf.location = (0, 0)      
        material_output = material.node_tree.nodes.get('Material Output')
        material_output.location = (400, 0)
                
        
        """Create Yellow Monochrome Color Ramp"""   

        # create node in group
        color_rmp = material.node_tree.nodes.new("ShaderNodeValToRGB")
        color_rmp.location = (-300, 0)
        color_rmp.color_ramp.elements[0].color = (1,1,0,1) #Yellow
        color_rmp.color_ramp.elements[1].color = (1,1,1,1)
        color_rmp.color_ramp.elements[0].position = 0.1 
        color_rmp.color_ramp.elements[1].position = 0.11
        
        material.node_tree.links.new(image_texture.outputs[0], color_rmp.inputs[0])
        material.node_tree.links.new(color_rmp.outputs[0], principled_bsdf.inputs[0])
        material.node_tree.links.new(principled_bsdf.outputs[0], material_output.inputs[0])


        
        new_name = name + 'Pink Mono'
        
        bpy.ops.object.duplicate()
        
        monochromes += [bpy.context.active_object]
        
        bpy.context.active_object.name = new_name
        
        #Fixes issue of being unable rerun script on source and make multiple monochrome copies
        new_name = bpy.context.active_object.name
        
        bpy.data.objects[new_name].active_material = bpy.data.objects[name].active_material.copy()
        
        bpy.data.objects[new_name].active_material.name = new_name
        
        #Fixes issue of being unable rerun script on source and make multiple monochrome copies
        material = bpy.data.objects[new_name].active_material
        
        bpy.data.objects[new_name].location[axis] += offset
        
        
        image_texture = material.node_tree.nodes.get('Image Texture')
        image_texture.location = (-600, 0)          
        principled_bsdf = material.node_tree.nodes.get('Principled BSDF')
        principled_bsdf.location = (0, 0)      
        material_output = material.node_tree.nodes.get('Material Output')
        material_output.location = (400, 0)
                
        
        """Create Pink Monochrome Color Ramp"""   

        # create node in group
        color_rmp = material.node_tree.nodes.new("ShaderNodeValToRGB")
        color_rmp.location = (-300, 0)
        color_rmp.color_ramp.elements[0].color = (0.5,0.0,0.5,1) #Pink
        color_rmp.color_ramp.elements[1].color = (1,1,1,1)
        color_rmp.color_ramp.elements[0].position = 0.1 
        color_rmp.color_ramp.elements[1].position = 0.11
        
        material.node_tree.links.new(image_texture.outputs[0], color_rmp.inputs[0])
        material.node_tree.links.new(color_rmp.outputs[0], principled_bsdf.inputs[0])
        material.node_tree.links.new(principled_bsdf.outputs[0], material_output.inputs[0])
        
    for ob in bpy.context.selected_objects:
                
        obj.select_set(False)
    
    #Let's select just these new monochrome objs to set up for next fns
    for monochrome in monochromes:
        
        monochrome.select_set(True)
        
        
        

    
def MakeInvertedMonoChromesSelected(axis=2, custom=False):
    
    """
    Then make one that changes black to white. 

    """
    
    if custom:
        
        custom_axis = axis
    
    #y-axis is acording to width, processed per obj in the for loop
    if axis == 1: 
        
        offset = 1
    
    #z-axis
    elif axis == 2:
        
        offset = 1
        
    #x-axis
    else:
        
        offset = -0.5
        
    
    objs = [o for o in bpy.context.selected_objects]
    
    #Let's have objs and newly made monochromes selected at the end
    monochromes = [o for o in objs]
            
    
    for obj in objs:
        
        #Process the y-axis value based on obj's width
        if axis == 1: 
            
            greatest_vert_loc = 0
            least_vert_loc = 0
            
            for vert in obj.data.vertices:
                                
                #vert.co[0] marks the y-axis location if it were not rotated 90 degs
                if vert.co[0] > greatest_vert_loc:
                    
                    greatest_vert_loc = vert.co[0]
                
                if vert.co[0] < least_vert_loc:
                    
                    least_vert_loc = vert.co[0]
            
                    
            offset = least_vert_loc * -1 + greatest_vert_loc
        
        if custom:
            
            axis = custom_axis
                         
        for ob in bpy.context.selected_objects: #Deselect any selected objects
                
            bpy.data.objects[ob.name].select_set(False)
                
        obj.select_set(True) #Select obj                
        
        bpy.context.view_layer.objects.active = obj #Set obj to be active object
        
        
        name = obj.name        
        new_name = name + ' Inv'
                
        """Create obj that uses above """
        bpy.ops.object.duplicate()
        
        monochromes += [bpy.context.active_object]
        
        bpy.context.active_object.name = new_name
        
        
        
        #Fixes issue of being unable rerun script on source and make multiple monochrome copies
        new_name = bpy.context.active_object.name
        
        bpy.data.objects[new_name].active_material = bpy.data.objects[name].active_material.copy()
        
        bpy.data.objects[new_name].active_material.name = new_name
        
        #Fixes issue of being unable rerun script on source and make multiple monochrome copies
        material = bpy.data.objects[new_name].active_material
        
        
        bpy.data.objects[new_name].location[axis] += offset
        
        color_rmp = material.node_tree.nodes.get('ColorRamp')
        

        color_rmp.color_ramp.elements[1].color = color_rmp.color_ramp.elements[0].color #Gets colored element based on prev fn
        color_rmp.color_ramp.elements[0].color = (1,1,1,1)
        
        
    for ob in bpy.context.selected_objects:
                
        obj.select_set(False)
    
    #Let's select monochrome objs
    for monochrome in monochromes:
        
        monochrome.select_set(True)
      
        
    
def MakeWhiteBlackMonoChromesSelected(axis=2, custom=False):
    
    """
    Then make one that changes black to white. 

    """
    
    if custom:
        
        custom_axis = axis
    
    #y-axis is acording to width, processed per obj in the for loop
    if axis == 1: 
        
        offset = 1
    
    #z-axis
    elif axis == 2:
        
        offset = 2
        
    #x-axis
    else:
        
        offset = -0.5
        
    
    objs = [o for o in bpy.context.selected_objects]
    
    #Let's have objs and newly made monochromes selected at the end
    monochromes = [o for o in objs]
            
    
    for obj in objs:
        
        #Process the y-axis value based on obj's width
        if axis == 1: 
            
            greatest_vert_loc = 0
            least_vert_loc = 0
            
            for vert in obj.data.vertices:
                                
                #vert.co[0] marks the y-axis location if it were not rotated 90 degs
                if vert.co[0] > greatest_vert_loc:
                    
                    greatest_vert_loc = vert.co[0]
                
                if vert.co[0] < least_vert_loc:
                    
                    least_vert_loc = vert.co[0]
            
                    
            offset = least_vert_loc * -1 + greatest_vert_loc
        
        if custom:
            
            axis = custom_axis
                                     
        for ob in bpy.context.selected_objects: #Deselect any selected objects
                
            bpy.data.objects[ob.name].select_set(False)
                
        obj.select_set(True) #Select obj                
        
        bpy.context.view_layer.objects.active = obj #Set obj to be active object
        
        
        name = obj.name        
        new_name = name + ' Blk'
                
        """Create obj that uses above """
        bpy.ops.object.duplicate()
        
        monochromes += [bpy.context.active_object]
        
        bpy.context.active_object.name = new_name
        
        
        #Fixes issue of being unable rerun script on source and make multiple monochrome copies
        new_name = bpy.context.active_object.name
        
        bpy.data.objects[new_name].active_material = bpy.data.objects[name].active_material.copy()
        
        bpy.data.objects[new_name].active_material.name = new_name
        
        #Fixes issue of being unable rerun script on source and make multiple monochrome copies
        material = bpy.data.objects[new_name].active_material
        
        
        bpy.data.objects[new_name].location[axis] += offset
        
        color_rmp = material.node_tree.nodes.get('ColorRamp')
        
        """
        
        for element in color_rmp.color_ramp.elements:
            
            if element.color == (1,1,1,1):
            
                element.color = (0,0,0,1)
        """
        
        #Hacky, but the above does not work for some reason
        if ' Inv' in name:
                
            #color_rmp.color_ramp.elements[1].color = color_rmp.color_ramp.elements[0].color #Gets colored element based on prev fn
            color_rmp.color_ramp.elements[0].color = (0,0,0,1)
            
        else:
            color_rmp.color_ramp.elements[1].color = (0,0,0,1)
                    


        
    for ob in bpy.context.selected_objects:
                
        obj.select_set(False)
    
    #Let's select just these new monochrome objs to set up for next fns
    for monochrome in monochromes:
        
        monochrome.select_set(True)
        
    #Make the first obj made the active obj
    
    bpy.context.active_object 



#CreateImagePlanesCol() #Run this just once per .blend file
#SetSelectedMaterials() 


###MakeMonoChromeNodeGroups() #For MakeMonoChromesSelectedOld(), but run this just once per .blend file
###MakeMonoChromesSelectedOld() #Note: it probably makes more sense to use this on a need to have basis

#MakeMonoChromesSelected() #Note: it probably makes more sense to use this on a need to have basis
#MakeInvertedMonoChromesSelected() #Use this after making mono chromed version and then selecting just those just created(color ramp required in the material)
#MakeWhiteBlackMonoChromesSelected() #Use this after reselecting desired, if the above was just run


class Images_PT_Panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Images"
    bl_idname = "OBJECT_PT_Images"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    #bl_context = "object"
    bl_category = "Images" #Name in UI Panel

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

        #No exception is thrown when calling operator method with null reference, so check for addon this way:
        check_images_as_planes = row.operator("import_image.to_plane")
        
        if not check_images_as_planes:
            print("The 'Import Images as Planes' panel button requires the 'Import Images as Planes' Addon. Install it to make the button appear.")
        
        #col = row.column(align=True)
        #row = layout.row()
        #col.operator("wm.copyanimop", icon="RESTRICT_SELECT_OFF", text="")
        #row.operator("wm.copyanimop", icon="RESTRICT_SELECT_OFF", text="")
        

        row = layout.row()
        row.operator("wm.setselectedmatsop")
        row = layout.row()
        row.operator("wm.makemonochromesop")
        row = layout.row()
        row.operator("wm.makeinvertedmonochromesop")
        row = layout.row()
        row.operator("wm.makewhiteblackmonochromesop")
        
        
class WM_OT_SetSelectedMaterialsOP(bpy.types.Operator):
    """Makes the image look much better by making material reflect light"""
    
    bl_label = "Set Materials"
    bl_idname = "wm.setselectedmatsop" 
        
    def execute(self, context):

        SetSelectedMaterials()
        
        return {'FINISHED'}
        
class WM_OT_MakeMonochromesSelectedOP(bpy.types.Operator):
    """Makes monochrome duplicates of the selected"""
    
    bl_label = "Make Monochromes"
    bl_idname = "wm.makemonochromesop" 
    
    x_axis: bpy.props.BoolProperty(name="x", default=False)
    y_axis: bpy.props.BoolProperty(name="y", default=True)
    z_axis: bpy.props.BoolProperty(name="z", default=False)
    
    
    custom_offset: bpy.props.BoolProperty(name="Custom Offset", default=False)
    amount: bpy.props.FloatProperty(name="", default=1.0)

    
    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)        
    
    def draw(self, context):
        
        layout = self.layout
        box = layout.box() #Makes a box separator to separate text from bl_label
        
        #use row for multiple items sharing the same row, and layout otherwise
        row = box.row()
        row.label(text="Axis:")
        row.prop(self, "x_axis")
        
        #row = box.row() #Ensures the following will share the same row
        #row.label(text="y_axis")
        row.prop(self, "y_axis")
        
        #row = box.row() #Ensures the following will share the same row
        #row.label(text="Brightness")        
        row.prop(self, "z_axis")
        
        box = layout.box() #Makes a box separator
        box.prop(self,"custom_offset") #will be on its own row
        
        """
        Making the selection exclusive is not working at all!! 
        Actually, it works z to x, but not x to z.
        if self.x_axis:
            self.x_axis = True
            self.y_axis = False
            self.z_axis = False
                    
        if self.y_axis:
            self.x_axis = False
            self.y_axis = True
            self.z_axis = False
                        
        if self.z_axis:
            self.x_axis = False
            self.y_axis = False
            self.z_axis = True      
        """                
        
        if self.custom_offset: #makes conditional on having box checked
        
            row = box.row() #Ensures the following will share the same row in the box
        
            row.prop(self, "amount")

    
        
    def execute(self, context):
        
        x_axis = self.x_axis
        y_axis = self.y_axis
        z_axis = self.z_axis
        custom_offset = self.custom_offset
        amount = self.amount
        
        if x_axis:
            axis = 0
        if y_axis:
            axis = 1
        if z_axis:
            axis = 2
        if custom_offset:
            axis = amount
            
        
        
        MakeMonoChromesSelected(axis)
        
        return {'FINISHED'}
        
class WM_OT_MakeInvertedMonoChromesSelectedOP(bpy.types.Operator):
    """Makes inverted monochrome duplicates of the selected"""
    
    bl_label = "Make Inverted Monochromes"
    bl_idname = "wm.makeinvertedmonochromesop" 
    
    
    
    x_axis: bpy.props.BoolProperty(name="x", default=False)
    y_axis: bpy.props.BoolProperty(name="y", default=False)
    z_axis: bpy.props.BoolProperty(name="z", default=True)
    
    
    custom_offset: bpy.props.BoolProperty(name="Custom Offset", default=False)
    amount: bpy.props.FloatProperty(name="", default=1.0)

    
    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)        
    
    def draw(self, context):
        
        layout = self.layout
        box = layout.box() #Makes a box separator to separate text from bl_label
        
        #use row for multiple items sharing the same row, and layout otherwise
        row = box.row()
        row.label(text="Axis:")
        row.prop(self, "x_axis")
        
        #row = box.row() #Ensures the following will share the same row
        #row.label(text="y_axis")
        row.prop(self, "y_axis")
        
        #row = box.row() #Ensures the following will share the same row
        #row.label(text="Brightness")        
        row.prop(self, "z_axis")
        
        box = layout.box() #Makes a box separator
        box.prop(self,"custom_offset") #will be on its own row               
        
        if self.custom_offset: #makes conditional on having box checked
        
            row = box.row() #Ensures the following will share the same row in the box
        
            row.prop(self, "amount")    
    
        
    def execute(self, context):

        x_axis = self.x_axis
        y_axis = self.y_axis
        z_axis = self.z_axis
        custom_offset = self.custom_offset
        amount = self.amount
        
        if x_axis:
            axis = 0
        if y_axis:
            axis = 1
        if z_axis:
            axis = 2
        if custom_offset:
            axis = amount


        MakeInvertedMonoChromesSelected()
        
        return {'FINISHED'}
        
class WM_OT_MakeWhiteBlackMonoChromesSelectedOP(bpy.types.Operator):
    """Makes white half black monochrome duplicates of the selected"""
    
    bl_label = "Make Black Monochromes"
    bl_idname = "wm.makewhiteblackmonochromesop"
    
    
    x_axis: bpy.props.BoolProperty(name="x", default=False)
    y_axis: bpy.props.BoolProperty(name="y", default=False)
    z_axis: bpy.props.BoolProperty(name="z", default=True)
    
    
    custom_offset: bpy.props.BoolProperty(name="Custom Offset", default=False)
    amount: bpy.props.FloatProperty(name="", default=1.0)

    
    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)        
    
    def draw(self, context):
        
        layout = self.layout
        box = layout.box() #Makes a box separator to separate text from bl_label
        
        #use row for multiple items sharing the same row, and layout otherwise
        row = box.row()
        row.label(text="Axis:")
        row.prop(self, "x_axis")
        
        #row = box.row() #Ensures the following will share the same row
        #row.label(text="y_axis")
        row.prop(self, "y_axis")
        
        #row = box.row() #Ensures the following will share the same row
        #row.label(text="Brightness")        
        row.prop(self, "z_axis")
        
        box = layout.box() #Makes a box separator
        box.prop(self,"custom_offset") #will be on its own row
                      
        
        if self.custom_offset: #makes conditional on having box checked
        
            row = box.row() #Ensures the following will share the same row in the box
        
            row.prop(self, "amount")
    
        
    def execute(self, context):
        
        x_axis = self.x_axis
        y_axis = self.y_axis
        z_axis = self.z_axis
        custom_offset = self.custom_offset
        amount = self.amount
        
        if x_axis:
            axis = 0
        if y_axis:
            axis = 1
        if z_axis:
            axis = 2
        if custom_offset:
            axis = amount

        MakeWhiteBlackMonoChromesSelected()
        
        return {'FINISHED'}


"""
CreateImagePlanesCol()
SetSelectedMaterials()
MakeMonochromesSelected()
MakeInvertedMonoChromesSelected()
MakeWhiteBlackMonoChromesSelected()
"""

classes = (
    Images_PT_Panel,  
    WM_OT_SetSelectedMaterialsOP,
    WM_OT_MakeMonochromesSelectedOP,
    WM_OT_MakeInvertedMonoChromesSelectedOP,
    WM_OT_MakeWhiteBlackMonoChromesSelectedOP,        
    )

      
register, unregister = bpy.utils.register_classes_factory(classes)


if __name__ == "__main__":
    register()
    #bpy.ops.wm.animop('INVOKE_DEFAULT')


