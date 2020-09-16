import bpy 


"""Good shaders/ ideas:
    
Black/White abstract RGB to BW -> Brightness Contrast (Main Controls are both) -> [Not needed, actually: Bump (Color to Normal)]

Above is good for making whites very bright

Black and monochrome: add Color Ramp and set factor to be a color (yellow is retro/60's looking);
adjust handles untill a good black/color contrast is made   
    
"""

def CreateImagePlanesCol():
    """Run this just once per blend file"""
    
    new_col = bpy.data.collections.new(name='Image Planes') #create new collection in data
    bpy.context.scene.collection.children.link(new_col) #add new collection to the scene  


def SetSelectedMaterials():
            
    objs = [o for o in bpy.context.selected_objects]
        
    for obj in objs:
        
        name = obj.name
        
        """Import Images as Planes names obj and material the same"""
        
        obj.location[2] += 1
                
        material = bpy.data.materials[name]
        
        material.node_tree.nodes["Principled BSDF"].inputs[4].default_value = 1 #Metallic
                        
        """Add Image to Image Planes Col"""
        obj_old_col = bpy.data.objects[name].users_collection #list of all collections the txt_obj is in, the main scene by default

        new_col = bpy.data.collections['Image Planes']
        
        for ob in obj_old_col: #unlink from all previous collections
            
            ob.objects.unlink(bpy.data.objects[name])   
                
        new_col.objects.link(bpy.data.objects[name]) #link txt_obj to new_col

