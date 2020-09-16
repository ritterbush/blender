bl_info = {
    "name": "Misc",
    "author": "Paul Ritterbush",
    "version": (1, 0),
    "blender": (2, 80, 2),
    "location": "View3D > Sidebar > Misc Tab",
    "description": "My best miscelaneous helpers",
    "warning": "",
    "wiki_url": "",
    "category": "Object",
}

import bpy


def CreateNewCol(name='New Collection', hide=False):
    """Creates a new collection"""
    
    new_col = bpy.data.collections.new(name) #create new collection in data
    bpy.context.scene.collection.children.link(new_col) #add new collection to the scene
    
    if hide:
        
        for view_layer in bpy.context.scene.view_layers:
                
            for child in view_layer.layer_collection.children:
                
                if child.name == name:
                
                    child.exclude = True      


def PutSelectedInCol(name='New Collection', hide=False, keep_in_other_cols=False):
    """Puts selected in collection. Creates it if not yet made"""
            
    objs = [o for o in bpy.context.selected_objects]
            
    if bpy.data.collections.get(name) is None:
        
        CreateNewCol(name)        
        
    for obj in objs:
        
        obj_name = obj.name                        

        obj_old_cols = bpy.data.objects[obj_name].users_collection 
        new_col = bpy.data.collections[name]
        
        if not keep_in_other_cols:
        
            for col in obj_old_cols:
            
                col.objects.unlink(obj)   
                
        new_col.objects.link(obj)
        
    if hide:
        
        for view_layer in bpy.context.scene.view_layers:
                
            for child in view_layer.layer_collection.children:
                
                if child.name == name:
                
                    child.exclude = True  
                    
                    
def AddBacklightToSelected(offset_around=0.4, offset_back=0.1, brightness=100, light_cutoff_distance=0.6, is_x=False, is_y=True, is_z=False, red=1, green=1, blue=1):
    """Adds powerful backlight just behind selected objects, sets its affective distance low,
    adds it to its own collection named after the first object and 'BLight'
    Tip: create an empty to control them as a group and lift them up slightly higher than the 
    objects they light to give a top light.
    
    """
    
    #pi = 3.141592653589793
        
    objs = [o for o in bpy.context.selected_objects]
    backlights = []
    
        
    new_col = bpy.data.collections.new(name=objs[0].name + 'BLight') #create new collection in data
    bpy.context.scene.collection.children.link(new_col) #add new collection to the scene  
    
    for obj in objs:
                       
        loc_x = obj.location[0]
        loc_y = obj.location[1]
        loc_z = obj.location[2]
        
        print('locationxyz', loc_x, loc_y, loc_z)
        
        #if is_x:
            
        #loc_x += offset_behind #Offset light from obj along x-axis
            
        if is_y:
        
            loc_y += offset_back #Offset behind obj   
            loc_x -= offset_around            
            loc_z += offset_around
            
        #if is_z:
        
        #loc_z += offset_behind #Offset light from obj along z-axis        
        
        """Left Backlight"""
        new_name = obj.name + 'BLight_L'
        
        bpy.ops.object.light_add(type='SPOT', location=(loc_x, loc_y, loc_z))       
        bpy.context.active_object.name = new_name
        
        spotlight = bpy.data.objects[new_name]        
        spotlight.data.color = [red, green, blue]
        spotlight.data.energy = brightness
        spotlight.data.use_custom_distance = True
        spotlight.data.cutoff_distance = light_cutoff_distance
        
        #spotlight.data.spot_size = 3.14159 #180 degrees
        #spotlight.data.spot_size = 1.5708 #90 degrees
        spotlight.data.spot_size = 0.5
 

        """Parent to Camera"""
        #cam_spotlight.parent = camera        
        
        """Tracking constraint"""
        spotlight.constraints.new(type='TRACK_TO')
        spotlight.constraints["Track To"].target = obj
        spotlight.constraints["Track To"].track_axis = 'TRACK_NEGATIVE_Z'
        spotlight.constraints["Track To"].up_axis = 'UP_Y'    
                
        obj_old_col = spotlight.users_collection #list of all collections the txt_obj is in, the main scene by default
        new_col.objects.link(spotlight) #link txt_obj to new_col
        
        for ob in obj_old_col: #unlink from all previous collections
            
            ob.objects.unlink(spotlight)
            
        backlights += [spotlight]
                
        
        """Right Backlight"""
        #print(loc_x, 'a')
        loc_x += offset_around * 2
        #print(loc_x, 'b')
        

        new_name = obj.name + 'BLight_R'
        
        bpy.ops.object.light_add(type='SPOT', location=(loc_x, loc_y, loc_z))       
        bpy.context.active_object.name = new_name
        
        spotlight = bpy.data.objects[new_name]        
        spotlight.data.color = [red, green, blue]
        spotlight.data.energy = brightness
        spotlight.data.use_custom_distance = True
        spotlight.data.cutoff_distance = light_cutoff_distance
        
        #spotlight.data.spot_size = 3.14159 #180 degrees
        #spotlight.data.spot_size = 1.5708 #90 degrees
        spotlight.data.spot_size = 0.5



        spotlight.constraints.new(type='TRACK_TO')
        spotlight.constraints["Track To"].target = obj
        spotlight.constraints["Track To"].track_axis = 'TRACK_NEGATIVE_Z'
        spotlight.constraints["Track To"].up_axis = 'UP_Y'    
                
        obj_old_col = spotlight.users_collection #list of all collections the txt_obj is in, the main scene by default
        new_col.objects.link(spotlight) #link txt_obj to new_col
        
        for ob in obj_old_col: #unlink from all previous collections
            
            ob.objects.unlink(spotlight)       
            
        backlights += [spotlight]   
            
        """Top Backlight"""
        loc_x -= offset_around
        loc_z += 1 * (0.5 * offset_around)
        
        new_name = obj.name + 'BLight_T'
        
        bpy.ops.object.light_add(type='SPOT', location=(loc_x, loc_y, loc_z))       
        bpy.context.active_object.name = new_name
        
        spotlight = bpy.data.objects[new_name]        
        spotlight.data.color = [red, green, blue]
        spotlight.data.energy = brightness
        spotlight.data.use_custom_distance = True
        spotlight.data.cutoff_distance = light_cutoff_distance
        
        #spotlight.data.spot_size = 1.5708 #90 degrees
        #spotlight.data.spot_size = 3.14159 #180 degrees
        spotlight.data.spot_size = 0.5
 

        """Parent to Camera"""
        #cam_spotlight.parent = camera        
        
        """Tracking constraint"""
        spotlight.constraints.new(type='TRACK_TO')
        spotlight.constraints["Track To"].target = obj
        spotlight.constraints["Track To"].track_axis = 'TRACK_NEGATIVE_Z'
        spotlight.constraints["Track To"].up_axis = 'UP_Y'    
                
        obj_old_col = spotlight.users_collection #list of all collections the txt_obj is in, the main scene by default
        new_col.objects.link(spotlight) #link txt_obj to new_col
        
        for ob in obj_old_col: #unlink from all previous collections
            
            ob.objects.unlink(spotlight)
        backlights += [spotlight]
        
        
    """End fn with our new objs selected"""
    for ob in bpy.context.selected_objects:
                
        obj.select_set(False)
    
    for backlight in backlights:
        
        backlight.select_set(True)    
    
    #Make active the first obj
    if objs:
        
        active_backlight_name = objs[0].name + 'BLight_L'
        active_backlight = bpy.data.objects[active_backlight_name]
        bpy.context.view_layer.objects.active = active_backlight
                  
