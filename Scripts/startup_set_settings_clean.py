import bpy

"""First make a default Blend file and add useful common compositing nodes groups there
by selecting them and pressing ctrl + G, and tabbing out and naming it sometihng. 
Now you can add it with Ctrl + A/ Node Groups, even after you delete it.

E.g. make a vignette node group

"""

name_of_blendfile = 'PlaceholderName_1_8.3'


def DeleteCube():
    
    bpy.data.objects.remove(bpy.data.objects['Cube'])
    

def SetupEvee():
    """ 
    For faster render times, use bpy.context.scene.eevee.taa_render_samples = 16, or else use 64 
    for (default) better quality. However, 16 is probably the best needed really. It does not look 
    much better beyond this. 1 actually looks okay surprisingly, and 2 will remove most background 
    artifacts of 1 so 1 or 2 is ideal for quick renders to see how something looks with shadows 
    enabled and so forth. Of corse disable shadows and stick to 1 if quickest renders are the priority.
    """
    
    scene = bpy.data.scenes['Scene']
    
    #For major differences to rendr time, change
    scene.eevee.taa_render_samples = 16
    
    scene.eevee.use_gtao = True #Ambient Occlusion
    scene.eevee.use_bloom = True #Bloom
    scene.eevee.use_ssr = True #Screen Space Reflections
    scene.eevee.use_ssr_refraction = True    
    scene.eevee.use_ssr_halfres = False
    scene.eevee.use_motion_blur = True #Motion Blur
    scene.eevee.use_shadow_high_bitdepth = True #High Bit Depth Shadows: note diference with space plane shadow if tilted and casting shadows--the shadow won't go al the way up to the object without this enabled
    #bpy.context.scene.render.film_transparent = True #Transparency for compositing
    

def SetResolutionOutput():
    """
    Initially, 4k is used and set to 50% (so it is 1080p).
    Bump it to 100% for final renders.
    
    The scene is given 600 frames for 10 seconds @ 60 fps.
    The render output is a PNG image sequence of 16-bit color. 
    
    60 is used because dropping a frame on the T.V. every 16+ seconds is not anything 
    to worry about, and most content online is consumed digitally.
    
    Does video of different fps's get modified seamlessly so it looks okay? If I were 
    to manually do it I would just add a duplicated where one would be dropped.
    
    If 59.94 is ever desired, add setting the Base value to 1.001 with:
    bpy.context.scene.render.fps_base = 1.001
        
    """
    scene = bpy.data.scenes['Scene']
    
    scene.render.resolution_x = 3840
    scene.render.resolution_y = 2160
    scene.render.resolution_percentage = 50
    scene.frame_end = 600 
    scene.render.fps = 60 # Int only up to v3.0 . Need to set fps_base, belowm, to get 59.94.
    scene.render.fps_base = 1.0010000467300415 # The value for all fractional fps presets. Default/ non-fractional is 1.0
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_depth = '16'

    
def SetRenderLoc(file_path):
    
    scene = bpy.data.scenes['Scene']
    
    scene.render.filepath = file_path


def CreateLightsCameraCollection():    
    """Makes collection for lights and cameras and puts default ones in it"""
    
    scene = bpy.data.scenes['Scene']
    new_col = bpy.data.collections.new(name='Lights Camera') #create new collection in data

    scene.collection.children.link(new_col) #add new collection to the scene        
    
    for name in ['Light', 'Camera']:
        
        obj_old_col = bpy.data.objects[name].users_collection #list of all collections the objs in, the main scene by default
        new_col.objects.link(bpy.data.objects[name]) #link objs to new_col
        
        for ob in obj_old_col: #unlink from all previous collections
            
            ob.objects.unlink(bpy.data.objects[name])        

           
def TrackCameraToEmpty():
    
        """Set Camera Rotation to 0"""
        camera = bpy.data.objects['Camera']
                
        bpy.data.objects['Camera'].rotation_euler[0] = 0
        bpy.data.objects['Camera'].rotation_euler[1] = 0
        bpy.data.objects['Camera'].rotation_euler[2] = 0

        
        """Add and set empty"""    
        bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
        bpy.context.active_object.name = 'View Location'
        view_location = bpy.data.objects['View Location']
        view_location.scale[0] = 5
        view_location.scale[1] = 5
        view_location.scale[2] = 5

                        
        """Tracking constraint"""
        camera.constraints.new(type='TRACK_TO')
        camera.constraints["Track To"].target = bpy.data.objects["View Location"]
        camera.constraints["Track To"].track_axis = 'TRACK_NEGATIVE_Z'
        camera.constraints["Track To"].up_axis = 'UP_Y'
        
        
        """Add the View Location to 'Lights Camera' collection"""
        new_col = bpy.data.collections['Lights Camera'] #This was already created by a previous fn        
        obj_old_col = bpy.data.objects['View Location'].users_collection #list of all collections the obj is in, the main scene by default
        new_col.objects.link(bpy.data.objects['View Location']) #link obj to new_col
        
        for ob in obj_old_col: #unlink from all previous collections
            
            ob.objects.unlink(bpy.data.objects['View Location'])
        
                   
def AddSpotlightToTrackWithCamera():
                
        bpy.ops.object.light_add(type='SPOT', radius=1, location=(0, 0, 0))
        bpy.context.active_object.name = 'Camera Spotlight'
        cam_spotlight = bpy.data.objects['Camera Spotlight']
        camera = bpy.data.objects['Camera']
        
        cam_spotlight.data.energy = 1000

        """Parent to Camera"""
        cam_spotlight.parent = camera
        
        
        """Tracking constraint"""
        cam_spotlight.constraints.new(type='TRACK_TO')
        cam_spotlight.constraints["Track To"].target = bpy.data.objects["View Location"]
        cam_spotlight.constraints["Track To"].track_axis = 'TRACK_NEGATIVE_Z'
        cam_spotlight.constraints["Track To"].up_axis = 'UP_Y'    
        
        
        """Add the Spotlight to 'Lights Camera' collection"""
        new_col = bpy.data.collections['Lights Camera'] #This was already created by a previous fn        
        obj_old_col = bpy.data.objects['Camera Spotlight'].users_collection #list of all collections the obj is in, the main scene by default
        new_col.objects.link(bpy.data.objects['Camera Spotlight']) #link obj to new_col
        
        for ob in obj_old_col: #unlink from all previous collections
            
            ob.objects.unlink(bpy.data.objects['Camera Spotlight']) 
        
            