def MakeMonoChromeNodeGroups():
    """
    Update: no real need to make a bunch of node groups for this. Just run the fn that doesn't
    use or create node groups.
    Note: run this fn just once and do not run if these groups have already been made!
    (Worst case is that you'll have unused copies that you can delete by checking 'Orphaned Data'
    as a selectable display mode in the outliner)
    
    I have the left handle set to .1 and the right to .11, and then a color given as expected
    """
    
    """Create Black Mono Group"""   
    blk_group = bpy.data.node_groups.new('Black Mono', 'ShaderNodeTree')

    # create group inputs
    blk_group_inputs = blk_group.nodes.new('NodeGroupInput')
    blk_group_inputs.location = (-300,0)
    #test_group.inputs.new('NodeSocketFloat','in_to_greater')
    #test_group.inputs.new('NodeSocketFloat','in_to_less')

    # create group outputs
    blk_group_outputs = blk_group.nodes.new('NodeGroupOutput')
    blk_group_outputs.location = (400,0)

    # create node in group
    color_rmp = blk_group.nodes.new("ShaderNodeValToRGB")
    color_rmp.location = (0, 0)
    color_rmp.color_ramp.elements[0].color = (0,0,0,1) #Black
    color_rmp.color_ramp.elements[1].color = (1,1,1,1)
    color_rmp.color_ramp.elements[0].position = 0.1 
    color_rmp.color_ramp.elements[1].position = 0.11

    # link input
    blk_group.links.new(blk_group_inputs.outputs[0], color_rmp.inputs[0])

    #link output
    blk_group.links.new(color_rmp.outputs[0], blk_group_outputs.inputs[0])
    blk_group.links.new(color_rmp.outputs[1], blk_group_outputs.inputs[1])
    
    """Create Red Mono Group"""   
    blk_group = bpy.data.node_groups.new('Red Mono', 'ShaderNodeTree')

    # create group inputs
    blk_group_inputs = blk_group.nodes.new('NodeGroupInput')
    blk_group_inputs.location = (-300,0)
    #test_group.inputs.new('NodeSocketFloat','in_to_greater')
    #test_group.inputs.new('NodeSocketFloat','in_to_less')

    # create group outputs
    blk_group_outputs = blk_group.nodes.new('NodeGroupOutput')
    blk_group_outputs.location = (400,0)

    # create node in group
    color_rmp = blk_group.nodes.new("ShaderNodeValToRGB")
    color_rmp.location = (0, 0)
    color_rmp.color_ramp.elements[0].color = (1,0,0,1) #Red
    color_rmp.color_ramp.elements[1].color = (1,1,1,1)
    color_rmp.color_ramp.elements[0].position = 0.1 
    color_rmp.color_ramp.elements[1].position = 0.11

    # link input
    blk_group.links.new(blk_group_inputs.outputs[0], color_rmp.inputs[0])

    #link output
    blk_group.links.new(color_rmp.outputs[0], blk_group_outputs.inputs[0])
    blk_group.links.new(color_rmp.outputs[1], blk_group_outputs.inputs[1])
        
    """Create Green Mono Group"""   
    blk_group = bpy.data.node_groups.new('Green Mono', 'ShaderNodeTree')

    # create group inputs
    blk_group_inputs = blk_group.nodes.new('NodeGroupInput')
    blk_group_inputs.location = (-300,0)
    #test_group.inputs.new('NodeSocketFloat','in_to_greater')
    #test_group.inputs.new('NodeSocketFloat','in_to_less')

    # create group outputs
    blk_group_outputs = blk_group.nodes.new('NodeGroupOutput')
    blk_group_outputs.location = (400,0)

    # create node in group
    color_rmp = blk_group.nodes.new("ShaderNodeValToRGB")
    color_rmp.location = (0, 0)
    color_rmp.color_ramp.elements[0].color = (0,1,0,1) #Green
    color_rmp.color_ramp.elements[1].color = (1,1,1,1)
    color_rmp.color_ramp.elements[0].position = 0.1 
    color_rmp.color_ramp.elements[1].position = 0.11

    # link input
    blk_group.links.new(blk_group_inputs.outputs[0], color_rmp.inputs[0])

    #link output
    blk_group.links.new(color_rmp.outputs[0], blk_group_outputs.inputs[0])
    blk_group.links.new(color_rmp.outputs[1], blk_group_outputs.inputs[1])
            
    """Create Blue Mono Group"""   
    blk_group = bpy.data.node_groups.new('Blue Mono', 'ShaderNodeTree')

    # create group inputs
    blk_group_inputs = blk_group.nodes.new('NodeGroupInput')
    blk_group_inputs.location = (-300,0)
    #test_group.inputs.new('NodeSocketFloat','in_to_greater')
    #test_group.inputs.new('NodeSocketFloat','in_to_less')

    # create group outputs
    blk_group_outputs = blk_group.nodes.new('NodeGroupOutput')
    blk_group_outputs.location = (400,0)

    # create node in group
    color_rmp = blk_group.nodes.new("ShaderNodeValToRGB")
    color_rmp.location = (0, 0)
    color_rmp.color_ramp.elements[0].color = (0,0,1,1) #Blue
    color_rmp.color_ramp.elements[1].color = (1,1,1,1)
    color_rmp.color_ramp.elements[0].position = 0.1 
    color_rmp.color_ramp.elements[1].position = 0.11

    # link input
    blk_group.links.new(blk_group_inputs.outputs[0], color_rmp.inputs[0])

    #link output
    blk_group.links.new(color_rmp.outputs[0], blk_group_outputs.inputs[0]) 
    blk_group.links.new(color_rmp.outputs[1], blk_group_outputs.inputs[1])
           
    """Create Yellow Mono Group"""   
    blk_group = bpy.data.node_groups.new('Yellow Mono', 'ShaderNodeTree')

    # create group inputs
    blk_group_inputs = blk_group.nodes.new('NodeGroupInput')
    blk_group_inputs.location = (-300,0)
    #test_group.inputs.new('NodeSocketFloat','in_to_greater')
    #test_group.inputs.new('NodeSocketFloat','in_to_less')

    # create group outputs
    blk_group_outputs = blk_group.nodes.new('NodeGroupOutput')
    blk_group_outputs.location = (400,0)

    # create node in group
    color_rmp = blk_group.nodes.new("ShaderNodeValToRGB")
    color_rmp.location = (0, 0)
    color_rmp.color_ramp.elements[0].color = (1,1,0,1) #Yellow
    color_rmp.color_ramp.elements[1].color = (1,1,1,1)
    color_rmp.color_ramp.elements[0].position = 0.1 
    color_rmp.color_ramp.elements[1].position = 0.11

    # link input
    blk_group.links.new(blk_group_inputs.outputs[0], color_rmp.inputs[0])

    #link output
    blk_group.links.new(color_rmp.outputs[0], blk_group_outputs.inputs[0])    
    blk_group.links.new(color_rmp.outputs[1], blk_group_outputs.inputs[1])
        
    """Create Pink Mono Group"""   
    blk_group = bpy.data.node_groups.new('Pink Mono', 'ShaderNodeTree')

    # create group inputs
    blk_group_inputs = blk_group.nodes.new('NodeGroupInput')
    blk_group_inputs.location = (-300,0)
    #test_group.inputs.new('NodeSocketFloat','in_to_greater')
    #test_group.inputs.new('NodeSocketFloat','in_to_less')

    # create group outputs
    blk_group_outputs = blk_group.nodes.new('NodeGroupOutput')
    blk_group_outputs.location = (400,0)

    # create node in group
    color_rmp = blk_group.nodes.new("ShaderNodeValToRGB")
    color_rmp.location = (0, 0)
    color_rmp.color_ramp.elements[0].color = (1,0,1,1) #Pink
    color_rmp.color_ramp.elements[1].color = (1,1,1,1)
    color_rmp.color_ramp.elements[0].position = 0.1 
    color_rmp.color_ramp.elements[1].position = 0.11

    # link input
    blk_group.links.new(blk_group_inputs.outputs[0], color_rmp.inputs[0])

    #link output
    blk_group.links.new(color_rmp.outputs[0], blk_group_outputs.inputs[0])    
    blk_group.links.new(color_rmp.outputs[1], blk_group_outputs.inputs[1])
              
    