def AddBacklightToSelected(offset_around=0.4, offset_back=0, brightness=100, light_cutoff_distance=0.6, is_x=False, is_y=True, is_z=False, red=1, green=1, blue=1):
    """Adds powerful backlight just behind selected objects, sets its affective distance low,
    adds it to its own collection named after the first object and 'BLight'
    Tip: create an empty to control them as a group and lift them up slightly higher than the 
    objects they light to give a top light.
    
    """
    
    #pi = 3.141592653589793
        
    objs = [o for o in bpy.context.selected_objects]
    backlights = []
    
        
    new_col = bpy.data.collections.new(name=objs[0].name + 'BLight') #create new collection in data
    bpy.context.scene.collection.children.link(new_col) #add new collection to the scene  
    
    for obj in objs:
                       
        loc_x = obj.location[0]
        loc_y = obj.location[1]
        loc_z = obj.location[2]
        
        print('locationxyz', loc_x, loc_y, loc_z)
        
        #if is_x:
            
        #loc_x += offset_behind #Offset light from obj along x-axis
            
        if is_y:
        
            loc_y += offset_back #Offset behind obj   
            loc_x -= offset_around            
            loc_z += offset_around
            
        #if is_z:
        
        #loc_z += offset_behind #Offset light from obj along z-axis        
        
        """Left Backlight"""
        new_name = obj.name + 'BLight_L'
        
        bpy.ops.object.light_add(type='AREA', location=(loc_x, loc_y, loc_z))       
        bpy.context.active_object.name = new_name
        
        spotlight = bpy.data.objects[new_name]        
        spotlight.data.color = [red, green, blue]
        spotlight.data.energy = brightness
        spotlight.data.use_custom_distance = True
        spotlight.data.cutoff_distance = light_cutoff_distance
        
        #spotlight.data.spot_size = 3.14159 #180 degrees
        #spotlight.data.spot_size = 1.5708 #90 degrees
        #spotlight.data.spot_size = 0.5
        
        spotlight.data.shape = 'RECTANGLE'
        spotlight.data.size = 0
        spotlight.data.size_y = 0



 

        """Parent to Camera"""
        #cam_spotlight.parent = camera        
        
        """Tracking constraint"""
        spotlight.constraints.new(type='TRACK_TO')
        spotlight.constraints["Track To"].target = obj
        spotlight.constraints["Track To"].track_axis = 'TRACK_NEGATIVE_Z'
        spotlight.constraints["Track To"].up_axis = 'UP_Y'    
                
        obj_old_col = spotlight.users_collection #list of all collections the txt_obj is in, the main scene by default
        new_col.objects.link(spotlight) #link txt_obj to new_col
        
        for ob in obj_old_col: #unlink from all previous collections
            
            ob.objects.unlink(spotlight)
            
        backlights += [spotlight]
                
        
        """Right Backlight"""
        #print(loc_x, 'a')
        loc_x += offset_around * 2
        #print(loc_x, 'b')
        

        new_name = obj.name + 'BLight_R'
        
        bpy.ops.object.light_add(type='AREA', location=(loc_x, loc_y, loc_z))       
        bpy.context.active_object.name = new_name
        
        spotlight = bpy.data.objects[new_name]        
        spotlight.data.color = [red, green, blue]
        spotlight.data.energy = brightness
        spotlight.data.use_custom_distance = True
        spotlight.data.cutoff_distance = light_cutoff_distance
        
        #spotlight.data.spot_size = 3.14159 #180 degrees
        #spotlight.data.spot_size = 1.5708 #90 degrees
        #spotlight.data.spot_size = 0.5
        
        spotlight.data.shape = 'RECTANGLE'
        spotlight.data.size = 0
        spotlight.data.size_y = 0



        spotlight.constraints.new(type='TRACK_TO')
        spotlight.constraints["Track To"].target = obj
        spotlight.constraints["Track To"].track_axis = 'TRACK_NEGATIVE_Z'
        spotlight.constraints["Track To"].up_axis = 'UP_Y'    
                
        obj_old_col = spotlight.users_collection #list of all collections the txt_obj is in, the main scene by default
        new_col.objects.link(spotlight) #link txt_obj to new_col
        
        for ob in obj_old_col: #unlink from all previous collections
            
            ob.objects.unlink(spotlight)       
            
        backlights += [spotlight]   
            
        """Top Backlight"""
        loc_x -= offset_around
        loc_z += 1 * (0.5 * offset_around)
        
        new_name = obj.name + 'BLight_T'
        
        bpy.ops.object.light_add(type='AREA', location=(loc_x, loc_y, loc_z))       
        bpy.context.active_object.name = new_name
        
        spotlight = bpy.data.objects[new_name]        
        spotlight.data.color = [red, green, blue]
        spotlight.data.energy = brightness
        spotlight.data.use_custom_distance = True
        spotlight.data.cutoff_distance = light_cutoff_distance
        
        #spotlight.data.spot_size = 1.5708 #90 degrees
        #spotlight.data.spot_size = 3.14159 #180 degrees
        #spotlight.data.spot_size = 0.5
        
        spotlight.data.shape = 'RECTANGLE'
        spotlight.data.size = 0
        spotlight.data.size_y = 0
 

        """Parent to Camera"""
        #cam_spotlight.parent = camera        
        
        """Tracking constraint"""
        spotlight.constraints.new(type='TRACK_TO')
        spotlight.constraints["Track To"].target = obj
        spotlight.constraints["Track To"].track_axis = 'TRACK_NEGATIVE_Z'
        spotlight.constraints["Track To"].up_axis = 'UP_Y'    
                
        obj_old_col = spotlight.users_collection #list of all collections the txt_obj is in, the main scene by default
        new_col.objects.link(spotlight) #link txt_obj to new_col
        
        for ob in obj_old_col: #unlink from all previous collections
            
            ob.objects.unlink(spotlight)
        backlights += [spotlight]
        
        
    """End fn with our new objs selected"""
    for ob in bpy.context.selected_objects:
                
        obj.select_set(False)
    
    for backlight in backlights:
        
        backlight.select_set(True)    
    
    #Make active the first obj
    if objs:
        
        active_backlight_name = objs[0].name + 'BLight_L'
        active_backlight = bpy.data.objects[active_backlight_name]
        bpy.context.view_layer.objects.active = active_backlight 
        
        
                    
                    