def AddMaterials():
        """
        Creates several materials, described where they are made below.
        
        Tip: When using these materials and altering them slightly, first rename it by appending 'v' + ###
        Tip: When duplicating an object with one of the materials and needing to alter it without altering
        the other objs with the material, click the shield icon to make a separate copy of the material.
        """
    
        """Creates Opacity/Transperancy Material, which may be adjusted with Factor value"""
        material = bpy.data.materials.new(name="Opacity Material")
        material.use_nodes = True

        # Get both default nodes and set color and location
        principled_bsdf = material.node_tree.nodes.get('Principled BSDF')
        principled_bsdf.inputs[0].default_value = default_value = (1.0, 0.0, 0.0, 1) #Red base Color; HEX = FF0000
        material_output = material.node_tree.nodes.get('Material Output')
        material_output.location = [600, 300] 
        
        #Add Transparency and Mix nodes
        transparent = material.node_tree.nodes.new("ShaderNodeBsdfTransparent")
        transparent.location = [-200, 450]  
        mix = material.node_tree.nodes.new("ShaderNodeMixShader")
        mix.location = [300, 450]

        # link nodes together
        material.node_tree.links.new(transparent.outputs[0], mix.inputs[1])
        material.node_tree.links.new(mix.outputs[0], material_output.inputs[0])
        material.node_tree.links.new(principled_bsdf.outputs[0], mix.inputs[2])
        
        #General Material Settings
        material.blend_method = 'BLEND' #Alpha Blend Blend Mode
        material.shadow_method = 'HASHED' #Alpha Hashed Shadow Mode
        #material.use_backface_culling = True #Needed for Cube, or just use below
        material.show_transparent_back = False #Needed for Cube
                
        """Creates Metallic Green Material"""
        metallic_green = bpy.data.materials.new(name="Metallic Green")
        metallic_green.use_nodes = True #Required for the below cmds to work
        
        bpy.data.materials["Metallic Green"].node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.000303477, 0.799103, 0.412543, 1) #Aqua greenish base Color; HEX = 01E7AC
        bpy.data.materials["Metallic Green"].node_tree.nodes["Principled BSDF"].inputs[4].default_value = 0.9 #Metallic
        bpy.data.materials["Metallic Green"].node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0.3 #Roughness

        """Creates Metallic Lime Material"""
        metallic_lime = bpy.data.materials.new(name="Metallic Lime")
        metallic_lime.use_nodes = True #Required for the below cmds to work
        
        metallic_lime.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0, 1, 0.065, 1) #lIME base Color; HEX = 00FF48
        metallic_lime.node_tree.nodes["Principled BSDF"].inputs[4].default_value = 0.9 #Metallic
        metallic_lime.node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0.2 #Roughness

        """Creates Metallic Black Material"""
        metallic_black = bpy.data.materials.new(name="Metallic Black")
        metallic_black.use_nodes = True #Required for the below cmds to work
        
        metallic_black.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0, 0, 0, 1) #Black base Color; HEX = 000000
        metallic_black.node_tree.nodes["Principled BSDF"].inputs[4].default_value = 0.8 #Metallic
        metallic_black.node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0.1 #Roughness

        """Creates Reflective Metal Material"""
        material = bpy.data.materials.new(name="Reflective Metal")
        material.use_nodes = True #Required for the below cmds to work
        
        material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1, 1, 1, 1) #Reflect; HEX = FFFFFF
        material.node_tree.nodes["Principled BSDF"].inputs[4].default_value = 1 #Metallic
        material.node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0 #Roughness

        """Creates Space Black Material"""
        material = bpy.data.materials.new(name="Space Black")
        material.use_nodes = True #Required for the below cmds to work
        
        material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.184, 0.184, 0.184, 1) #Grey; HEX = 777777
        material.node_tree.nodes["Principled BSDF"].inputs[4].default_value = 0.99 #Metallic
        material.node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0.01 #Roughness

        """Creates refrigerator white material, highly optional for letters"""
        fridge = bpy.data.materials.new(name="Fridge White")
        fridge.use_nodes = True #Required for the below cmds to work
        
        fridge.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.98, 0.98, 0.98, 1) #White base Color; HEX = EEEEEE
        fridge.node_tree.nodes["Principled BSDF"].inputs[4].default_value = 0.3 #Metallic
        fridge.node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0.2 #Roughness

        """Creates gold material"""
        gold = bpy.data.materials.new(name="Gold")
        gold.use_nodes = True #Required for the below cmds to work
        
        gold.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.98, 0.98, 0.98, 1) #Gold base Color; HEX = E7C989
        gold.node_tree.nodes["Principled BSDF"].inputs[4].default_value = 1 #Metallic
        gold.node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0.444 #Roughness

        """Creates Basic Primary Colors Materials"""
        red = bpy.data.materials.new(name="Red")
        green = bpy.data.materials.new(name="Green")
        blue = bpy.data.materials.new(name="Blue")
        
        red.use_nodes = True #Required for the below cmds to work
        green.use_nodes = True #Required for the below cmds to work
        blue.use_nodes = True #Required for the below cmds to work
        
        red.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1, 0, 0, 1) #HEX = FF0000
        green.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0, 1, 0, 1)  #HEX = 00FF00
        blue.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0, 0, 1, 1) #HEX = 0000FF


def AddCubesForMaterials():    
    """Give all above materials an object so they remain after save/quit/reload and may be copied 
    in their original form to other objects and modified from there"""
    
    scene = bpy.data.scenes['Scene']
    
    new_col = bpy.data.collections.new(name='Material Cubes') #create new collection in data
    scene.collection.children.link(new_col) #add new collection to the scene  
    
    material_names = (
        'Opacity Material', 
        'Metallic Green', 
        'Metallic Lime', 
        'Metallic Black', 
        'Reflective Metal', 
        'Space Black', 
        'Fridge White', 
        'Gold', 
        'Red', 
        'Green', 
        'Blue',
        )
    
    start_x = -5
    increment = 0.5
    count = 0
    
    for material_name in material_names:
    
        name = material_name + ' Cube'    
        bpy.ops.mesh.primitive_cube_add(size=.25, enter_editmode=False, location=(start_x + (increment * count), -1, 0))
        bpy.context.active_object.name = name
        bpy.data.objects[name].location[2] = 0.25
        bpy.data.objects[name].active_material = bpy.data.materials[material_name]
        
        """Add Cube to new col"""        
        obj_old_col = bpy.data.objects[name].users_collection #list of all collections the obj is in, the main scene by default

        for ob in obj_old_col: #unlink from all previous collections
            
            ob.objects.unlink(bpy.data.objects[name])  

        new_col.objects.link(bpy.data.objects[name]) #link obj to new_col    
        
        count += 1


def AddReflectiveSphere():
    
    name = 'Reflective Sphere'
    
    bpy.ops.mesh.primitive_uv_sphere_add(segments=128, ring_count=128, radius=0.5, enter_editmode=False, location=(3, -3, 1))
        
    bpy.ops.object.shade_smooth() #Looked around but unsure how to non-complicatedly do this by accessing object data directly

    bpy.context.active_object.name = name
    bpy.data.objects[name].active_material = bpy.data.objects['Reflective Metal Cube'].active_material.copy()
    
 
def AddSpacePlane():
    
    name = 'Space Plane'
    
    bpy.ops.mesh.primitive_plane_add(size=3, enter_editmode=False, align='WORLD', location=(-10, -10, 1.5), rotation=(0, 1.5708, -0.5))
    bpy.context.active_object.name = name
    bpy.data.objects[name].active_material = bpy.data.objects['Space Black Cube'].active_material.copy()


#####################################################################################
#####################################################################################
#####################################################################################