def MakeMonoChromesSelectedOld():
    
    """
    Prereq: make the monochrome nodes into a node group with Ctrl + G and then
    name it according to the names used below (e.g., 'Red Mono');
    Note that the fn above now does this.
    Play around by duplicateing inverting the color/white or making the white portions black instead

    """
    
    objs = [o for o in bpy.context.selected_objects]
        
    
    for obj in objs:
        
                         
        for ob in bpy.context.selected_objects: #Deselect any selected objects
                
            bpy.data.objects[ob.name].select_set(False)
                
        obj.select_set(True) #Select obj                
        
        bpy.context.view_layer.objects.active = obj #Set obj to be active object
        
        
        name = obj.name
        
        new_name = name + 'Black Mono'
        
        
        """Create obj that uses above """
        bpy.ops.object.duplicate()
        
        bpy.context.active_object.name = new_name
        
        bpy.data.objects[new_name].active_material = bpy.data.objects[name].material_slots[0].material.copy()
        
        bpy.data.objects[new_name].active_material.name = new_name
        
        material = bpy.data.materials[new_name]
        
        bpy.data.objects[new_name].location[0] += -0.5
        
        principled_bsdf = material.node_tree.nodes.get('Principled BSDF')
        material_output = material.node_tree.nodes.get('Material Output')
        
        #emission = material.node_tree.nodes.new("ShaderNodeEmission")
        #color_ramp = material.node_tree.nodes.new("ConverterNodeColorramp")
        #color_ramp = material.node_tree.nodes.new("ShaderNodeValToRGB")
        blk_mono = material.node_tree.nodes.new("ShaderNodeGroup")
        
        blk_mono.node_tree = bpy.data.node_groups['Black Mono']
        
    
        image_texture = material.node_tree.nodes.get('Image Texture')
        
        
        material.node_tree.links.new(image_texture.outputs[0], blk_mono.inputs[0])
        material.node_tree.links.new(blk_mono.outputs[0], principled_bsdf.inputs[0])
        #material.node_tree.links.new(principled_bsdf.outputs[0], material_output.inputs[0])
        
        
        new_name = name + 'Red Mono'
        
        bpy.ops.object.duplicate()
        
        bpy.context.active_object.name = new_name
        
        bpy.data.objects[new_name].active_material = bpy.data.objects[name].material_slots[0].material.copy()
        
        bpy.data.objects[new_name].active_material.name = new_name
        
        material = bpy.data.materials[new_name]
        
        bpy.data.objects[new_name].location[0] += -0.5
        
        principled_bsdf = material.node_tree.nodes.get('Principled BSDF')
        material_output = material.node_tree.nodes.get('Material Output')
        

        red_mono = material.node_tree.nodes.new("ShaderNodeGroup")
        
        red_mono.node_tree = bpy.data.node_groups['Red Mono']
        
    
        image_texture = material.node_tree.nodes.get('Image Texture')
        
        
        material.node_tree.links.new(image_texture.outputs[0], red_mono.inputs[0])
        material.node_tree.links.new(red_mono.outputs[0], principled_bsdf.inputs[0])


        
        new_name = name + 'Green Mono'
        
        bpy.ops.object.duplicate()
        
        bpy.context.active_object.name = new_name
        
        bpy.data.objects[new_name].active_material = bpy.data.objects[name].material_slots[0].material.copy()
        
        bpy.data.objects[new_name].active_material.name = new_name
        
        material = bpy.data.materials[new_name]
        
        bpy.data.objects[new_name].location[0] += -0.5
        
        principled_bsdf = material.node_tree.nodes.get('Principled BSDF')
        material_output = material.node_tree.nodes.get('Material Output')
        

        red_mono = material.node_tree.nodes.new("ShaderNodeGroup")
        
        red_mono.node_tree = bpy.data.node_groups['Green Mono']
        
    
        image_texture = material.node_tree.nodes.get('Image Texture')
        
        
        material.node_tree.links.new(image_texture.outputs[0], red_mono.inputs[0])
        material.node_tree.links.new(red_mono.outputs[0], principled_bsdf.inputs[0])

        
        new_name = name + 'Blue Mono'
        
        bpy.ops.object.duplicate()
        
        bpy.context.active_object.name = new_name
        
        bpy.data.objects[new_name].active_material = bpy.data.objects[name].material_slots[0].material.copy()
        
        bpy.data.objects[new_name].active_material.name = new_name
        
        material = bpy.data.materials[new_name]
        
        bpy.data.objects[new_name].location[0] += -0.5
        
        principled_bsdf = material.node_tree.nodes.get('Principled BSDF')
        material_output = material.node_tree.nodes.get('Material Output')
        

        red_mono = material.node_tree.nodes.new("ShaderNodeGroup")
        
        red_mono.node_tree = bpy.data.node_groups['Blue Mono']
        
    
        image_texture = material.node_tree.nodes.get('Image Texture')
        
        
        material.node_tree.links.new(image_texture.outputs[0], red_mono.inputs[0])
        material.node_tree.links.new(red_mono.outputs[0], principled_bsdf.inputs[0])

                
        new_name = name + 'Yellow Mono'
        
        bpy.ops.object.duplicate()
        
        bpy.context.active_object.name = new_name
        
        bpy.data.objects[new_name].active_material = bpy.data.objects[name].material_slots[0].material.copy()
        
        bpy.data.objects[new_name].active_material.name = new_name
        
        material = bpy.data.materials[new_name]
        
        bpy.data.objects[new_name].location[0] += -0.5
        
        principled_bsdf = material.node_tree.nodes.get('Principled BSDF')
        material_output = material.node_tree.nodes.get('Material Output')
        

        red_mono = material.node_tree.nodes.new("ShaderNodeGroup")
        
        red_mono.node_tree = bpy.data.node_groups['Yellow Mono']
        
    
        image_texture = material.node_tree.nodes.get('Image Texture')
        
        
        material.node_tree.links.new(image_texture.outputs[0], red_mono.inputs[0])
        material.node_tree.links.new(red_mono.outputs[0], principled_bsdf.inputs[0])


        
        new_name = name + 'Pink Mono'
        
        bpy.ops.object.duplicate()
        
        bpy.context.active_object.name = new_name
        
        bpy.data.objects[new_name].active_material = bpy.data.objects[name].material_slots[0].material.copy()
        
        bpy.data.objects[new_name].active_material.name = new_name
        
        material = bpy.data.materials[new_name]
        
        bpy.data.objects[new_name].location[0] += -0.5
        
        principled_bsdf = material.node_tree.nodes.get('Principled BSDF')
        material_output = material.node_tree.nodes.get('Material Output')
        

        red_mono = material.node_tree.nodes.new("ShaderNodeGroup")
        
        red_mono.node_tree = bpy.data.node_groups['Pink Mono']
        
    
        image_texture = material.node_tree.nodes.get('Image Texture')
        
        
        material.node_tree.links.new(image_texture.outputs[0], red_mono.inputs[0])
        material.node_tree.links.new(red_mono.outputs[0], principled_bsdf.inputs[0])

    
    