def AddBacklightToSelected(offset_around=0.4, offset_back=0.1, brightness=100, light_cutoff_distance=0.6, is_x=False, is_y=True, is_z=False, red=1, green=1, blue=1):
    """Adds powerful backlight just behind selected objects, sets its affective distance low,
    adds it to its own collection named after the first object and 'BLight'
    Tip: create an empty to control them as a group and lift them up slightly higher than the 
    objects they light to give a top light.
    
    """
    
    #pi = 3.141592653589793
        
    objs = [o for o in bpy.context.selected_objects]
    backlights = []
    
        
    new_col = bpy.data.collections.new(name=objs[0].name + 'BLight') #create new collection in data
    bpy.context.scene.collection.children.link(new_col) #add new collection to the scene  
    
    for obj in objs:
                       
        loc_x = obj.location[0]
        loc_y = obj.location[1]
        loc_z = obj.location[2]
        
        print('locationxyz', loc_x, loc_y, loc_z)
        
        #if is_x:
            
        #loc_x += offset_behind #Offset light from obj along x-axis
            
        if is_y:
        
            loc_y += offset_back #Offset behind obj   #1.5
            #loc_x -= offset_around            
            #loc_z += offset_around
            
            location = (loc_x, loc_y, loc_z)
            

            
        #if is_z:
        
        #loc_z += offset_behind #Offset light from obj along z-axis        

            
        """Top Backlight"""
        #loc_x -= offset_around
        #loc_z += 1 * (0.5 * offset_around)
        
        new_name = obj.name + 'BLight_T'
        
        bpy.ops.object.light_add(type='POINT', location=(loc_x, loc_y, loc_z + (obj.dimensions[1] / 2)))       
        bpy.context.active_object.name = new_name
        
        spotlight = bpy.data.objects[new_name]        
        spotlight.data.color = [red, green, blue]
        spotlight.data.energy = brightness
        spotlight.data.use_custom_distance = True
        spotlight.data.cutoff_distance = light_cutoff_distance #0.6
        
        #spotlight.data.spot_size = 1.5708 #90 degrees
        #spotlight.data.spot_size = 3.14159 #180 degrees
        #spotlight.data.spot_size = 0.523525
        spotlight.data.shadow_soft_size = 0.25
        
        obj_old_col = spotlight.users_collection #list of all collections the txt_obj is in, the main scene by default
        new_col.objects.link(spotlight) #link txt_obj to new_col
        
        for ob in obj_old_col: #unlink from all previous collections
            
            ob.objects.unlink(spotlight)
        backlights += [spotlight]
            
        """Mid Backlight"""
        #loc_x -= offset_around
        #loc_z += 1 * (0.5 * offset_around)
        
        new_name = obj.name + 'BLight_M'
        
        bpy.ops.object.light_add(type='POINT', location=(loc_x, loc_y, loc_z))       
        bpy.context.active_object.name = new_name
        
        spotlight = bpy.data.objects[new_name]        
        spotlight.data.color = [red, green, blue]
        spotlight.data.energy = brightness
        spotlight.data.use_custom_distance = True
        spotlight.data.cutoff_distance = light_cutoff_distance #0.6
        
        #spotlight.data.spot_size = 1.5708 #90 degrees
        #spotlight.data.spot_size = 3.14159 #180 degrees
        #spotlight.data.spot_size = 0.523525
        spotlight.data.shadow_soft_size = 0.25
        
        obj_old_col = spotlight.users_collection #list of all collections the txt_obj is in, the main scene by default
        new_col.objects.link(spotlight) #link txt_obj to new_col
        
        for ob in obj_old_col: #unlink from all previous collections
            
            ob.objects.unlink(spotlight)
        backlights += [spotlight]

            
        """Bottom Backlight"""
        #loc_x -= offset_around
        #loc_z += 1 * (0.5 * offset_around)
        
        new_name = obj.name + 'BLight_B'
        
        bpy.ops.object.light_add(type='POINT', location=(loc_x, loc_y, loc_z - (obj.dimensions[1] / 2)))       
        bpy.context.active_object.name = new_name
        
        spotlight = bpy.data.objects[new_name]        
        spotlight.data.color = [red, green, blue]
        spotlight.data.energy = brightness
        spotlight.data.use_custom_distance = True
        spotlight.data.cutoff_distance = light_cutoff_distance #0.6
        
        #spotlight.data.spot_size = 1.5708 #90 degrees
        #spotlight.data.spot_size = 3.14159 #180 degrees
        #spotlight.data.spot_size = 0.523525
        spotlight.data.shadow_soft_size = 0.25



 

        """Parent to Camera"""
        #cam_spotlight.parent = camera        
        
        """Tracking constraint"""
        """
        spotlight.constraints.new(type='TRACK_TO')
        spotlight.constraints["Track To"].target = obj
        spotlight.constraints["Track To"].track_axis = 'TRACK_NEGATIVE_Z'
        spotlight.constraints["Track To"].up_axis = 'UP_Y'
        
        """    
                
        obj_old_col = spotlight.users_collection #list of all collections the txt_obj is in, the main scene by default
        new_col.objects.link(spotlight) #link txt_obj to new_col
        
        for ob in obj_old_col: #unlink from all previous collections
            
            ob.objects.unlink(spotlight)
        backlights += [spotlight]
        
        
    """End fn with our new objs selected"""
    for ob in bpy.context.selected_objects:
                
        obj.select_set(False)
    
    for backlight in backlights:
        
        backlight.select_set(True)    
    
    #Make active the first obj
    if objs:
        
        active_backlight_name = objs[0].name + 'BLight_T'
        active_backlight = bpy.data.objects[active_backlight_name]
        bpy.context.view_layer.objects.active = active_backlight
        
                 