def AddBezierPaths():
    
    bezier_name = 'Squiggle' 
    point_1_loc = [0,9,0] 
    point_2_loc = [5,4,0] 
    point_3_loc = [0,0,0] 
    sub_div = 0
    
    bpy.ops.curve.primitive_bezier_curve_add(radius=1, enter_editmode=False, location=(0, 0, 0))
    bpy.context.active_object.name = bezier_name
    
    bezier_obj = bpy.data.objects[bezier_name]
    
    for ob in bpy.context.selected_objects: #Deselect any selected objects
            
        bpy.data.objects[ob.name].select_set(False)
            
    bezier_obj.select_set(True) #Select bexier_obj                
    bpy.context.view_layer.objects.active = bezier_obj #Sets the active object to be bezier_obj, needed below         
 
    
    #bpy.ops.object.editmode_toggle() #might not be needed depending on how I move vertex below

    #bpy.ops.transform.translate(value=(1, 0, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

    #bpy.ops.transform.translate(value=(1, 0, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

    bpy.ops.object.editmode_toggle()
    #bpy.ops.curve.extrude_move(CURVE_OT_extrude={"mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(-5, 5, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
    #bpy.ops.curve.switch_direction()
    #bpy.ops.object.editmode_toggle()
    
    bpy.ops.curve.select_all() #On creation, both verteces are selected by defualt, this deselects them all (This will also deselect all if less than all are selected, a bit unintuitive)
    bpy.ops.curve.de_select_first() #Example of inconsistent naming scheme -- this will select the first since nothing is selected (naming should be 'toggle_select')
    
    
    """Place starting point"""
    bpy.ops.transform.translate(value=(point_1_loc[0]+1, point_1_loc[1], point_1_loc[2]), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

    bpy.data.objects[bezier_name].data.splines[0].bezier_points[0].handle_left=[point_1_loc[0]-1,point_1_loc[1]+1,0]
    bpy.data.objects[bezier_name].data.splines[0].bezier_points[0].handle_right=[point_1_loc[0]-1,point_1_loc[1]-1.5,0]
    
    bpy.ops.curve.de_select_first() #Actually does what it is named in this case
    bpy.ops.curve.de_select_last() #Selects last (last should be the only one selected)
    
    """Place second point"""
    bpy.ops.transform.translate(value=(point_2_loc[0]-1, point_2_loc[1], point_2_loc[2]), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
    
    bpy.data.objects[bezier_name].data.splines[0].bezier_points[1].handle_left=[point_2_loc[0],point_2_loc[1]+2,0]
    bpy.data.objects[bezier_name].data.splines[0].bezier_points[1].handle_right=[point_2_loc[0],point_2_loc[1]-2,0]
    
    """Extrude final point"""
    #When extruding, the old point extruded from is deselected and the new point selected
    
    #We need to use the location of the second point to calculate where to extrude to in 
    #order to get to the final point loc
    
    #point_2_loc=[5,4,0]    
    #point_3_loc=[0,0,0]
    
    move_to_point_3_x = point_3_loc[0] - point_2_loc[0]
    move_to_point_3_y = point_3_loc[1] - point_2_loc[1]
    move_to_point_3_z = point_3_loc[2] - point_2_loc[2]       
    
    bpy.ops.curve.extrude_move(CURVE_OT_extrude={"mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(move_to_point_3_x, move_to_point_3_y, move_to_point_3_z), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

    bpy.data.objects[bezier_name].data.splines[0].bezier_points[2].handle_left=[point_3_loc[0],point_3_loc[1]+1,0]
    bpy.data.objects[bezier_name].data.splines[0].bezier_points[2].handle_right=[point_3_loc[0],point_3_loc[1]-1,0]
    

    #bpy.ops.transform.translate(value=(0, 0, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
    
    
    for i in range(0, sub_div):
        bpy.ops.curve.select_all() #Deselects last point
        bpy.ops.curve.select_all() #Selects all
        bpy.ops.curve.subdivide()
        
        
       
    
    bpy.ops.object.editmode_toggle()


def RepeatExtrudeSelectedBezier():
    
    """Kinda neat, this will basically grow the selcted curve each time this is run"""
    
    pass

    bpy.ops.object.editmode_toggle()

    ##Insert bpy.ops.curve.extrude_move(...) cmd here! Select curve, remove above pass, run script w/this fn

    bpy.ops.object.editmode_toggle()
    

"""In edit mode, just have at least one of the vertex points selected and
 run this to reverse the direction of whole line """ 
#bpy.ops.curve.switch_direction()    

""" Translate obj. Useful?"""
#bpy.ops.transform.translate(value=(1, 0, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)


"""
BackToFrontCurvyPath()
BackToFrontCurvyPath('Squigglez', [0, 9, 0], [5,4,0], [0,0,-6], 2)
BackToFrontCurvyPath('Squigglez2', [0, 9, 0], [5,4,0], [0,0,-15], 3)
BackToFrontCurvyPath('SquiggleAnti', [0,9,0], [-5,4,0], [0,0,0])

"""

#BackToFrontCurvyPath('LettersPathwayTest', [3,0,1], [-0.25,0,0], [0,0,0]) #After add a subdiv between the two longest points

########################################################################################
########################################################################################
########################################################################################    



"""I am here converting context calls to data calls.


Watch the video on the popup dialogue box. 



"""

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
        
    material.node_tree.links.new(emission.outputs[0], material_output.inputs[0])
    
    """Add Sphere with Above Material"""

    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=32, radius=0.1, enter_editmode=False, location=(-3, -3, 1))
        
    bpy.ops.object.shade_smooth()


    bpy.context.active_object.name = name
    bpy.data.objects[name].active_material = material
        
        
    """Creates Neon Pink Emission Material"""
    
        
    name = 'Neon Pink Sphere'
    names += [name]
    
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True #Required for the below cmds to work
    
    principled_bsdf = material.node_tree.nodes.get('Principled BSDF')
    material_output = material.node_tree.nodes.get('Material Output')
    material.node_tree.nodes.remove(principled_bsdf)
    
    emission = material.node_tree.nodes.new("ShaderNodeEmission")
        
    emission.inputs[0].default_value = (1, 0, 0.89, 1) #Grey; HEX = FFFF00
    emission.inputs[1].default_value = 20 #Strength
    #emission.inputs[7].default_value = 0.01 #Roughness
    
    material.node_tree.links.new(emission.outputs[0], material_output.inputs[0])
    
    """Add Sphere with Above Material"""
    
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=32, radius=0.1, enter_editmode=False, location=(-3, -3, 2))
        
    bpy.ops.object.shade_smooth()


    bpy.context.active_object.name = name
    bpy.data.objects[name].active_material = material
    
            
    """Creates Neon Blue Emission Material"""
    
        
    name = 'Neon Blue Sphere'
    names += [name]
    
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True #Required for the below cmds to work
    
    principled_bsdf = material.node_tree.nodes.get('Principled BSDF')
    material_output = material.node_tree.nodes.get('Material Output')
    material.node_tree.nodes.remove(principled_bsdf)
    
    emission = material.node_tree.nodes.new("ShaderNodeEmission")
        
    emission.inputs[0].default_value = (0, 1, 1, 1) #Grey; HEX = 00FFFF
    emission.inputs[1].default_value = 20 #Strength
    #emission.inputs[7].default_value = 0.01 #Roughness
    
    material.node_tree.links.new(emission.outputs[0], material_output.inputs[0])
    
    """Add Sphere with Above Material"""
    
    
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=32, radius=0.1, enter_editmode=False, location=(-3, -3, 3))
        
    bpy.ops.object.shade_smooth()


    bpy.context.active_object.name = name
    bpy.data.objects[name].active_material = material
    
        
    """Add these Emission Sphere to their own collection"""
    
    new_col = bpy.data.collections.new(name='Neon Spheres') #create new collection in data
    bpy.context.scene.collection.children.link(new_col) #add new collection to the scene  
    
    for name in names:
        
    
        obj_old_col = bpy.data.objects[name].users_collection #list of all collections the txt_obj is in, the main scene by default

        for ob in obj_old_col: #unlink from all previous collections
            
            ob.objects.unlink(bpy.data.objects[name])  


        new_col.objects.link(bpy.data.objects[name])
        

def AddLights():
    """Add some lights with distinctive neon glows
    
    Add them to the 'Lights Camera' colection once added"""
    
    
    """Add Pink Area Light"""
    bpy.ops.object.light_add(type='AREA', radius=5, location=(5, 5, 0))

    bpy.context.active_object.name = 'Neon Pink'
    
    obj = bpy.data.objects['Neon Pink']
    
    obj.rotation_euler = (-0.0, 1.570796251296997, 0.0)
    obj.data.color = (1, 0, 0.89) #Hot Pink, HEX = FF00A9
    obj.data.energy = 50   
    obj.data.specular_factor = 7 #Try playing with this more, the effect is seemingly more bloom; used to be 2; default is 1
    
    """Add Blue Area Light"""
    bpy.ops.object.light_add(type='AREA', radius=5, location=(-5, 5, 0))

    bpy.context.active_object.name = 'Neon Blue'
    
    obj = bpy.data.objects['Neon Blue']
    
    obj.rotation_euler = (-0.0, -1.570796251296997, 0.0)
    obj.data.color = (0, 0.05, 1) #Hot Pink, HEX = FF00A9
    obj.data.energy = 50  
    obj.data.specular_factor = 7 #Try playing with this more, the effect is seemingly more bloom; used to be 2; default is 1

    """Add White Area Light"""
    bpy.ops.object.light_add(type='AREA', radius=5, location=(5, 0, 0))

    bpy.context.active_object.name = 'White'
    
    obj = bpy.data.objects['White']
    
    obj.rotation_euler = (-0.0, 1.570796251296997, 0.0)
    obj.data.color = (1, 1, 1)
    obj.data.energy = 50
    obj.data.specular_factor = 7 #Try playing with this more, the effect is seemingly more bloom; used to be 2; default is 1


    """Add Bright Yellow Point Light"""
    bpy.ops.object.light_add(type='POINT', radius=1, location=(-10, 10, 10))
    
    
    bpy.context.active_object.name = 'Bright Yellow' 
    obj = bpy.data.objects['Bright Yellow']
    
    obj.data.color[2] = 0
    obj.data.color = (1, 1, 0)
    obj.data.energy = 10000
    
    """Add a Red Sun Light, Just to Play With World Colors"""
    
    bpy.ops.object.light_add(type='SUN', location=(0, 0, 5))
    
    bpy.context.active_object.name = 'Sun' 
    obj = bpy.data.objects['Sun']
    
    obj.data.color = (1, 0, 0)
    obj.data.energy = 50


    
    """Add the lights to 'Lights Camera' collection"""
    for name in ['Neon Pink', 'Neon Blue', 'White', 'Bright Yellow', 'Sun']:
        new_col = bpy.data.collections['Lights Camera'] #This was already created by a previous fn        
        obj_old_col = bpy.data.objects[name].users_collection #list of all collections the txt_obj is in, the main scene by default
        new_col.objects.link(bpy.data.objects[name]) #link txt_obj to new_col
        
        for ob in obj_old_col: #unlink from all previous collections
            
            ob.objects.unlink(bpy.data.objects[name])        
                
    
def AddGreenMatallicFloor():
    """Relies on above fn for its material"""
    
    bpy.ops.mesh.primitive_plane_add(size=40, enter_editmode=False, location=(0, 0, 0))
    bpy.context.active_object.name = 'Floor'
    bpy.data.objects['Floor'].active_material = bpy.data.objects['Metallic Green Cube'].material_slots[0].material.copy()
    

    """    
    if len(obj.data.vertices) == 0: #This also allows for blank spaces, with little added cost, besides several more assignments; better here in case this is called in the future                

        return None
    """
    
    obj = bpy.data.objects['Floor']
    
    
    #bpy.ops.object.mode_set(mode = 'OBJECT')
    #obj = bpy.context.active_object
    #bpy.ops.object.mode_set(mode = 'EDIT') 
    
    bpy.ops.object.editmode_toggle() #Get into Edit Mode, needed to properly deselect verts
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.mesh.select_all(action = 'DESELECT')
    
    #bpy.ops.object.mode_set(mode = 'OBJECT')
    
    bpy.ops.object.editmode_toggle() #Back into Object Mode, needed to properly select the verts (weird!)
    
    for vert in obj.data.vertices:
        
        if vert.co[1] == 20:
                    
            vert.select = True
    
    bpy.ops.object.editmode_toggle() #Back into Edit Mode, in order to extrude the selected verts (this makes sense since extrude is regularly performed in edit mode)
    #bpy.ops.object.mode_set(mode = 'EDIT') 
    
    """
                                                                          
    obj_start_vert = obj.data.vertices[0].co[0]  #Vertices[0] is just the first vertice, and .co[0] signifies location value of the x-axis               
    top_y_verts = obj_start_vert #Starting data to compare
                                  
    for vert in obj.data.vertices: #Update leftmost verts that are found more left
    
        if vert.co[0] < leftmost_vert:
                            
            leftmost_vert = vert.co[0]
                    
    leftmost_verts += [leftmost_vert] #Add to the lst
                                               
    return  [names_with_verts, leftmost_verts]                
    """
        
    bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, 20), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

    #Deselect verts again while in Edit Mode
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.mesh.select_all(action = 'DESELECT')
    
        
    bpy.ops.object.editmode_toggle() #Back into Object Mode, needed to properly select the verts again (weird! . . . again)
    
    for vert in obj.data.vertices:
        
        if vert.co[1] == 20 and vert.co[2] == 0:
                    
            vert.select = True
    
    bpy.ops.object.editmode_toggle() #Back into Edit Mode, in order to extrude the selected verts (this makes sense since extrude is regularly performed in edit mode)
    
    # vertex_only parameter not recognized in version 9.0
    #bpy.ops.mesh.bevel(offset=1, offset_pct=0, segments=7, vertex_only=False)
    bpy.ops.mesh.bevel(offset=1, offset_pct=0, segments=7)
    
    
    bpy.ops.object.editmode_toggle() #Back into object mode to shade the bevel smooth
    bpy.ops.object.shade_smooth()


    print("Floor Created!")
    