def MakeMonoChromesSelected():
    
    """
    This is now the preferred method. It no longer needs any node groups. 

    """
    
    objs = [o for o in bpy.context.selected_objects]
        
    
    for obj in objs:
        
                         
        for ob in bpy.context.selected_objects: #Deselect any selected objects
                
            bpy.data.objects[ob.name].select_set(False)
                
        obj.select_set(True) #Select obj                
        
        bpy.context.view_layer.objects.active = obj #Set obj to be active object
        
        
        name = obj.name
        
        new_name = name + 'Black Mono'
        
        
        """Create obj that uses above """
        bpy.ops.object.duplicate()
        
        bpy.context.active_object.name = new_name
        
        bpy.data.objects[new_name].active_material = bpy.data.objects[name].material_slots[0].material.copy()
        
        bpy.data.objects[new_name].active_material.name = new_name
        
        material = bpy.data.materials[new_name]
        
        bpy.data.objects[new_name].location[0] += -0.5
        bpy.data.objects[new_name].location[1] += 1
        
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
        
        bpy.context.active_object.name = new_name
        
        bpy.data.objects[new_name].active_material = bpy.data.objects[name].material_slots[0].material.copy()
        
        bpy.data.objects[new_name].active_material.name = new_name
        
        material = bpy.data.materials[new_name]
        
        bpy.data.objects[new_name].location[0] += -0.5
        
        
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
        
        bpy.context.active_object.name = new_name
        
        bpy.data.objects[new_name].active_material = bpy.data.objects[name].material_slots[0].material.copy()
        
        bpy.data.objects[new_name].active_material.name = new_name
        
        material = bpy.data.materials[new_name]
        
        bpy.data.objects[new_name].location[0] += -0.5
        
        
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
        
        bpy.context.active_object.name = new_name
        
        bpy.data.objects[new_name].active_material = bpy.data.objects[name].material_slots[0].material.copy()
        
        bpy.data.objects[new_name].active_material.name = new_name
        
        material = bpy.data.materials[new_name]
        
        bpy.data.objects[new_name].location[0] += -0.5
        
        
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
        
        bpy.context.active_object.name = new_name
        
        bpy.data.objects[new_name].active_material = bpy.data.objects[name].material_slots[0].material.copy()
        
        bpy.data.objects[new_name].active_material.name = new_name
        
        material = bpy.data.materials[new_name]
        
        bpy.data.objects[new_name].location[0] += -0.5
        
        
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
        
        bpy.context.active_object.name = new_name
        
        bpy.data.objects[new_name].active_material = bpy.data.objects[name].material_slots[0].material.copy()
        
        bpy.data.objects[new_name].active_material.name = new_name
        
        material = bpy.data.materials[new_name]
        
        bpy.data.objects[new_name].location[0] += -0.5
        
        
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

    
def MakeInvertedMonoChromesSelected():
    
    """
    Then make one that changes black to white. 

    """
    
    objs = [o for o in bpy.context.selected_objects]
        
    
    for obj in objs:
        
                         
        for ob in bpy.context.selected_objects: #Deselect any selected objects
                
            bpy.data.objects[ob.name].select_set(False)
                
        obj.select_set(True) #Select obj                
        
        bpy.context.view_layer.objects.active = obj #Set obj to be active object
        
        
        name = obj.name        
        new_name = name + ' Inv'
                
        """Create obj that uses above """
        bpy.ops.object.duplicate()
        
        bpy.context.active_object.name = new_name
        
        bpy.data.objects[new_name].active_material = bpy.data.objects[name].material_slots[0].material.copy()
        
        bpy.data.objects[new_name].active_material.name = new_name
        
        material = bpy.data.materials[new_name]
        
        bpy.data.objects[new_name].location[2] += 1
        
        color_rmp = material.node_tree.nodes.get('ColorRamp')
        

        color_rmp.color_ramp.elements[1].color = color_rmp.color_ramp.elements[0].color #Gets colored element based on prev fn
        color_rmp.color_ramp.elements[0].color = (1,1,1,1)
        
        """Create Black Monochrome Color Ramp"""   
        """
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
        
        """
        
        
    