def AddBacklightToSelected2(offset_around=0.4, offset_back=0.1, brightness=100, light_cutoff_distance=0.6, is_x=False, is_y=True, is_z=False, red=1, green=1, blue=1):
    """Adds powerful backlight just behind selected objects, sets its affective distance low,
    adds it to its own collection named after the first object and 'BLight'
    Tip: create an empty to control them as a group and lift them up slightly higher than the 
    objects they light to give a top light.
    
    """
    
    #pi = 3.141592653589793
        
    objs = [o for o in bpy.context.selected_objects]
    backlights = []
    
        
    new_col = bpy.data.collections.new(name=objs[0].name + 'BLight') #create new collection in data
    bpy.context.scene.collection.children.link(new_col) #add new collection to the scene  
    
    for obj in objs:
        
        
        x_dimension = obj.dimensions[0] 
        y_dimension = obj.dimensions[2] 
        z_dimension = obj.dimensions[1] 
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
                       
        loc_x = obj.location[0]
        loc_y = obj.location[1]
        loc_z = obj.location[2]
        
        
        
        
        
        
        
        
        
        
        print('locationxyz', loc_x, loc_y, loc_z)
        
        #if is_x:
            
        #loc_x += offset_behind #Offset light from obj along x-axis
        
        #Defaults to neutral for most lights
        if is_y:
        
            loc_y += offset_back/2  #divide by 2 to ensure that light reaches edges while not going beyond the letter itself, except minimally behind it #Offset behind obj   #1.5
            #loc_x -= offset_around            
            #loc_z += offset_around
            
            #location = (loc_x, loc_y, loc_z)
            
            #light_cutoff_distance = (obj.dimensions[1] / 2) + offset_back
            
            #loc_z += obj.dimensions[1] / 2
            light_cutoff_distance = offset_back
            
        #if is_z:
        
        #loc_z += offset_behind #Offset light from obj along z-axis        

        smidge = 0.001
        #smidge = 0
            
        """Top Backlight"""
        #loc_x -= offset_around
        #loc_z += 1 * (0.5 * offset_around)
        
        new_name = obj.name + 'BLight_T'
        
        #bpy.ops.object.light_add(type='AREA', location=(loc_x, loc_y, loc_z + (obj.dimensions[1] / 2)))       
        bpy.ops.object.light_add(type='AREA', location=(loc_x, loc_y, loc_z + (obj.dimensions[1] / 2) + smidge)) #2 Notes:
       
        #The y-dimension axis is the z-dimension axis because rotated text cannot be applied (reset); cut the z-dimension in half, add it to the object's z-location; you cannot put the lights centered at the offset without needing to increase the cutoffdistance beyond the object's dimensions everywhere.
        bpy.context.active_object.name = new_name
        
        spotlight = bpy.data.objects[new_name]        
        spotlight.data.color = [red, green, blue]
        spotlight.data.energy = brightness
        spotlight.data.use_custom_distance = True
        spotlight.data.cutoff_distance =  obj.dimensions[1] #Z-axis of obj #OLD light_cutoff_distance #0.6
        
        #spotlight.data.spot_size = 1.5708 #90 degrees
        #spotlight.data.spot_size = 3.14159 #180 degrees
        #spotlight.data.spot_size = 0.523525
        #spotlight.data.shadow_soft_size = 0.25
        
        bpy.context.object.data.shape = 'RECTANGLE'
        bpy.context.object.data.size = obj.dimensions[0] #x-axes
        bpy.context.object.data.size_y = offset_back
        print(offset_back * 2, 'is 2?')
        print(light_cutoff_distance * 2, 'is 2?')

        
        
        obj_old_col = spotlight.users_collection #list of all collections the txt_obj is in, the main scene by default
        new_col.objects.link(spotlight) #link txt_obj to new_col
        
        for ob in obj_old_col: #unlink from all previous collections
            
            ob.objects.unlink(spotlight)
        backlights += [spotlight]
                
        
        """Bottom Backlight"""
        #loc_x -= offset_around
        #loc_z += 1 * (0.5 * offset_around)
        
        new_name = obj.name + 'BLight_B'
        
        bpy.ops.object.light_add(type='AREA', location=(loc_x, loc_y, loc_z - (obj.dimensions[1] / 2) - smidge))       
        bpy.context.active_object.name = new_name
        
        spotlight = bpy.data.objects[new_name]        
        spotlight.data.color = [red, green, blue]
        spotlight.data.energy = brightness
        spotlight.data.use_custom_distance = True
        spotlight.data.cutoff_distance = obj.dimensions[1] #OLDlight_cutoff_distance #0.6
        
        #spotlight.data.spot_size = 1.5708 #90 degrees
        #spotlight.data.spot_size = 3.14159 #180 degrees
        #spotlight.data.spot_size = 0.523525
        #spotlight.data.shadow_soft_size = 0.25
        
        bpy.context.object.data.shape = 'RECTANGLE'        
        bpy.context.object.data.size = obj.dimensions[0]
        bpy.context.object.data.size_y = offset_back
        
        spotlight.rotation_euler[1] = 3.14159 #Point up 180 degs
        
        
   
        obj_old_col = spotlight.users_collection #list of all collections the txt_obj is in, the main scene by default
        new_col.objects.link(spotlight) #link txt_obj to new_col
        
        for ob in obj_old_col: #unlink from all previous collections
            
            ob.objects.unlink(spotlight)
        backlights += [spotlight]

          
        
            
        """Mid Backlight"""
        #loc_x -= offset_around
        #loc_z += 1 * (0.5 * offset_around)
        
        new_name = obj.name + 'BLight_M'
        
        #Old
        #loc_y -= (offset_back/4)
        
        
        bpy.ops.object.light_add(type='AREA', location=(loc_x, loc_y - (offset_back/4) - smidge, loc_z))
        bpy.context.active_object.name = new_name
        
        spotlight = bpy.data.objects[new_name]        
        spotlight.data.color = [red, green, blue]
        spotlight.data.energy = brightness
        spotlight.data.use_custom_distance = True
        spotlight.data.cutoff_distance = obj.dimensions[1]/2#OLD light_cutoff_distance #0.6
        
        #spotlight.data.spot_size = 1.5708 #90 degrees
        #spotlight.data.spot_size = 3.14159 #180 degrees
        #spotlight.data.spot_size = 0.523525
        #spotlight.data.shadow_soft_size = 0.25
        
        bpy.context.object.data.shape = 'RECTANGLE'
        bpy.context.object.data.size = obj.dimensions[0] #x-axes
        bpy.context.object.data.size_y = obj.dimensions[1] #y-axes
        bpy.context.object.rotation_euler[0] = -1.5708

        
        
        obj_old_col = spotlight.users_collection #list of all collections the txt_obj is in, the main scene by default
        new_col.objects.link(spotlight) #link txt_obj to new_col
        
        for ob in obj_old_col: #unlink from all previous collections
            
            ob.objects.unlink(spotlight)
        backlights += [spotlight]
      
                
        """Left Backlight"""
        #loc_x -= offset_around
        #loc_z += 1 * (0.5 * offset_around)
        
        new_name = obj.name + 'BLight_L'
        
        bpy.ops.object.light_add(type='AREA', location=(loc_x - (obj.dimensions[0] / 2) - smidge, loc_y, loc_z))       
        bpy.context.active_object.name = new_name
        
        spotlight = bpy.data.objects[new_name]        
        spotlight.data.color = [red, green, blue]
        spotlight.data.energy = brightness
        spotlight.data.use_custom_distance = True
        spotlight.data.cutoff_distance = obj.dimensions[1] #OLDlight_cutoff_distance #0.6
        
        #spotlight.data.spot_size = 1.5708 #90 degrees
        #spotlight.data.spot_size = 3.14159 #180 degrees
        #spotlight.data.spot_size = 0.523525
        #spotlight.data.shadow_soft_size = 0.25
        
        bpy.context.object.data.shape = 'RECTANGLE'
        bpy.context.object.data.size = obj.dimensions[1]
        bpy.context.object.data.size_y = offset_back
        bpy.context.object.rotation_euler[1] = -1.5708

        
        
        obj_old_col = spotlight.users_collection #list of all collections the txt_obj is in, the main scene by default
        new_col.objects.link(spotlight) #link txt_obj to new_col
        
        for ob in obj_old_col: #unlink from all previous collections
            
            ob.objects.unlink(spotlight)
        backlights += [spotlight]
        
        """Right Backlight"""
        #loc_x -= offset_around
        #loc_z += 1 * (0.5 * offset_around)
        
        new_name = obj.name + 'BLight_R'
        
        bpy.ops.object.light_add(type='AREA', location=(loc_x + (obj.dimensions[0] / 2) + smidge, loc_y, loc_z))       
        bpy.context.active_object.name = new_name
        
        spotlight = bpy.data.objects[new_name]        
        spotlight.data.color = [red, green, blue]
        spotlight.data.energy = brightness
        spotlight.data.use_custom_distance = True
        spotlight.data.cutoff_distance = obj.dimensions[1] #OLD light_cutoff_distance #0.6
        
        #spotlight.data.spot_size = 1.5708 #90 degrees
        #spotlight.data.spot_size = 3.14159 #180 degrees
        #spotlight.data.spot_size = 0.523525
        #spotlight.data.shadow_soft_size = 0.25
        
        bpy.context.object.data.shape = 'RECTANGLE'
        bpy.context.object.data.size = obj.dimensions[1]
        bpy.context.object.data.size_y = offset_back
        bpy.context.object.rotation_euler[1] = 1.5708

        
        
        obj_old_col = spotlight.users_collection #list of all collections the txt_obj is in, the main scene by default
        new_col.objects.link(spotlight) #link txt_obj to new_col
        
        for ob in obj_old_col: #unlink from all previous collections
            
            ob.objects.unlink(spotlight)
        backlights += [spotlight]

            
        
        
    """End fn with our new objs selected"""
    for ob in bpy.context.selected_objects:
                
        obj.select_set(False)
    
    for backlight in backlights:
        
        backlight.select_set(True)    
    
    #Make active the first obj
    if objs:
        
        active_backlight_name = objs[0].name + 'BLight_T'
        active_backlight = bpy.data.objects[active_backlight_name]
        bpy.context.view_layer.objects.active = active_backlight         