def AddHDRITwinklyStars(path_to_hdri):
    
    """Creates full nodes from scratch; the below fn will instead try to create node groups to make controls more
    salient
    
    Tip: use 1st RGB curves to make stars brighter, play with saturation in Hue/Sat node, use the 2nd RBG curves 
    to decrease green and increase blue.
    Can also change these thorughout video according to mood: e.g., all red stars
    
    Also, duplicate the bottom row, change the z rotation so the stars are clearly different (200 worked well), 
    and plug it into another mix node to add more stars (These won't twinkle unless you plug in the twinkly bit 
    into it, but this may be undesireable). Do this as many times as desired, but once makes a crazy amount anyway. 
    
    To animate, only a little variation on the z location is needed. Have keyframes repeat 0 to 0.05 (at frame 300),
    then back to 0 at frame 600, and just loop this.     
    """
    
    #Use for help getting correct name of nodes to add: bpy.context.scene.world.node_tree.nodes[4].bl_idname
    #To change values use node.inputs[1].default_value[1] = 1    
         
    world = bpy.context.scene.world
    #world = bpy.data.scenes['Scene.001'].world #Was trying to add a scene with JUST the HDRI and this didn't work.
    world.use_nodes = True
    
    hdri_node = world.node_tree.nodes.new("ShaderNodeTexEnvironment") #OLD
    hdri_node.location= (-900, -100)
    hdri_node.image = bpy.data.images.load(path_to_hdri)
    
    node_tree = bpy.context.scene.world.node_tree

    node_tree.links.new(hdri_node.outputs['Color'], node_tree.nodes['Background'].inputs['Color']) 
    
    text_coord = world.node_tree.nodes.new("ShaderNodeTexCoord")
    text_coord.location = (-1300, -100)    
    mapping = world.node_tree.nodes.new("ShaderNodeMapping")
    mapping.location = (-1100, -100)
    
    mapping.inputs['Location'].default_value[2] = 0.6 #Z location
    mapping.inputs['Rotation'].default_value[2] = 1.22173 #Z rotation
    

    
    rgb_bw = world.node_tree.nodes.new("ShaderNodeRGBToBW")
    rgb_bw.location = (-500, -100)
    rgb_curve = world.node_tree.nodes.new("ShaderNodeRGBCurve")
    rgb_curve.location = (-300, -100)
    #bkgrnd = world.node_tree.nodes.get("ShaderNodeBackground")
    bkgrnd = world.node_tree.nodes[1] #Avoids a false Nonetype error given when using the above and linking to its input instead
    bkgrnd.location = (50, 50)
    output_wrld = world.node_tree.nodes[0]
    output_wrld.location = (900, 300)
    
    #rgb_curve points
    curve_c = rgb_curve.mapping.curves[3]
    curve_c.points.new(.459,.037) #Original: .677,.144
    curve_c.points.new(.905,.575) #Original: .777,.912
    
    node_tree.links.new(text_coord.outputs['Generated'], mapping.inputs['Vector']) 
    node_tree.links.new(mapping.outputs['Vector'], hdri_node.inputs['Vector'])     
    node_tree.links.new(hdri_node.outputs['Color'], rgb_bw.inputs['Color'])
    node_tree.links.new(rgb_bw.outputs['Val'], rgb_curve.inputs['Color']) 
    
    #In case I need to first remove a link between two nodes (I havene't had to in order to make new links)
    #link = bkgrnd.inputs[0].links[0]
    #node_tree.links.remove(link)
    
    #node_tree.links.new(rgb_curve.outputs['Color'], bkgrnd.inputs[0])
    #node_tree.links.new(rgb_curve.outputs['Color'], bkgrnd.inputs['Color']) 
    
    noise_txtr = world.node_tree.nodes.new("ShaderNodeTexNoise")    
    noise_txtr.location = (300, -100)
    magic_txtr = world.node_tree.nodes.new("ShaderNodeTexMagic")
    magic_txtr.location = (500, -100)
    bright_cntr = world.node_tree.nodes.new("ShaderNodeBrightContrast")
    bright_cntr.location = (700, -100)
    hue_sat = world.node_tree.nodes.new("ShaderNodeHueSaturation")
    hue_sat.location = (900, -100)
    rgb_curve_b = world.node_tree.nodes.new("ShaderNodeRGBCurve")
    rgb_curve_b.location = (1100, -100) 
    color = world.node_tree.nodes.new("ShaderNodeMixRGB")
    color.location = (1400, -100)
    
    noise_txtr.inputs['Scale'].default_value = 11.0
    noise_txtr.inputs['Detail'].default_value = 7.8
    noise_txtr.inputs['Distortion'].default_value = 7.4
    
    magic_txtr.inputs['Scale'].default_value = -0.6
    magic_txtr.inputs['Distortion'].default_value = 2.4
    
    bright_cntr.inputs['Contrast'].default_value = 2.2
    hue_sat.inputs['Saturation'].default_value = 1 #Play with this for better color effects. Old val 10.0
    
    #rgb_curve_b points
    curve_c = rgb_curve_b.mapping.curves[1] #Green
    #curve_c.points.new(1.0,0.05625) #Helps bring down green quite a bit OOPS don't make a new point,use one there
    curve_c.points[1].location = (1.0,0.05625) #Helps bring down green quite a bit
    curve_c = rgb_curve_b.mapping.curves[2] #Blue
    #curve_c.points.new(1.0,0.5) #Halves blue OOPS don't make a new point, use one there
    curve_c.points[1].location = (1.0,0.5) #Halves blue
    
    
    #???bpy.data.worlds["World"].node_tree.nodes["RGB Curves.001"].inputs[0].default_value = 0.372727
    rgb_curve_b.inputs[0].default_value = 1 #Old val: 0.372727 -- but why?

    
    color.inputs['Fac'].default_value = 0.5 #Saturation OLD val 0.7
    color.inputs['Color1'].default_value[0] = 1.0
    color.inputs['Color1'].default_value[1] = 1.0
    color.inputs['Color1'].default_value[2] = 1.0
    color.blend_type = 'COLOR'     
    
    #node_tree.links.new(group_a.inputs[0], magic_txtr.inputs['Vector']) 
    node_tree.links.new(noise_txtr.outputs['Color'], magic_txtr.inputs['Vector']) 
    node_tree.links.new(magic_txtr.outputs['Color'], bright_cntr.inputs['Color']) 
    node_tree.links.new(bright_cntr.outputs['Color'], hue_sat.inputs['Color']) 
    node_tree.links.new(hue_sat.outputs['Color'], rgb_curve_b.inputs['Color']) 
    node_tree.links.new(rgb_curve_b.outputs['Color'], color.inputs['Color2']) 
    node_tree.links.new(rgb_curve.outputs['Color'], color.inputs['Color1']) 
    node_tree.links.new(color.outputs['Color'], bkgrnd.inputs['Color'])
    #node_tree.links.new(hdri_node.outputs['Color'], rgb_bw.inputs['Color']) 
    #node_tree.links.new(rgb_bw.outputs['Val'], rgb_curve.inputs['Color']) 
    
    
    bkgrnd_b = world.node_tree.nodes.new("ShaderNodeBackground")
    bkgrnd_b.location = (-100, 50)
    mix_shdr = world.node_tree.nodes.new("ShaderNodeMixShader")
    mix_shdr.location = (300, 300)
    mix_shdr_b = world.node_tree.nodes.new("ShaderNodeMixShader") #My addition to keep part of the noise+magic texture
    mix_shdr_b.location = (700, 300)
    text_coord_b = world.node_tree.nodes.new("ShaderNodeTexCoord")
    text_coord_b.location = (-900, 400)    
    mapping_b = world.node_tree.nodes.new("ShaderNodeMapping")
    mapping_b.location = (-700, 400)
    noise_txtr_b = world.node_tree.nodes.new("ShaderNodeTexNoise")    
    noise_txtr_b.location = (-500, 400)
    color_rmp = world.node_tree.nodes.new("ShaderNodeValToRGB")
    color_rmp.location = (-300, 400)
    
    bkgrnd_b.inputs['Color'].default_value[0] = 0
    bkgrnd_b.inputs['Color'].default_value[1] = 0
    bkgrnd_b.inputs['Color'].default_value[2] = 0
    #mix_shdr_b.inputs['Fac'].default_value = 0.0007
    mix_shdr_b.inputs['Fac'].default_value = 0.0005 #Ever so slight distortion/artifacts from magic texture
    mapping_b.inputs['Location'].default_value[2] = 900 #Z location, keyframe this to .5 over about 5 seconds, but should experiment too; I think fast flickering could be cool
    mapping_b.inputs['Location'].default_value[1] = 900 
    mapping_b.inputs['Location'].default_value[0] = 900
    noise_txtr_b.inputs['Scale'].default_value = 5.2
    noise_txtr_b.inputs['Detail'].default_value = 2.0
    noise_txtr_b.inputs['Distortion'].default_value = 120 #OLD val: 4.2
    color_rmp.color_ramp.elements[0].color = (1,1,1,1)
    color_rmp.color_ramp.elements[1].color = (0,0,0,1)
    #color_rmp.color_ramp.elements[0].position = 0.21 #Val from video: 0.21    
    #color_rmp.color_ramp.elements[1].position = 0.7 #Val from video: 0.534
    color_rmp.color_ramp.elements[0].position = 0.0
    color_rmp.color_ramp.elements[1].position = 0.6
    
    #color_rmp.inputs['Distortion'].default_value = 4.2
    #color_rmp.inputs['Distortion'].default_value = 4.2
    #curve_c = rgb_curve.mapping.curves[3]
    #curve_c.points.new(.677,.144)
    #curve_c.points.new(.777,.912)
    
    node_tree.links.new(bkgrnd_b.outputs['Background'], mix_shdr.inputs['Shader'])
    node_tree.links.new(mix_shdr.outputs['Shader'], mix_shdr_b.inputs['Shader'])
    node_tree.links.new(mix_shdr_b.outputs['Shader'], output_wrld.inputs['Surface'])
    node_tree.links.new(bkgrnd.outputs['Background'], mix_shdr.inputs[2]) #Funny, this input has the same name 'Shader' so instead I need to use its index    
    node_tree.links.new(hue_sat.outputs['Color'], mix_shdr_b.inputs[2]) #Funny, this input has the same name 'Shader' so instead I need to use its index    
    node_tree.links.new(text_coord_b.outputs['Generated'], mapping_b.inputs['Vector']) 
    node_tree.links.new(mapping_b.outputs['Vector'], noise_txtr_b.inputs['Vector'])
    node_tree.links.new(noise_txtr_b.outputs['Fac'], color_rmp.inputs['Fac'])
    node_tree.links.new(color_rmp.outputs['Color'], mix_shdr.inputs['Fac'])
    
    
    #bpy.ops.anim.change_frame(frame=0)
    bpy.context.scene.frame_set(0)
    #mapping_b.keyframe_insert(data_path="location")
    mapping_b.inputs['Location'].keyframe_insert(data_path="default_value")
    #bpy.ops.anim.change_frame(frame=60000)
    bpy.context.scene.frame_set(60000)
    
    #.keyframe_insert(data_path="", frame=0)
    
    mapping_b.inputs['Location'].default_value[2] = 1000
    mapping_b.inputs['Location'].default_value[1] = 1000
    mapping_b.inputs['Location'].default_value[0] = 1000
    
    #mapping_b.keyframe_insert(data_path="location")
    mapping_b.inputs['Location'].keyframe_insert(data_path="default_value")
    
    

    
    #bpy.data.worlds["World"].node_tree.nodes["Mapping.001"].inputs[2].default_value[2] = 0.0349066

    
    """"""
    
    
    #From here, maybe make this into his own Group Node
    #keyframe the z-axis of the second mapping node, btw. 0 and 1 is good per 5-10 seconds
    #The main controls are color fac, to make stars more/less colorful,
    #RGB curves for how much of original image to include and brighten
    #color_rmp positions and values for how dark/bright range stars will be
    #fac on the final mix shader
    
    #Oh, and probably disable the space plane or else shrink it or w/e, make small copies and put them around,
    #same for lights
    