def MakeWhiteBlackMonoChromesSelected():
    
    """
    Then make one that changes black to white. 

    """
    
    objs = [o for o in bpy.context.selected_objects]
        
    
    for obj in objs:
        
                         
        for ob in bpy.context.selected_objects: #Deselect any selected objects
                
            bpy.data.objects[ob.name].select_set(False)
                
        obj.select_set(True) #Select obj                
        
        bpy.context.view_layer.objects.active = obj #Set obj to be active object
        
        
        name = obj.name        
        new_name = name + ' Blk'
                
        """Create obj that uses above """
        bpy.ops.object.duplicate()
        
        bpy.context.active_object.name = new_name
        
        bpy.data.objects[new_name].active_material = bpy.data.objects[name].material_slots[0].material.copy()
        
        bpy.data.objects[new_name].active_material.name = new_name
        
        material = bpy.data.materials[new_name]
        
        bpy.data.objects[new_name].location[2] += 2
        
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
                    
        

CreateImagePlanesCol() #Run this just once per .blend file
SetSelectedMaterials() 


###MakeMonoChromeNodeGroups() #For MakeMonoChromesSelectedOld(), but run this just once per .blend file
###MakeMonoChromesSelectedOld() #Note: it probably makes more sense to use this on a need to have basis

#MakeMonoChromesSelected() #Note: it probably makes more sense to use this on a need to have basis
#MakeInvertedMonoChromesSelected() #Use this after making mono chromed version and then selecting just those just created(color ramp required in the material)
#MakeWhiteBlackMonoChromesSelected() #Use this after reselecting desired, if the above was just run