def AddBacklightToSelected(offset_around=0.4, offset_back=0.1, brightness=100, light_cutoff_distance=0.6, is_x=False, is_y=True, is_z=False, red=1, green=1, blue=1):
    """Adds powerful backlight just behind selected objects, sets its affective distance low,
    adds it to its own collection named after the first object and 'BLight'
    Tip: create an empty to control them as a group and lift them up slightly higher than the 
    objects they light to give a top light.
    
    Also adds an empty to control original obj alongside all of its lights.
    
    """
    
    #pi = 3.141592653589793
        
    objs = [o for o in bpy.context.selected_objects]
    backlights = []
    
        
    new_col = bpy.data.collections.new(name=objs[0].name + 'BLight') #create new collection in data
    bpy.context.scene.collection.children.link(new_col) #add new collection to the scene  
    
    
    
    control_col = bpy.data.collections.new(name=objs[0].name + 'Controls') #create new collection in data
    bpy.context.scene.collection.children.link(control_col) #add new collection to the scene  
    
    
    for obj in objs:
        
        
        """Add Empty For Control"""
        
        location = obj.location
        
        bpy.ops.object.empty_add(type='SPHERE', radius=0.25, location=location)
        
        bpy.context.active_object.name = obj.name + 'Control'
        empty_controller = bpy.data.objects[obj.name + 'Control'] 
        #empty_controller.location = location
        
        """Ad Empty to Obj's Controls Collection"""
        
        obj_old_col = empty_controller.users_collection #list of all collections the txt_obj is in, the main scene by default
        control_col.objects.link(empty_controller) #link txt_obj to new_col
        
        for ob in obj_old_col: #unlink from all previous collections
            
            ob.objects.unlink(empty_controller)

                
 
        """Make Empty Parent of Obj"""

        obj.parent = empty_controller
        
        #This is used to clear (i.e., not keep) transform 
        obj.matrix_parent_inverse = empty_controller.matrix_world.inverted()
        
           
        
        
        """Add Backlights"""                       
        loc_x = obj.location[0]
        loc_y = obj.location[1]
        loc_z = obj.location[2]
        
        print('locationxyz', loc_x, loc_y, loc_z)
        
        #if is_x:
            
        #loc_x += offset_behind #Offset light from obj along x-axis
        
        #Defaults to neutral for most lights
        if is_y:
        
            loc_y += offset_back/2  #divide by 2 to ensure that light reaches edges while not going beyond the letter itself, except minimally behind it #Offset behind obj   #1.5
            #loc_x -= offset_around            
            #loc_z += offset_around
            
            #location = (loc_x, loc_y, loc_z)
            
            #light_cutoff_distance = (obj.dimensions[1] / 2) + offset_back
            
            #loc_z += obj.dimensions[1] / 2
            light_cutoff_distance = offset_back
            
        #if is_z:
        
        #loc_z += offset_behind #Offset light from obj along z-axis        

        smidge = 0.001
        #smidge = 0
            
        """Top Backlight"""
        #loc_x -= offset_around
        #loc_z += 1 * (0.5 * offset_around)
        
        new_name = obj.name + 'BLight_T'
        
        #bpy.ops.object.light_add(type='AREA', location=(loc_x, loc_y, loc_z + (obj.dimensions[1] / 2)))       
        bpy.ops.object.light_add(type='AREA', location=(loc_x, loc_y, loc_z + (obj.dimensions[1] / 2) + smidge)) #2 Notes:
       
        #The y-dimension axis is the z-dimension axis because rotated text cannot be applied (reset); cut the z-dimension in half, add it to the object's z-location; you cannot put the lights centered at the offset without needing to increase the cutoffdistance beyond the object's dimensions everywhere.
        bpy.context.active_object.name = new_name
        
        spotlight = bpy.data.objects[new_name]        
        spotlight.data.color = [red, green, blue]
        spotlight.data.energy = brightness
        spotlight.data.use_custom_distance = True
        spotlight.data.cutoff_distance =  obj.dimensions[0] #X-axis of obj #OLD light_cutoff_distance #0.6
        
        #spotlight.data.spot_size = 1.5708 #90 degrees
        #spotlight.data.spot_size = 3.14159 #180 degrees
        #spotlight.data.spot_size = 0.523525
        #spotlight.data.shadow_soft_size = 0.25
        
        bpy.context.object.data.shape = 'RECTANGLE'
        bpy.context.object.data.size = obj.dimensions[0] #x-axes
        bpy.context.object.data.size_y = offset_back


        
        
        obj_old_col = spotlight.users_collection #list of all collections the txt_obj is in, the main scene by default
        new_col.objects.link(spotlight) #link txt_obj to new_col
        
        for ob in obj_old_col: #unlink from all previous collections
            
            ob.objects.unlink(spotlight)
        backlights += [spotlight]
        
        
        """Parent to Empty"""
        spotlight.parent = empty_controller
                
        #This is used to clear (i.e., not keep) transform 
        spotlight.matrix_parent_inverse = empty_controller.matrix_world.inverted()
        
                
        
        
        """Bottom Backlight"""
        #loc_x -= offset_around
        #loc_z += 1 * (0.5 * offset_around)
        
        new_name = obj.name + 'BLight_B'
        
        bpy.ops.object.light_add(type='AREA', location=(loc_x, loc_y, loc_z - (obj.dimensions[1] / 2) - smidge))       
        bpy.context.active_object.name = new_name
        
        spotlight = bpy.data.objects[new_name]        
        spotlight.data.color = [red, green, blue]
        spotlight.data.energy = brightness
        spotlight.data.use_custom_distance = True
        spotlight.data.cutoff_distance = obj.dimensions[0] #OLDlight_cutoff_distance #0.6
        
        #spotlight.data.spot_size = 1.5708 #90 degrees
        #spotlight.data.spot_size = 3.14159 #180 degrees
        #spotlight.data.spot_size = 0.523525
        #spotlight.data.shadow_soft_size = 0.25
        
        bpy.context.object.data.shape = 'RECTANGLE'        
        bpy.context.object.data.size = obj.dimensions[0]
        bpy.context.object.data.size_y = offset_back
        
        spotlight.rotation_euler[1] = 3.14159 #Point up 180 degs
        
        
   
        obj_old_col = spotlight.users_collection #list of all collections the txt_obj is in, the main scene by default
        new_col.objects.link(spotlight) #link txt_obj to new_col
        
        for ob in obj_old_col: #unlink from all previous collections
            
            ob.objects.unlink(spotlight)
        backlights += [spotlight]

        """Parent to Empty"""
        spotlight.parent = empty_controller
                        
        #This is used to clear (i.e., not keep) transform 
        spotlight.matrix_parent_inverse = empty_controller.matrix_world.inverted()
 
        
            
        """Mid Backlight"""
        #loc_x -= offset_around
        #loc_z += 1 * (0.5 * offset_around)
        
        new_name = obj.name + 'BLight_M'
        
        #Old
        #loc_y -= (offset_back/4)
        
        
        bpy.ops.object.light_add(type='AREA', location=(loc_x, loc_y - (offset_back/4) - smidge, loc_z))
        bpy.context.active_object.name = new_name
        
        spotlight = bpy.data.objects[new_name]        
        spotlight.data.color = [red, green, blue]
        spotlight.data.energy = brightness
        spotlight.data.use_custom_distance = True
        spotlight.data.cutoff_distance = obj.dimensions[1]/2#OLD light_cutoff_distance #0.6
        
        #spotlight.data.spot_size = 1.5708 #90 degrees
        #spotlight.data.spot_size = 3.14159 #180 degrees
        #spotlight.data.spot_size = 0.523525
        #spotlight.data.shadow_soft_size = 0.25
        
        bpy.context.object.data.shape = 'RECTANGLE'
        bpy.context.object.data.size = obj.dimensions[0] #x-axes
        bpy.context.object.data.size_y = obj.dimensions[1] #y-axes
        bpy.context.object.rotation_euler[0] = -1.5708

        
        
        obj_old_col = spotlight.users_collection #list of all collections the txt_obj is in, the main scene by default
        new_col.objects.link(spotlight) #link txt_obj to new_col
        
        for ob in obj_old_col: #unlink from all previous collections
            
            ob.objects.unlink(spotlight)
        backlights += [spotlight]
        
        """Parent to Empty"""
        spotlight.parent = empty_controller
        
                
        #This is used to clear (i.e., not keep) transform 
        spotlight.matrix_parent_inverse = empty_controller.matrix_world.inverted()
 
               
  
                
        """Left Backlight"""
        #loc_x -= offset_around
        #loc_z += 1 * (0.5 * offset_around)
        
        new_name = obj.name + 'BLight_L'
        
        bpy.ops.object.light_add(type='AREA', location=(loc_x - (obj.dimensions[0] / 2) - smidge, loc_y, loc_z))       
        bpy.context.active_object.name = new_name
        
        spotlight = bpy.data.objects[new_name]        
        spotlight.data.color = [red, green, blue]
        spotlight.data.energy = brightness
        spotlight.data.use_custom_distance = True
        spotlight.data.cutoff_distance = obj.dimensions[1] #OLDlight_cutoff_distance #0.6
        
        #spotlight.data.spot_size = 1.5708 #90 degrees
        #spotlight.data.spot_size = 3.14159 #180 degrees
        #spotlight.data.spot_size = 0.523525
        #spotlight.data.shadow_soft_size = 0.25
        
        bpy.context.object.data.shape = 'RECTANGLE'
        bpy.context.object.data.size = obj.dimensions[1]
        bpy.context.object.data.size_y = offset_back
        bpy.context.object.rotation_euler[1] = -1.5708

        
        
        obj_old_col = spotlight.users_collection #list of all collections the txt_obj is in, the main scene by default
        new_col.objects.link(spotlight) #link txt_obj to new_col
        
        for ob in obj_old_col: #unlink from all previous collections
            
            ob.objects.unlink(spotlight)
        backlights += [spotlight]
        
        """Parent to Empty"""
        spotlight.parent = empty_controller
        
                
        #This is used to clear (i.e., not keep) transform 
        spotlight.matrix_parent_inverse = empty_controller.matrix_world.inverted()
 
               
  
        
        
        """Right Backlight"""
        #loc_x -= offset_around
        #loc_z += 1 * (0.5 * offset_around)
        
        new_name = obj.name + 'BLight_R'
        
        bpy.ops.object.light_add(type='AREA', location=(loc_x + (obj.dimensions[0] / 2) + smidge, loc_y, loc_z))       
        bpy.context.active_object.name = new_name
        
        spotlight = bpy.data.objects[new_name]        
        spotlight.data.color = [red, green, blue]
        spotlight.data.energy = brightness
        spotlight.data.use_custom_distance = True
        spotlight.data.cutoff_distance = obj.dimensions[1] #OLD light_cutoff_distance #0.6
        
        #spotlight.data.spot_size = 1.5708 #90 degrees
        #spotlight.data.spot_size = 3.14159 #180 degrees
        #spotlight.data.spot_size = 0.523525
        #spotlight.data.shadow_soft_size = 0.25
        
        bpy.context.object.data.shape = 'RECTANGLE'
        bpy.context.object.data.size = obj.dimensions[1]
        bpy.context.object.data.size_y = offset_back
        bpy.context.object.rotation_euler[1] = 1.5708

        
        
        obj_old_col = spotlight.users_collection #list of all collections the txt_obj is in, the main scene by default
        new_col.objects.link(spotlight) #link txt_obj to new_col
        
        for ob in obj_old_col: #unlink from all previous collections
            
            ob.objects.unlink(spotlight)
        backlights += [spotlight]
        
        
        """Parent to Empty"""
        spotlight.parent = empty_controller
                
        #This is used to clear (i.e., not keep) transform 
        spotlight.matrix_parent_inverse = empty_controller.matrix_world.inverted()
     
  
            
        
        
    """End fn with our new objs selected"""
    for ob in bpy.context.selected_objects:
                
        obj.select_set(False)
    
    for backlight in backlights:
        
        backlight.select_set(True)    
    
    #Make active the first obj
    if objs:
        
        active_backlight_name = objs[0].name + 'BLight_T'
        active_backlight = bpy.data.objects[active_backlight_name]
        bpy.context.view_layer.objects.active = active_backlight        