def AddHDRITwinklyStarsNodeGroup(path_to_hdri):
    
    """This should match the above fn, except that it uses a node group to better highlight the variables you 
    can play with. Tips are repeated from the above fn:
    
    Tip: use 1st RGB curves to make stars brighter, use the 2nd RBG curves to decrease green and increase blue.
    Can also change these thorughout video according to mood: e.g., all red stars
    
    Also, duplicate the bottom row, change the z rotation so the stars are clearly different (200 worked well), 
    and plug it into another mix node to add more stars (These won't twinkle unless you plug in the twinkly bit 
    into it, but this may be undesireable). Do this as many times as desired, but once makes a crazy amount anyway. 
    
    To animate, only a little variation on the z location is needed. Have keyframes repeat 0 to 0.05 (at frame 300),
    then back to 0 at frame 600, and just loop this. 
       
    """
    
    #Use for help getting correct name of nodes to add: bpy.context.scene.world.node_tree.nodes[4].bl_idname
    #To change values use node.inputs[1].default_value[1] = 1    
    
    
    world = bpy.context.scene.world
    world.use_nodes = True
    
    hdri_node = world.node_tree.nodes.new("ShaderNodeTexEnvironment") #OLD
    hdri_node.location= (-900, -100)
    hdri_node.image = bpy.data.images.load(path_to_hdri)
    
    node_tree = bpy.context.scene.world.node_tree

    #node_tree.links.new(hdri_node.outputs['Color'], node_tree.nodes['Background'].inputs['Color']) 
    
    text_coord = world.node_tree.nodes.new("ShaderNodeTexCoord")
    text_coord.location = (-1300, -100)    
    mapping = world.node_tree.nodes.new("ShaderNodeMapping")
    mapping.location = (-1100, -100)
    
    mapping.inputs['Location'].default_value[2] = 0.6 #Z location
    mapping.inputs['Rotation'].default_value[2] = 1.22173 #Z rotation
    

  


    rgb_bw = world.node_tree.nodes.new("ShaderNodeRGBToBW")
    rgb_bw.location = (-500, -100)
    rgb_curve = world.node_tree.nodes.new("ShaderNodeRGBCurve")
    rgb_curve.location = (-300, -100)
    #bkgrnd = world.node_tree.nodes.get("ShaderNodeBackground")
    bkgrnd = world.node_tree.nodes[1] #Avoids a false Nonetype error given when using the above and linking to its input instead
    bkgrnd.location = (50, 50)
    output_wrld = world.node_tree.nodes[0]
    output_wrld.location = (900, 300)
       
    curve_c = rgb_curve.mapping.curves[3]
    curve_c.points.new(.459,.037) #Original: .677,.144
    curve_c.points.new(.905,.575) #Original: .777,.912
    
    node_tree.links.new(text_coord.outputs['Generated'], mapping.inputs['Vector']) 
    node_tree.links.new(mapping.outputs['Vector'], hdri_node.inputs['Vector'])     
    node_tree.links.new(hdri_node.outputs['Color'], rgb_bw.inputs['Color'])
    node_tree.links.new(rgb_bw.outputs['Val'], rgb_curve.inputs['Color']) 

    #bkgrnd = world.node_tree.nodes.get("ShaderNodeBackground")
    bkgrnd = world.node_tree.nodes[1] #Avoids a false Nonetype error given when using the above and linking to its input instead
    bkgrnd.location = (50, 50)
    output_wrld = world.node_tree.nodes[0]
    output_wrld.location = (900, 300)
       
    curve_c = rgb_curve.mapping.curves[3]
    curve_c.points.new(.459,.037) #Original: .677,.144
    curve_c.points.new(.905,.575) #Original: .777,.912
    
    node_tree.links.new(text_coord.outputs['Generated'], mapping.inputs['Vector']) 
    node_tree.links.new(mapping.outputs['Vector'], hdri_node.inputs['Vector'])     
    node_tree.links.new(hdri_node.outputs['Color'], rgb_bw.inputs['Color'])
    node_tree.links.new(rgb_bw.outputs['Val'], rgb_curve.inputs['Color']) #OLD w/o node group

    
    """Create Groups and their input and output nodes"""    
    
    
    starry_grp = bpy.data.node_groups.new('StarControls', 'ShaderNodeTree')


    # create group inputs
    starry_grp_inputs = starry_grp.nodes.new('NodeGroupInput')
    starry_grp_inputs.location = (-500, 0)

    # create group outputs

    starry_grp_outputs = starry_grp.nodes.new('NodeGroupOutput')
    starry_grp_outputs.location = (1300, 300)
    #test_group.outputs.new('NodeSocketFloat','out_result')
    
    starry_grp.inputs.new('NodeSocketColor','Color')
    starry_grp.inputs.new('NodeSocketFloat','Color Amnt')
    starry_grp.inputs.new('NodeSocketFloat','Galaxy Amnt')
    starry_grp.inputs.new('NodeSocketFloat','Animate Z Loc')
    starry_grp.inputs.new('NodeSocketShader','Bkg Shader')

    #starry_grp.inputs[0].name = 'Color' #Can also rename like this
    
        
    #Set min/max/default values 
    input = bpy.data.node_groups["StarControls"].inputs['Color Amnt']
    input.min_value     = 0.0
    input.max_value     = 1.0
    input.default_value = 0.7    
    input = bpy.data.node_groups["StarControls"].inputs['Galaxy Amnt']
    input.min_value     = 0.0
    input.max_value     = 1.0
    input.default_value = 0.001
    input = bpy.data.node_groups["StarControls"].inputs['Animate Z Loc']
    input.min_value     = 0.0
    input.max_value     = 10.0
    input.default_value = 0.0

    

    # create group outputs
    #group_outputs = test_group.nodes.new('NodeGroupOutput')
    #group_outputs.location = (300,0)
    starry_grp.outputs.new('NodeSocketColor','Color')
    starry_grp.outputs.new('NodeSocketShader','Shader')
    

    ## link input
    #new_group.links.new(group_inputs.outputs[0], color_rmp.inputs[0])
    #test_group.links.new(group_inputs.outputs['in_to_less'], node_less.inputs[0])
    ##link output
    #new_group.links.new(color_rmp.outputs[0], group_outputs.inputs[0])

        
 

    
    #In case I need to first remove a link between two nodes (I havene't had to in order to make new links)
    #link = bkgrnd.inputs[0].links[0]
    #node_tree.links.remove(link)
    
    #node_tree.links.new(rgb_curve.outputs['Color'], bkgrnd.inputs[0])
    #node_tree.links.new(rgb_curve.outputs['Color'], bkgrnd.inputs['Color']) 
    
    noise_txtr = starry_grp.nodes.new("ShaderNodeTexNoise")    
    noise_txtr.location = (300, -100)
    magic_txtr = starry_grp.nodes.new("ShaderNodeTexMagic")
    magic_txtr.location = (500, -100)
    bright_cntr = starry_grp.nodes.new("ShaderNodeBrightContrast")
    bright_cntr.location = (700, -100)
    hue_sat = starry_grp.nodes.new("ShaderNodeHueSaturation")
    hue_sat.location = (900, -100)
    rgb_curve_b = starry_grp.nodes.new("ShaderNodeRGBCurve")
    rgb_curve_b.location = (1100, -100)    
    color = starry_grp.nodes.new("ShaderNodeMixRGB")
    color.location = (1400, -100)
    
    noise_txtr.inputs['Scale'].default_value = 11.0
    noise_txtr.inputs['Detail'].default_value = 7.8
    noise_txtr.inputs['Distortion'].default_value = 7.4
    
    magic_txtr.inputs['Scale'].default_value = -0.6
    magic_txtr.inputs['Distortion'].default_value = 2.4
    
    bright_cntr.inputs['Contrast'].default_value = 2.2
    hue_sat.inputs['Saturation'].default_value = 10.0
    
    color.inputs['Fac'].default_value = 0.7
    color.inputs['Color1'].default_value[0] = 1.0
    color.inputs['Color1'].default_value[1] = 1.0
    color.inputs['Color1'].default_value[2] = 1.0
    color.blend_type = 'COLOR'     
    
    #node_tree.links.new(group_a.inputs[0], magic_txtr.inputs['Vector']) 
    starry_grp.links.new(starry_grp_inputs.outputs[0], color.inputs['Color1']) 
    starry_grp.links.new(starry_grp_inputs.outputs[1], color.inputs['Fac']) 
    starry_grp.links.new(noise_txtr.outputs['Color'], magic_txtr.inputs['Vector']) 
    starry_grp.links.new(magic_txtr.outputs['Color'], bright_cntr.inputs['Color']) 
    starry_grp.links.new(bright_cntr.outputs['Color'], hue_sat.inputs['Color']) 
    starry_grp.links.new(hue_sat.outputs['Color'], rgb_curve_b.inputs['Color']) 
    starry_grp.links.new(rgb_curve_b.outputs['Color'], color.inputs['Color2']) 
    starry_grp.links.new(rgb_curve.outputs['Color'], color.inputs['Color1']) 
    starry_grp.links.new(color.outputs['Color'], bkgrnd.inputs['Color'])
    #node_tree.links.new(hdri_node.outputs['Color'], rgb_bw.inputs['Color']) 
    #node_tree.links.new(rgb_bw.outputs['Val'], rgb_curve.inputs['Color']) 
    
    
    bkgrnd_b = starry_grp.nodes.new("ShaderNodeBackground")
    bkgrnd_b.location = (-100, 150)
    mix_shdr = starry_grp.nodes.new("ShaderNodeMixShader")
    mix_shdr.location = (300, 300)
    mix_shdr_b = starry_grp.nodes.new("ShaderNodeMixShader") #My addition to keep part of the noise+magic texture
    mix_shdr_b.location = (700, 300)
    text_coord_b = starry_grp.nodes.new("ShaderNodeTexCoord")
    text_coord_b.location = (-900, 400)    
    mapping_b = starry_grp.nodes.new("ShaderNodeMapping")
    mapping_b.location = (-700, 400)
    noise_txtr_b = starry_grp.nodes.new("ShaderNodeTexNoise")    
    noise_txtr_b.location = (-500, 400)
    color_rmp = starry_grp.nodes.new("ShaderNodeValToRGB")
    color_rmp.location = (-300, 400)
    
    bkgrnd_b.inputs['Color'].default_value[0] = 0
    bkgrnd_b.inputs['Color'].default_value[1] = 0
    bkgrnd_b.inputs['Color'].default_value[2] = 0
    mix_shdr_b.inputs['Fac'].default_value = 0.0007
    mapping_b.inputs['Location'].default_value[2] = 0.0 #Z location, keyframe this to .5 over about 5 seconds, but should experiment too; I think fast flickering could be cool
    noise_txtr_b.inputs['Scale'].default_value = 5.2
    noise_txtr_b.inputs['Detail'].default_value = 2.0
    noise_txtr_b.inputs['Distortion'].default_value = 4.2
    color_rmp.color_ramp.elements[0].color = (1,1,1,1)
    color_rmp.color_ramp.elements[1].color = (0,0,0,1)
    color_rmp.color_ramp.elements[0].position = 0.21 #Val from video: 0.21    
    color_rmp.color_ramp.elements[1].position = 0.7 #Val from video: 0.534
    
    #color_rmp.inputs['Distortion'].default_value = 4.2
    #color_rmp.inputs['Distortion'].default_value = 4.2
    #curve_c = rgb_curve.mapping.curves[3]
    #curve_c.points.new(.677,.144)
    #curve_c.points.new(.777,.912)
    
    starry_grp.links.new(starry_grp_inputs.outputs[2], mix_shdr_b.inputs['Fac']) 
    starry_grp.links.new(starry_grp_inputs.outputs[3], mapping_b.inputs['Location'])
    starry_grp.links.new(starry_grp_inputs.outputs[4], mix_shdr.inputs[2]) #Need 2nd shader input
    starry_grp.links.new(color.outputs['Color'], starry_grp_outputs.inputs[0])
    starry_grp.links.new(mix_shdr_b.outputs['Shader'], starry_grp_outputs.inputs[1])
    starry_grp.links.new(bkgrnd_b.outputs['Background'], mix_shdr.inputs['Shader'])
    starry_grp.links.new(mix_shdr.outputs['Shader'], mix_shdr_b.inputs['Shader'])
    starry_grp.links.new(mix_shdr_b.outputs['Shader'], output_wrld.inputs['Surface'])
    starry_grp.links.new(bkgrnd.outputs['Background'], mix_shdr.inputs[2]) #Funny, this input has the same name 'Shader' so instead I need to use its index    
    starry_grp.links.new(hue_sat.outputs['Color'], mix_shdr_b.inputs[2]) #Funny, this input has the same name 'Shader' so instead I need to use its index    
    starry_grp.links.new(text_coord_b.outputs['Generated'], mapping_b.inputs['Vector']) 
    starry_grp.links.new(mapping_b.outputs['Vector'], noise_txtr_b.inputs['Vector'])
    starry_grp.links.new(noise_txtr_b.outputs['Fac'], color_rmp.inputs['Fac'])
    starry_grp.links.new(color_rmp.outputs['Color'], mix_shdr.inputs['Fac'])
    
    world_starry = world.node_tree.nodes.new("ShaderNodeGroup")
    world_starry.location = (100, -100)
        
    world_starry.node_tree = bpy.data.node_groups['StarControls']
    
    node_tree.links.new(rgb_curve.outputs['Color'], world_starry.inputs['Color']) 
    node_tree.links.new(world_starry.outputs['Color'], bkgrnd.inputs['Color'])
    node_tree.links.new(bkgrnd.outputs['Background'], world_starry.inputs['Bkg Shader'])
    node_tree.links.new(world_starry.outputs['Shader'], output_wrld.inputs['Surface'])
    
    #node_tree.links.new(rgb_bw.outputs['Val'], rgb_curve.inputs['Color']) 
    
    

 
    
    
    #From here, maybe make this into his own Group Node
    #keyframe the z-axis of the second mapping node, btw. 0 and 1 is good per 5-10 seconds
    #The main controls are color fac, to make stars more/less colorful,
    #RGB curves for how much of original image to include and brighten
    #color_rmp positions and values for how dark/bright range stars will be
    #fac on the final mix shader
    
    #Oh, and probably disable the space plane or else shrink it or w/e, make small copies and put them around,
    #same for lights
            
               
    