def AddEmissionObjs():
    
    """These create new emission materials with the spheres that use them
    Note: these will not behave like lights; these are more meant to add interest
    backgrounds, probably"""
    
    names = []
    
    """Creates Neon Yellow Emission Material"""
        
    name = 'Neon Yellow Sphere'
    names += [name]
    
    
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True #Required for the below cmds to work
    
    principled_bsdf = material.node_tree.nodes.get('Principled BSDF')
    material_output = material.node_tree.nodes.get('Material Output')
    material.node_tree.nodes.remove(principled_bsdf)
    
    emission = material.node_tree.nodes.new("ShaderNodeEmission")
        
    emission.inputs[0].default_value = (1, 1, 0, 1) #Grey; HEX = FFFF00
    emission.inputs[1].default_value = 20 #Strength
    #emission.inputs[7].default_value = 0.01 #Roughness
        
    
    # link nodes together
    material.node_tree.links.new(transparent.outputs[0], mix.inputs[1])
    material.node_tree.links.new(mix.outputs[0], material_output.inputs[0])
    material.node_tree.links.new(principled_bsdf.outputs[0], mix.inputs[2])
        
    #General Material Settings
    material.blend_method = 'BLEND' #Alpha Blend Blend Mode
    material.shadow_method = 'HASHED' #Alpha Hashed Shadow Mode
    #material.use_backface_culling = True #Needed for Cube, or just use below
    material.show_transparent_back = False #Needed for Cube
    

    metallic_lime = bpy.data.materials.new(name="Metallic Lime")
    metallic_lime.use_nodes = True #Required for the below cmds to work
    
    metallic_lime.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0, 1, 0.065, 1) #lIME base Color; HEX = 00FF48
    metallic_lime.node_tree.nodes["Principled BSDF"].inputs[4].default_value = 0.9 #Metallic
    metallic_lime.node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0.2 #Roughness