def AddFacelightToSelected(offset_behind=0.75, brightness=100, light_cutoff_distance=0.6, is_x=False, is_y=True, is_z=False, red=1, green=1, blue=1):
    """Adds powerful backlight just behind selected objects, sets its affective distance low,
    adds it to its own collection named after the first object and 'BLight'
    Tip: create an empty to control them as a group and lift them up slightly higher than the 
    objects they light to give a top light.
    
    """
        
    objs = [o for o in bpy.context.selected_objects]
        
    new_col = bpy.data.collections.new(name=objs[0].name + 'FLight') #create new collection in data
    bpy.context.scene.collection.children.link(new_col) #add new collection to the scene  
    
    for obj in objs:
        
               
        loc_x = obj.location[0]
        loc_y = obj.location[1]
        loc_z = obj.location[2]
        
        if is_x:
            
            loc_x += offset_behind #Offset light from obj along x-axis
            
        if is_y:
        
            loc_y += offset_behind #Offset light from obj along y-axis
            
        if is_z:
        
            loc_z += offset_behind #Offset light from obj along z-axis
        
        
        new_name = obj.name + 'FLight'
        
        bpy.ops.object.light_add(type='POINT', location=(loc_x, loc_y, loc_z))       
        
        bpy.context.active_object.name = new_name
        
        bpy.data.objects[new_name].data.color = [red, green, blue]
        bpy.data.objects[new_name].data.energy = brightness
        bpy.data.objects[new_name].data.use_custom_distance = True
        bpy.data.objects[new_name].data.cutoff_distance = light_cutoff_distance
        
        obj_old_col = bpy.data.objects[new_name].users_collection #list of all collections the txt_obj is in, the main scene by default
        new_col.objects.link(bpy.data.objects[new_name]) #link txt_obj to new_col
        
        for ob in obj_old_col: #unlink from all previous collections
            
            ob.objects.unlink(bpy.data.objects[new_name])        


class Miscellaneous_PT_Panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Misc"
    bl_idname = "OBJECT_PT_Miscellaneous"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    #bl_context = "object"
    bl_category = "Misc" #Name in UI Panel

    def draw(self, context):
        
        layout = self.layout        
        
        #row = layout.row()
        #row.operator("wm.createnewcolop")
        row = layout.row()
        row.operator("wm.putselincolop")
        row = layout.row()
        row.operator("wm.addbacklightsop")
        row = layout.row()
        row.operator("wm.addfacelightsop")
        row = layout.row() 
        row.operator("wm.addspotlightop") 
        row = layout.row()
        row.operator("wm.vignetteop") 
        row = layout.row()
        row.operator("wm.cameralightop")
        row = layout.row()
        row.operator("wm.pngrendersetop")
        row.operator("wm.ffmpegrendersetop")        


class WM_OT_CreateNewCol(bpy.types.Operator):
    """"""
    
    bl_label = "Create New Collection"
    bl_idname = "wm.createnewcolop" 
    
    
    brightness: bpy.props.FloatProperty(name='', default=100)
    
    name: bpy.props.StringProperty(name='Name', default="New Collection")
    hide: bpy.props.BoolProperty(name="Hide Collection", default=False)
    
    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)      
      
    
    def draw(self, context):
        
        layout = self.layout
        box = layout.box() #Makes a box separator to separate text from bl_label
        
        #use row for multiple items sharing the same row, and layout otherwise
        row = box.row()
        #row.label(text="Name")
        row.prop(self, "name")
        
        row = box.row() #Ensures the following will share the same row
        #row.label(text="Hide")
        row.prop(self, "hide")
        
        """
        row = box.row() #Ensures the following will share the same row
        row.label(text="Brightness")        
        row.prop(self, "brightness")
                
        box = layout.box() #Makes a box separator
        row = box.row() #Ensures the following will share the same row in the box
        row.label(text="Placement axes:")
        
        row = box.row() #Ensures the following will share a different row in the same box as above
        row.prop(self, "is_x")
        row.prop(self, "is_y")
        row.prop(self, "is_z")
        
        box = layout.box() #Makes a box separator
        box.prop(self,"custom_rgb") #will be on its own row
        
        if self.custom_rgb: #makes conditional on having box checked
        
            row = box.row() #Ensures the following will share the same row in the box
        
            row.prop(self, "red")
            row.prop(self, "green")
            row.prop(self, "blue")
        """        
        
    def execute(self, context):
        
        name = self.name
        hide = self.hide

        CreateNewCol(name, hide)
        
        return {'FINISHED'}