def AddVignetteGroupNode():
    
    """Works now; also use the monochrome group node creator in my image plane monochrome fn 
    
    Adds a test_group node via usable code for changing below;
    note the below code does not create said node"""
    
    # switch on nodes and get reference
    bpy.context.scene.use_nodes = True
    
    
    tree = bpy.context.scene.node_tree

    """
    # clear default nodes
    for node in tree.nodes:
        tree.nodes.remove(node)
    """
    
    """
    
    # create input image node
    render_node = tree.nodes[1]
    #image_node.image = bpy.data.images['YOUR_IMAGE_NAME']
    render_node.location = (0, -300)

    # create output node
    comp_node = tree.nodes[0]  
    comp_node.location = (400, 0)

    # link nodes
    tree.links.new(render_node.outputs[0], comp_node.inputs[0])
    """
    
    vignette = bpy.data.node_groups.new('Vignette', 'CompositorNodeTree')

    # create group inputs
    vignette_inputs = vignette.nodes.new('NodeGroupInput')
    vignette_inputs.location = (-1100,0)
    #test_group.inputs.new('NodeSocketFloat','in_to_greater')
    #test_group.inputs.new('NodeSocketFloat','in_to_less')

    # create group outputs
    vignette_outputs = vignette.nodes.new('NodeGroupOutput')
    vignette_outputs.location = (500,0)
    #test_group.outputs.new('NodeSocketFloat','out_result')

    # create node in group
    mix = vignette.nodes.new('CompositorNodeMixRGB')
    mix.location = (-700, 0)
    lens_dist = vignette.nodes.new('CompositorNodeLensdist')
    lens_dist.location = (-500, 0)
    scale = vignette.nodes.new('CompositorNodeScale')
    scale.location = (-300, 0)
    alpha_over = vignette.nodes.new('CompositorNodeAlphaOver')
    alpha_over.location = (-100, 0)
    blur = vignette.nodes.new('CompositorNodeBlur')
    blur.location = (100, 0)
    #Set to fast gaussian
    mix_b = vignette.nodes.new('CompositorNodeMixRGB')
    mix_b.location = (300, 0)
    #set to multiply
    connection = vignette.nodes.new('NodeReroute')
    connection.location = (-900, 0)
    
        
    mix.inputs[1].default_value[0] = 1
    mix.inputs[1].default_value[1] = 1
    mix.inputs[1].default_value[2] = 1
    lens_dist.inputs['Distort'].default_value = 1
    
    alpha_over.inputs['Image'].default_value[0] = 0.046 #Change these to darken/brighten vignette
    alpha_over.inputs['Image'].default_value[1] = 0.046
    alpha_over.inputs['Image'].default_value[2] = 0.046
    
    blur.filter_type = 'FAST_GAUSS'
    blur.size_x = 250
    blur.size_y = 250


    mix_b.blend_type = 'MULTIPLY'
    
    #Explicitly make Image color input or else image is black and white for some reason
    #Actually, just create them in this manner so we can name them and so don't have to rename later
    vignette.inputs.new('NodeSocketColor','Image')
    vignette.inputs.new('NodeSocketFloat','X')
    vignette.inputs.new('NodeSocketFloat','Y')
    vignette.inputs.new('NodeSocketFloat','Feather')
    
    
    #Set min/max/default values 
    input = bpy.data.node_groups["Vignette"].inputs['X']
    input.min_value     = 0.0
    input.max_value     = 12000.0
    input.default_value = 1.0
    input = bpy.data.node_groups["Vignette"].inputs['Y']
    input.min_value     = 0.0
    input.max_value     = 12000.0
    input.default_value = 1.0
    input = bpy.data.node_groups["Vignette"].inputs['Feather']
    input.min_value     = 0.0
    input.max_value     = 1.0
    input.default_value = 1.0
    

    # link nodes together
    vignette.links.new(mix.outputs['Image'], lens_dist.inputs['Image'])
    vignette.links.new(lens_dist.outputs['Image'], scale.inputs['Image'])
    vignette.links.new(scale.outputs['Image'], alpha_over.inputs[2]) #Needs to be the final image input
    vignette.links.new(alpha_over.outputs['Image'], blur.inputs['Image'])
    vignette.links.new(blur.outputs['Image'], mix_b.inputs['Image'])
    vignette.links.new(connection.outputs[0], mix.inputs['Image'])
    vignette.links.new(connection.outputs[0], mix_b.inputs[2]) #Needs to be the final image input    

    # link input
    vignette.links.new(vignette_inputs.outputs[0], connection.inputs[0])
    vignette.links.new(vignette_inputs.outputs[1], scale.inputs['X'])
    vignette.links.new(vignette_inputs.outputs[2], scale.inputs['Y'])
    vignette.links.new(vignette_inputs.outputs[3], blur.inputs['Size'])
    #test_group.links.new(group_inputs.outputs['in_to_less'], node_less.inputs[0])

    #link output
    vignette.links.new(mix_b.outputs[0], vignette_outputs.inputs[0])
    
    #Rename
    #vignette_inputs.outputs[3].name = 'Feather' #Only renames input name inside of the group node
    #vignette.inputs[3].name = 'Feather' #I can't believe it but this worked!
        
    
    vig_comp = tree.nodes.new("CompositorNodeGroup")
    vig_comp.location = (0, 200)
    vig_comp.node_tree = bpy.data.node_groups['Vignette']
    
    
    render_node = tree.nodes[1]
    render_node.location = (-300, 200)

    comp_node = tree.nodes[0]  
    comp_node.location = (200, 200)

    # link nodes
    tree.links.new(render_node.outputs[0], vig_comp.inputs[0])   
    tree.links.new(vig_comp.outputs[0], comp_node.inputs[0])
    
    
    """
    
    
    new_group = bpy.data.node_groups.new('NewGroup', 'ShaderNodeTree')

    # create group inputs
    group_inputs = new_group.nodes.new('NodeGroupInput')
    group_inputs.location = (-300,0)
    #test_group.inputs.new('NodeSocketFloat','in_to_greater')
    #test_group.inputs.new('NodeSocketFloat','in_to_less')

    # create group outputs
    group_outputs = new_group.nodes.new('NodeGroupOutput')
    group_outputs.location = (400,0)
    #test_group.outputs.new('NodeSocketFloat','out_result')

    # create node in group
    color_rmp = new_group.nodes.new("ShaderNodeValToRGB")
    color_rmp.location = (0, 0)
    color_rmp.color_ramp.elements[0].color = (1,1,0,1) #Yellow
    color_rmp.color_ramp.elements[1].color = (0,0,0,1)
    color_rmp.color_ramp.elements[0].position = 0  
    color_rmp.color_ramp.elements[1].position = 1

    # link nodes together
    #new_group.links.new(node_add.inputs[0], node_greater.outputs[0])
    #new_group.links.new(node_add.inputs[1], node_less.outputs[0])

    # link input
    new_group.links.new(group_inputs.outputs[0], color_rmp.inputs[0])
    #test_group.links.new(group_inputs.outputs['in_to_less'], node_less.inputs[0])

    #link output
    new_group.links.new(color_rmp.outputs[0], group_outputs.inputs[0])
    """

    
    """
    ##########
    
    # create a group
    test_group = bpy.data.node_groups.new('testGroup', 'ShaderNodeTree')

    # create group inputs
    group_inputs = test_group.nodes.new('NodeGroupInput')
    group_inputs.location = (-350,0)
    test_group.inputs.new('NodeSocketFloat','in_to_greater')
    test_group.inputs.new('NodeSocketFloat','in_to_less')

    # create group outputs
    group_outputs = test_group.nodes.new('NodeGroupOutput')
    group_outputs.location = (300,0)
    test_group.outputs.new('NodeSocketFloat','out_result')

    # create three math nodes in a group
    node_add = test_group.nodes.new('ShaderNodeMath')
    node_add.operation = 'ADD'
    node_add.location = (100,0)

    node_greater = test_group.nodes.new('ShaderNodeMath')
    node_greater.operation = 'GREATER_THAN'
    node_greater.label = 'greater'
    node_greater.location = (-100,100)

    node_less = test_group.nodes.new('ShaderNodeMath')
    node_less.operation = 'LESS_THAN'
    node_less.label = 'less'
    node_less.location = (-100,-100)

    # link nodes together
    test_group.links.new(node_add.inputs[0], node_greater.outputs[0])
    test_group.links.new(node_add.inputs[1], node_less.outputs[0])

    # link inputs
    test_group.links.new(group_inputs.outputs['in_to_greater'], node_greater.inputs[0])
    test_group.links.new(group_inputs.outputs['in_to_less'], node_less.inputs[0])

    #link output
    test_group.links.new(node_add.outputs[0], group_outputs.inputs['out_result'])
    
    """
    """
    group = bpy.context.scene.node_tree.nodes.new('CompositorNodeGroup')
    
    
    group.node_tree = bpy.data.node_groups['somegroupname']
    
    return None
        
        
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

    """
        
    


DeleteCube()
CreateLightsCameraCollection()
TrackCameraToEmpty()
AddSpotlightToTrackWithCamera()
SetupEvee()
SetResolutionOutput()
AddMaterials()
AddCubesForMaterials()
AddReflectiveSphere()
AddSpacePlane()
AddEmissionObjs()
AddLights()
AddGreenMatallicFloor()
AddVignetteGroupNode()
AddHDRITwinklyStars('/home/paul/Documents/HDRI Images/satara_night_no_lamps_16k.hdr')
#AddHDRITwinklyStarsNodeGroup('/home/paul/Documents/HDRI Images/satara_night_no_lamps_16k.hdr')
SetRenderLoc("/home/paul/Documents/Blender/Renders/" + name_of_blendfile + '/')
bpy.ops.wm.save_as_mainfile(filepath='/home/paul/Documents/Blender/' + name_of_blendfile + '.blend')


#bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath) #Useful: let's you save based on what it is named, if you don't want to reenter filepath later



#AddHDRITwinklyStars('/home/paul/Documents/HDRI Images/satara_night_no_lamps_16k.hdr')


"""Below are extras to eventually put elsewhere"""
    
def AddBacklightToSelected():
    """Adds powerful backlight just behind selected objects, sets its affective distance low,
    adds it to its own collection named after the first object and 'BLight'
    """
        
    objs = [o for o in bpy.context.selected_objects]
        
    new_col = bpy.data.collections.new(name=objs[0].name + 'BLight') #create new collection in data
    bpy.context.scene.collection.children.link(new_col) #add new collection to the scene  
    
    for obj in objs:
        
        loc_x = obj.location[0]
        loc_y = obj.location[1] + 0.75
        loc_z = obj.location[2]
        
        new_name = obj.name + 'BLight'
        
        bpy.ops.object.light_add(type='POINT', location=(loc_x, loc_y, loc_z))

        bpy.context.object.data.energy = 5000
        bpy.context.object.data.use_custom_distance = True
        bpy.context.object.data.cutoff_distance = 1
        bpy.context.active_object.name = new_name
        
        
        obj_old_col = bpy.data.objects[new_name].users_collection #list of all collections the txt_obj is in, the main scene by default
        new_col.objects.link(bpy.data.objects[new_name]) #link txt_obj to new_col
        
        for ob in obj_old_col: #unlink from all previous collections
            
            ob.objects.unlink(bpy.data.objects[new_name])   
            
def SetImagesOnceOnPlanes():
    
    """This fn will take names of images on planes and add a bumpmap and set shader to be correct
    It's probably more convenient to just select them and run this"""
    
    objs = [o for o in bpy.context.selected_objects]
    
    for obj in objs:
        
        pass   