class WM_OT_PutSelectedInCol(bpy.types.Operator):
    """Puts selected in the named collection, and creates it if it does not exist"""
    
    bl_label = "Move to Collection"
    bl_idname = "wm.putselincolop"
    
    name: bpy.props.StringProperty(name="Name", default="Collection")
    hide: bpy.props.BoolProperty(name="Hide Collection", default=False)
    keep_in_other_cols: bpy.props.BoolProperty(name="Keep In Other Collections", default=False)
    
    
    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)    
    
    
    def draw(self, context):
        
        layout = self.layout
        box = layout.box() #Makes a box separator to separate text from bl_label
        
        #use row for multiple items sharing the same row, and layout otherwise
        row = box.row()
        #row.label(text="Name")
        row.prop(self, "name")
        
        row = box.row() #Ensures the following will share the same row
        #row.label(text="Hide")
        row.prop(self, "hide")
        
        row = box.row() #Ensures the following will share the same row
        #row.label(text="Hide")
        row.prop(self, "keep_in_other_cols")
        
        """
        
        box = layout.box() #Makes a box separator
        box.prop(self,"custom_rgb") #will be on its own row
        
        if self.custom_rgb: #makes conditional on having box checked
        
            row = box.row() #Ensures the following will share the same row in the box
        
            row.prop(self, "red")
            row.prop(self, "green")
            row.prop(self, "blue")
        """
    
        
    def execute(self, context):
        
        name = self.name
        hide = self.hide        
        keep_in_other_cols = self.keep_in_other_cols

        PutSelectedInCol(name, hide, keep_in_other_cols)
        
        return {'FINISHED'}
    
    
        
class WM_OT_AddBacklights(bpy.types.Operator):
    """Adds backlights to the selected"""
    
    bl_label = "Add Backlights"
    bl_idname = "wm.addbacklightsop" 
    
    #primes: List[int] = []
    
    offset_around: bpy.props.FloatProperty(name='', default=0.35)
    offset_back: bpy.props.FloatProperty(name='', default=0.04) #Same as thickness of object (e.g. text)
    light_cutoff_distance: bpy.props.FloatProperty(name='', default=0.35)
    brightness: bpy.props.FloatProperty(name='', default=100)
    #text: bpy.props.StringProperty(name='', default="Select placement axis:") #Best I can do to easily insert some text without reformatting everything with a draw() fn

    is_x: bpy.props.BoolProperty(name="x", default=False)
    is_y: bpy.props.BoolProperty(name="y", default=True)
    is_z: bpy.props.BoolProperty(name="z", default=False)
    
    #custom_rgb: bpy.props.BoolProperty(name="Customize RGB values:", default=False)
    custom_rgb: bpy.props.BoolProperty(name="Customize RGB values", default=False)

    red: bpy.props.FloatProperty(name="Red", default=1)
    green: bpy.props.FloatProperty(name="Green", default=1)
    blue: bpy.props.FloatProperty(name="Blue", default=1)

    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)    

    
    def draw(self, context):
        layout = self.layout
        box = layout.box() #Makes a box separator to separate text from bl_label
        
        #use row for multiple items sharing the same row, and layout otherwise
        row = box.row()
        row.label(text="Distance Around")
        row.prop(self, "offset_around")
        row.label(text="Distance Behind")
        row.prop(self, "offset_back")
        
        row = box.row() #Ensures the following will share the same row
        row.label(text="Light Cutoff")
        row.prop(self, "light_cutoff_distance")
        
        row = box.row() #Ensures the following will share the same row
        row.label(text="Brightness")        
        row.prop(self, "brightness")
                
        box = layout.box() #Makes a box separator
        row = box.row() #Ensures the following will share the same row in the box
        row.label(text="Placement axes:")
        
        row = box.row() #Ensures the following will share a different row in the same box as above
        row.prop(self, "is_x")
        row.prop(self, "is_y")
        row.prop(self, "is_z")
        
        box = layout.box() #Makes a box separator
        box.prop(self,"custom_rgb") #will be on its own row
        
        if self.custom_rgb: #makes conditional on having box checked
        
            row = box.row() #Ensures the following will share the same row in the box
        
            row.prop(self, "red")
            row.prop(self, "green")
            row.prop(self, "blue")

    
    def execute(self, context):
        
        offset_around = self.offset_around
        offset_back = self.offset_back
        brightness = self.brightness
        light_cutoff_distance = self.light_cutoff_distance
        is_x = self.is_x
        is_y = self.is_y
        is_z = self.is_z
        red = self.red
        green = self.green
        blue = self.blue        

        AddBacklightToSelected(offset_around, offset_back, brightness, light_cutoff_distance, is_x, is_y, is_z, red, green, blue)
        
        return {'FINISHED'}  

        
class WM_OT_AddFacelights(bpy.types.Operator):
    """Adds facelights to the selected; used to illuminate faces"""
    
    bl_label = "Add Facelights"
    bl_idname = "wm.addfacelightsop" 
    
    #primes: List[int] = []
    
    offset_behind: bpy.props.FloatProperty(name='', default=0.75)
    light_cutoff_distance: bpy.props.FloatProperty(name='', default=0.6)
    brightness: bpy.props.FloatProperty(name='', default=100)
    #text: bpy.props.StringProperty(name='', default="Select placement axis:") #Best I can do to easily insert some text without reformatting everything with a draw() fn

    is_x: bpy.props.BoolProperty(name="x", default=False)
    is_y: bpy.props.BoolProperty(name="y", default=True)
    is_z: bpy.props.BoolProperty(name="z", default=False)
    
    #custom_rgb: bpy.props.BoolProperty(name="Customize RGB values:", default=False)
    custom_rgb: bpy.props.BoolProperty(name="Customize RGB values", default=False)

    red: bpy.props.FloatProperty(name="Red", default=1)
    green: bpy.props.FloatProperty(name="Green", default=1)
    blue: bpy.props.FloatProperty(name="Blue", default=1)

    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)    

    
    def draw(self, context):
        layout = self.layout
        box = layout.box() #Makes a box separator to separate text from bl_label
        
        #use row for multiple items sharing the same row, and layout otherwise
        row = box.row()
        row.label(text="Distance Behind")
        row.prop(self, "offset_behind")
        
        row = box.row() #Ensures the following will share the same row
        row.label(text="Light Cutoff")
        row.prop(self, "light_cutoff_distance")
        
        row = box.row() #Ensures the following will share the same row
        row.label(text="Brightness")        
        row.prop(self, "brightness")
                
        box = layout.box() #Makes a box separator
        row = box.row() #Ensures the following will share the same row in the box
        row.label(text="Placement axes:")
        
        row = box.row() #Ensures the following will share a different row in the same box as above
        row.prop(self, "is_x")
        row.prop(self, "is_y")
        row.prop(self, "is_z")
        
        box = layout.box() #Makes a box separator
        box.prop(self,"custom_rgb") #will be on its own row
        
        if self.custom_rgb: #makes conditional on having box checked
        
            row = box.row() #Ensures the following will share the same row in the box
        
            row.prop(self, "red")
            row.prop(self, "green")
            row.prop(self, "blue")

    
    def execute(self, context):
        
        offset_behind = self.offset_behind
        brightness = self.brightness
        light_cutoff_distance = self.light_cutoff_distance
        is_x = self.is_x
        is_y = self.is_y
        is_z = self.is_z
        red = self.red
        green = self.green
        blue = self.blue        

        AddFacelightToSelected(offset_behind, brightness, light_cutoff_distance, is_x, is_y, is_z, red, green, blue)
        
        return {'FINISHED'}  
    
    
class WM_OT_Add_SpotLight(bpy.types.Operator):
    """Adds a spotlight with a view axes empty that tracks where it points.\nConvention: Spotlights added that use the same name as another obj\nand with a likewise named view axes obj will use that same view axes"""
    
    bl_label = "Add Spotlight"
    bl_idname = "wm.addspotlightop"
    
    name: bpy.props.StringProperty(name="Name", default='New Spotlight')
    brightness: bpy.props.FloatProperty(name='Brightness', default=1000)
    red: bpy.props.FloatProperty(name="Red", default=1)
    green: bpy.props.FloatProperty(name="Green", default=1)
    blue: bpy.props.FloatProperty(name="Blue", default=1)
    x_val: bpy.props.FloatProperty(name="X loc", default=1)
    y_val: bpy.props.FloatProperty(name="Y loc", default=1)
    z_val: bpy.props.FloatProperty(name="Z loc", default=1)
        
    
    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)    
    
    
    def draw(self, context):
        
        layout = self.layout
        box = layout.box() #Makes a box separator to separate text from bl_label
        
        #use row for multiple items sharing the same row, and layout otherwise
        row = box.row()
        row.prop(self, "name") 
        row = box.row()
        #row.label(text="Name")
        row.prop(self, "brightness")      
        row = box.row() #Ensures the following will share the same row
        row.prop(self, "red")
        row.prop(self, "green")
        row.prop(self, "blue")
        row = box.row() #Ensures the following will share the same row
        row.prop(self, "x_val")
        row.prop(self, "y_val")
        row.prop(self, "z_val")
           
     
    def execute(self, context):
        
        name = self.name
        brightness = self.brightness
        red = self.red
        green = self.green
        blue = self.blue
        x_val = self.x_val
        y_val = self.y_val
        z_val = self.z_val
        
        view_axes_name = name + ' View Axes'
        same_view_axes = False
        
        #Convention: spotlights added that use the same name as another obj and with a likewise named view axes obj will use that same view axes
        if bpy.data.objects.get(name) and bpy.data.objects.get(view_axes_name):
            
            same_view_axes = True
            
        bpy.ops.object.light_add(type='SPOT', radius=1, location=(x_val, y_val, z_val))
        bpy.context.active_object.name = name
        spotlight = bpy.data.objects[name]
        

        spotlight.data.energy = brightness                
        #spotlight.rotation_euler[0] = 0
        #spotlight.rotation_euler[1] = 0
        #spotlight.rotation_euler[2] = 0
        spotlight.rotation_euler = (0, 0, 0)
        spotlight.data.color = (red, green, blue)

 
        
        #We will make previous named view axes the current one unless a new name is given
        if not same_view_axes:
            
            """Add and set view axes empty"""    

            bpy.ops.object.empty_add(type='PLAIN_AXES', location=(x_val-1, y_val-1, z_val-1))
            bpy.context.active_object.name = view_axes_name
        
        view_axes = bpy.data.objects[name + ' View Axes']
        view_axes.scale[0] = 5
        view_axes.scale[1] = 5
        view_axes.scale[2] = 5

                        
        """Tracking constraint"""

        spotlight.constraints.new(type='TRACK_TO')
        spotlight.constraints["Track To"].target = view_axes
        spotlight.constraints["Track To"].track_axis = 'TRACK_NEGATIVE_Z'
        spotlight.constraints["Track To"].up_axis = 'UP_Y'

        
        """Add the View Location to 'Lights Camera' collection"""
        """
        new_col = bpy.data.collections['Lights Camera'] #This was already created by a previous fn        
        obj_old_col = bpy.data.objects['View Location'].users_collection #list of all collections the obj is in, the main scene by default
        new_col.objects.link(bpy.data.objects['View Location']) #link obj to new_col
        
        for ob in obj_old_col: #unlink from all previous collections
            
            ob.objects.unlink(bpy.data.objects['View Location'])
        """
        return {'FINISHED'}  


class WM_OT_Camera_Light(bpy.types.Operator):
    """Puts selected in the named collection, and creates it if it does not exist"""
    
    bl_label = "Camera Light"
    bl_idname = "wm.cameralightop"
    
    brightness: bpy.props.FloatProperty(name='Brightness', default=1000)
    red: bpy.props.FloatProperty(name="Red", default=1)
    green: bpy.props.FloatProperty(name="Green", default=1)
    blue: bpy.props.FloatProperty(name="Blue", default=1)
    
    
    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)    
    
    
    def draw(self, context):
        
        layout = self.layout
        box = layout.box() #Makes a box separator to separate text from bl_label
        
        #use row for multiple items sharing the same row, and layout otherwise
        row = box.row()
        #row.label(text="Name")
        row.prop(self, "brightness")      
        row = box.row() #Ensures the following will share the same row
        row.prop(self, "red")
        row.prop(self, "green")
        row.prop(self, "blue")
           
     
    def execute(self, context):
        
        brightness = self.brightness
        red = self.red
        green = self.green
        blue = self.blue  
        
        bpy.data.objects['Camera Spotlight'].data.color = (red, green, blue)
        bpy.data.objects['Camera Spotlight'].data.energy = brightness
        
        return {'FINISHED'}          
 
class WM_OT_Vignette(bpy.types.Operator):
    """Tweak vignette. Set feather to 0 and position the oval to the desired edges with Scale. Scale at 1 positions it right along the edges. Move out to effectively disable it. Feather is the size of the area blurred"""
    
    bl_label = "Vignette Controls"
    bl_idname = "wm.vignetteop"
        
    scale_x: bpy.props.FloatProperty(name="Scale X", default=1, min=0, max=10)
    scale_y: bpy.props.FloatProperty(name="Scale Y", default=1, min=0, max=10)
    feather: bpy.props.FloatProperty(name="Feather", default=1, min=0, max=10)
    
    blur_x: bpy.props.FloatProperty(name="Blur X", default=250, min=0, max=2048)
    blur_y: bpy.props.FloatProperty(name="Blur Y", default=250, min=0, max=2048)
        
    
    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)    
    
    
    def draw(self, context):
        
        layout = self.layout
        box = layout.box() #Makes a box separator to separate text from bl_label
        
        #use row for multiple items sharing the same row, and layout otherwise
        row = box.row()
        #row.label(text="Name")
        row.prop(self, "brightness")
        row = box.row() #Ensures the following will share the same row
        row.prop(self, "scale_x")
        row.prop(self, "scale_y")   
  
        row = box.row() #Ensures the following will share the same row
        row.prop(self, "blur_x")
        row.prop(self, "blur_y")
        row = box.row() #Ensures the following will share the same row
        row.prop(self, "feather")  
           
     
    def execute(self, context):
        
        scale_x = self.scale_x
        scale_y = self.scale_y
 
        blur_x = self.blur_x
        blur_y = self.blur_y
        feather = self.feather


        bpy.context.scene.node_tree.nodes["Group"].node_tree.nodes["Blur"].size_x = blur_x
        bpy.context.scene.node_tree.nodes["Group"].node_tree.nodes["Blur"].size_y = blur_y
        bpy.context.scene.node_tree.nodes["Group"].inputs["X"].default_value = scale_x
        bpy.context.scene.node_tree.nodes["Group"].inputs["Y"].default_value = scale_y
        bpy.context.scene.node_tree.nodes["Group"].inputs["Feather"].default_value = feather
        
        
        return {'FINISHED'}          
 
     

class WM_OT_PNGRenderSettings(bpy.types.Operator):
    """Puts selected in the named collection, and creates it if it does not exist"""
    
    bl_label = "PNG Render Settings"
    bl_idname = "wm.pngrendersetop"
    
        
    def execute(self, context):
        
        bpy.context.scene.render.image_settings.file_format = 'PNG'
        bpy.context.scene.render.image_settings.color_mode = 'RGBA'
        bpy.context.scene.render.image_settings.color_depth = '16'
        
        return {'FINISHED'}

    
class WM_OT_FFmpegRenderSettings(bpy.types.Operator):
    """Puts selected in the named collection, and creates it if it does not exist"""
    
    bl_label = "FFMPEG Render Settings"
    bl_idname = "wm.ffmpegrendersetop"
    
        
    def execute(self, context):
        
        bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
        
        return {'FINISHED'}



classes = (

    Miscellaneous_PT_Panel, 
    WM_OT_PutSelectedInCol,
    WM_OT_AddBacklights,
    WM_OT_AddFacelights,
    WM_OT_Add_SpotLight,
    WM_OT_Camera_Light,
    WM_OT_Vignette,
    WM_OT_PNGRenderSettings,
    WM_OT_FFmpegRenderSettings,
         
    )

      
register, unregister = bpy.utils.register_classes_factory(classes)


if __name__ == "__main__":
    register()
    #bpy.ops.wm.animop('INVOKE_DEFAULT')

