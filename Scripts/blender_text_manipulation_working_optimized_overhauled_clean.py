import bpy


def GetText(file_name):    
    """
    Copies text from text file into Blender. Include full file path to the text file. It will also name
    the text object and put it into its own collection, which is named the same as the text object, and 
    will remove it from any other collection. Names are provided by the text file according to the 
    conventions mentioned below.
    
    The text file is formated so that what follows 'NAME=' indicates what the text object will be named.
    '###' anywhere on a line indicates that it is commented out. 
    Blank lines are not included.
    
    GetText() will return a list of the names of the text added, in order of its being added, in order to be 
    used by later fns that modify the text by name.   
    """
    
    names_lst = []    
    y_offset, counter = 2, 0    
    text_file = open(file_name,'r') #Opens text file in read mode, so the below method may be used
    lines_lst = text_file.read().splitlines() #Avoids adding '/n' newline indicators to text! Old: text_file.readlines() #Assigns a list of every line of text_file
    text_file.close() #Be nice to the memory buffer
        
    for line in lines_lst:
        
        if len(line) == 0 or '###' in line: #We don't need blank lines, and '###' is used to comment out a line; note that '###' could be anywhere in the line

            continue        
        
        """Separate name and content of line"""                
        name_index = line.index('NAME=')        
        text_content = line[:name_index]
        font_index = line.index('FONT=')
        font = line[font_index:]
        text_content += font #Add complete font indicator back to end of text for SetText        
        post_name_index = name_index + 5
        text_name = line[post_name_index:font_index]    
        
        """Add text objects"""
        bpy.ops.object.text_add(enter_editmode=False, location=(0, counter * y_offset, 0)) #Add new text object
        counter += 1 #Any additional text is placed in different spot
        bpy.context.active_object.name = text_name #Set name of active object, which is the added object
        names_lst = names_lst + [text_name]
        bpy.data.objects[text_name].data.body = text_content #Set line to be content of text object
        
        """Make collections for text"""
        new_col = bpy.data.collections.new(name=text_name) #create new collection in data and give it same name as text
        bpy.context.scene.collection.children.link(new_col) #add new collection to the scene        
        obj_old_col = bpy.data.objects[text_name].users_collection #list of all collections the txt_obj is in, the main scene by default
        new_col.objects.link(bpy.data.objects[text_name]) #link txt_obj to new_col
        
        for ob in obj_old_col: #unlink from all previous collections
            
            ob.objects.unlink(bpy.data.objects[text_name])
    
    return names_lst
   

def SetText(names_lst):    
    """
    The text of the text names of names_lst will be extruded, beveled, rotated etc. It will no longer be (re)spaced
    evenly along the y-axis, since this will be assumed  be taken care of by the initialization fn that adds it.
    
    Change y_location_offset according to how spaced apart along the y-axis the text will be.
    
    This uses the Linux Libertine font with its style variations. Change the file path if it's different or a different font is desired.
        
        
    New lesson learned: when using active objects, always do the deselect all, select obj, then make obj active routine.
    """
    
    y_location_offset = 2
    y_location = 0
    count = 0

    for name in names_lst:
                       
        text_obj = bpy.data.objects[name]
        
        for ob in bpy.context.selected_objects: #Deselect any selected objects
            
            bpy.data.objects[ob.name].select_set(False)
            
        text_obj.select_set(True) #Select text_obj                
        bpy.context.view_layer.objects.active = text_obj #Sets the active object to be obj, needed below for setting origin        
        content = text_obj.data.body  
             
        """Setting Fonts"""
        
        font_index = content.index('FONT=') #If I return to this, put in a try/except test for this
        font = content[font_index:]
        content = content[:font_index] #Remove 'FONT= . . . ' from content
        text_obj.data.body = content
        
        print('Setting line:', content)
        font = font[5:]
        
        if font == 'LIN':
            
            """Linux Libertine"""        
            regular_font= "/usr/share/fonts/ttf-linux-libertine/LinLibertine_R.otf" #Filepaths for the fonts
            bold_font = "/usr/share/fonts/ttf-linux-libertine/LinLibertine_RB.otf"
            italics_font = "/usr/share/fonts/ttf-linux-libertine/LinLibertine_RI.otf"
            bold_italics_font = "/usr/share/fonts/ttf-linux-libertine/LinLibertine_RBI.otf"
            
        elif font == 'ANT':
            
            """Anton"""
            regular_font= "/usr/share/fonts/Anton/Anton-Regular.ttf" #Filepaths for the fonts
            bold_font = "/usr/share/fonts/ttf-linux-libertine/LinLibertine_RB.otf"
            italics_font = "/usr/share/fonts/ttf-linux-libertine/LinLibertine_RI.otf"
            bold_italics_font = "/usr/share/fonts/ttf-linux-libertine/LinLibertine_RBI.otf"
            
        elif font == 'FEL':
            
            regular_font= "/usr/share/fonts/IM_Fell_English/IMFellEnglish-Regular.ttf" #Filepaths for the fonts
            bold_font = "/usr/share/fonts/ttf-linux-libertine/LinLibertine_RB.otf"
            italics_font = "/usr/share/fonts/IM_Fell_English/IMFellEnglish-RegularItalic.ttf"
            bold_italics_font = "/usr/share/fonts/ttf-linux-libertine/LinLibertine_RBI.otf"
                               
        text_obj.data.font = bpy.data.fonts.load(regular_font)
        text_obj.data.font_bold = bpy.data.fonts.load(bold_font)
        text_obj.data.font_italic = bpy.data.fonts.load(italics_font)
        text_obj.data.font_bold_italic = bpy.data.fonts.load(bold_italics_font)
        
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN') #Same as in console: sets origin of active object to geometry
             
        """Setting Cemter, Origin Values"""
        text_obj.data.align_x = 'CENTER'
        text_obj.data.align_y = 'CENTER'

        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN') #Same as in console: sets origin of active object to geometry       
        
        """Set Location"""
        text_obj.location[0] = 0 #Set x-axis location to 0
        text_obj.location[1] = y_location
        text_obj.location[2] = .36 #For setting Linux Libertine on the x/y plane
        y_location = y_location + y_location_offset #Increment y_location so that text_obj's are y_location_offset apart
        text_obj.rotation_euler[0] = 1.5708 #entering ‘90’ into the x-axis rotation. 
                    
        """Final Set Origin to Geometry"""
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN') #Same as in console: sets origin of active object to geometry
       

def IndividuateCharsOfText(names_lst):    
    """
    Use the lst returned by GetText(), or else nsure that names_lst is a list of the names 
    of those text objects you want duplicated and then individuated into characters, because this fn won't.
    """
    
    y_offset = 0.1
       
    for name in names_lst:
        
        print('Separating characters for ', name)
       
        y_iter = 0        
        word_obj = bpy.data.objects[name]
                
        for ob in bpy.context.selected_objects: #First deselect any selected objects
            
            bpy.data.objects[ob.name].select_set(False)
            
        word_obj.select_set(True) #Needed or else weird results: set word_obj to selected
        bpy.context.view_layer.objects.active = word_obj #Set word_obj to active
        content = word_obj.data.body 
        
        i = 0        
           
        while i < len(content):
            
                if content[i] == ' ':                                
                    i += 1
                    continue          
                
                y_iter += 1
                
                for ob in bpy.context.selected_objects: #First deselect any selected objects
                    bpy.data.objects[ob.name].select_set(False)
                word_obj.select_set(True) #Once again this is needed or else weird results occur: set word_obj to selected
                bpy.context.view_layer.objects.active = word_obj #Always copy the original word object  
                            
                bpy.ops.object.duplicate()
                bpy.context.active_object.location[1] = word_obj.location[1] + (y_offset * y_iter)
                
                if len(content) < 3 or len(content) - i < 3:
                    
                    bpy.context.active_object.data.body = content[i]
                    
                    i += 1
                                           
                    continue
                
                if content[i] != '*': #Obvious optimization
                    
                    bpy.context.active_object.data.body = content[i]
                    
                    i += 1
                    
                    continue
                                
                if len(content) == 3 and content[i+1] == '*': #Is italics when content is just 3 chars

                    bpy.context.active_object.data.body = '**' + content[i+2]
                        
                    i += 3
                    
                    continue                
                
                if content[i+1] == '*' and content[i+2] == '*': #Is bold
                    
                    if len(content) - i == 3: #Check for a '***' tail here because it will check just half the time, assuming half of stylized characters are bold
                        
                        bpy.context.active_object.data.body = '***'
                        
                        i += 3
                    
                    else:
                        bpy.context.active_object.data.body = '***' + content[i+3]
                    
                        i += 4 
                        
                    continue
                
                if content[i+1] == '*': #is italics
                    
                    bpy.context.active_object.data.body = '**' + content[i+2]
                    
                    i += 3
                    
                    continue
                
                bpy.context.active_object.data.body = content[i] #Triggered for single '*'s                               

                i += 1
  

def StylizeText(names_lst):
        
        """Stylizes the text object and its characters.
        
        The first while loop is just for the text obj
        The fore loop below covers the stylized chars
        """
        
        for name in names_lst:
            
            print('Stylizing text and text characters for ', name)
            text_obj = bpy.data.objects[name]            
            content = text_obj.data.body
            
            for ob in bpy.context.selected_objects: #Deselect any selected objects
                
                bpy.data.objects[ob.name].select_set(False)
                
            text_obj.select_set(True) #Select text_obj                
            bpy.context.view_layer.objects.active = text_obj #Sets the active object to be obj, needed below for setting origin            
            bpy.ops.object.editmode_toggle() #Enter edit mode. Add more of these when debugging to see any updates to text_obj.data.body
            bpy.ops.font.move(type='LINE_BEGIN')
            
            i = 0
            
            while i + 2 < len(content):
         
                if content[i] != '*':
                
                    bpy.ops.font.move(type='NEXT_CHARACTER')
                
                    i += 1
                    
                    continue
            
                next_i = i + 1
                
                if i + 3 == len(content) and content[next_i] == '*': #Last char is italics, even if it is a *

                    bpy.ops.font.move(type='NEXT_CHARACTER')
                    bpy.ops.font.move(type='NEXT_CHARACTER')
                    bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION')
                    bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION')
                    bpy.ops.font.move_select(type='NEXT_CHARACTER')
                    bpy.ops.font.style_toggle(style='ITALIC')
                    bpy.ops.font.move(type='NEXT_CHARACTER') #Blender is weird here: to get cursor just past the newly italicized, go forward then back
                    bpy.ops.font.move(type='PREVIOUS_CHARACTER')
                
                    i += 3
                    
                    continue
                    
                next_next_i = i + 2
                
                if i + 4 == len(content) and content[next_i] == '*' and content[next_next_i] == '*': #Last char is bold, even if it is a *
                                    
                    bpy.ops.font.move(type='NEXT_CHARACTER')
                    bpy.ops.font.move(type='NEXT_CHARACTER')
                    bpy.ops.font.move(type='NEXT_CHARACTER')
                    bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION')
                    bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION')
                    bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION')
                    bpy.ops.font.move_select(type='NEXT_CHARACTER')
                    bpy.ops.font.style_toggle(style='BOLD')
                    bpy.ops.font.move(type='NEXT_CHARACTER') #Blender is weird here: to get cursor just past the newly bolded, go forward then back
                    bpy.ops.font.move(type='PREVIOUS_CHARACTER')
                                
                    i += 4
                    
                    continue
            
                if content[next_i] == '*' and content[next_next_i] == '*': #Is bold
                                    
                    bpy.ops.font.move(type='NEXT_CHARACTER')
                    bpy.ops.font.move(type='NEXT_CHARACTER')
                    bpy.ops.font.move(type='NEXT_CHARACTER')
                    bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION')
                    bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION')
                    bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION')
                    bpy.ops.font.move_select(type='NEXT_CHARACTER')
                    bpy.ops.font.style_toggle(style='BOLD')
                    bpy.ops.font.move(type='NEXT_CHARACTER') #Blender is weird here: to get cursor just past the newly bolded, go forward then back
                    bpy.ops.font.move(type='PREVIOUS_CHARACTER')
                                
                    i += 4
                    
                    continue
                
                if content[next_i] == '*' and content[next_next_i] != '*': #Is italics
                                   
                    bpy.ops.font.move(type='NEXT_CHARACTER')
                    bpy.ops.font.move(type='NEXT_CHARACTER')
                    bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION')
                    bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION')
                    bpy.ops.font.move_select(type='NEXT_CHARACTER')
                    bpy.ops.font.style_toggle(style='ITALIC')
                    bpy.ops.font.move(type='NEXT_CHARACTER') #Blender is weird here: to get cursor just past the newly italicized, go forward then back
                    bpy.ops.font.move(type='PREVIOUS_CHARACTER')
                
                    i += 3
                    
                    continue

                bpy.ops.font.move(type='NEXT_CHARACTER')
            
                i += 1
                
            bpy.ops.font.move(type='LINE_END') #Put at a default position                
            bpy.ops.object.editmode_toggle() #Re-enter object mode                
            col = text_obj.users_collection[0]
            
            for obj in col.objects:                
                
                if text_obj.name == obj.name or len(obj.data.body) == 1:
                    
                    continue
                
                content = obj.data.body
                
                for ob in bpy.context.selected_objects: #Deselect any selected objects
                    bpy.data.objects[ob.name].select_set(False)
                obj.select_set(True) #Select obj                
                bpy.context.view_layer.objects.active = obj #Sets the active object to be obj, needed below for setting origin            
                bpy.ops.object.editmode_toggle() #Enter edit mode. Add more of these when debugging to see any updates to text_obj.data.body
                bpy.ops.font.move(type='LINE_END')
                
                if len(content) == 4: #is bold
                    
                    bpy.ops.font.move(type='PREVIOUS_CHARACTER')
                    bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION')
                    bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION')
                    bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION')
                    bpy.ops.font.move_select(type='NEXT_CHARACTER')
                    bpy.ops.font.style_toggle(style='BOLD')
                    bpy.ops.font.move(type='LINE_END')

                if len(content) == 3: #is italics
                    
                    bpy.ops.font.move(type='PREVIOUS_CHARACTER')
                    bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION')
                    bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION')
                    bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION')
                    bpy.ops.font.move_select(type='NEXT_CHARACTER')
                    bpy.ops.font.style_toggle(style='ITALIC')
                    bpy.ops.font.move(type='LINE_END')
                
                bpy.ops.object.editmode_toggle() #Re-enter object mode
                    

def NameChars(names_lst):    
    """ 
    This fn finds only single characters in collections with one, longer word object, and names 
    each character in that colection according to "$NAMEOFWORDOBJ" + 'C' + str(###), in order of
    location along the y-axis.
    
    Maximum characters is 999 per single word of colection for guaranteed proper ordering by name (change code if needed).
       
    Findings: the obj.data.name comes apart from the obj.name name.
    
    I should not run/ change obj.data.name (unless perhaps if I should close some massive gaps between names in data after 
    deleting a whole bunch?), but rather obj.name. 
    
    Warning: do not change bpy.data.objects[txt].data.name; this does not change the viewable or findable through python name;
    my guess is that it is an internal to code name that keeps things clean internally that isn't meant to be viewable.    
    
    """   
                   
    for name in names_lst:
        
        col = bpy.data.objects[name].users_collection[0] #Recall that names_lst has only those names of text objects of one collection            
        count = 0 #Numbers in names reset according to collection                                      
        name_lst = []
        loc_lst = []
                        
        for obj in col.objects: # iterate through all objects of the collection                   
                
            if obj.type == 'FONT' and obj.name != name: #Check it's a text object: update, added name to allow for one character text objects
                        
                if len(obj.data.body) == 1: #Check it's a single character #Update: shouldn't need this anymore due to the above; test deleting later
                                                        
                    loc_y = bpy.data.objects[obj.name].location[1]
                    name_lst = name_lst + [obj.name] # a list of names in order of iteration
                    loc_lst = loc_lst + [loc_y] #y-axis locations in the same order

        ordered_loc_lst = loc_lst[:] #Important: duplicate lst by using list comprehension; without it loc_lst will be sort()ed below!
        ordered_loc_lst.sort()
                    
        for loc_data in ordered_loc_lst:
            
            name_index = loc_lst.index(loc_data)                                
            old_name = name_lst[name_index] #Get that name from name_lst 
                       
            count += 1
                           
            if count < 10:
                       
                bpy.data.objects[old_name].name = name + 'C00' + str(count) #Name based on name of single word in that collection from names_lst
                
            elif count < 100:
                        
                bpy.data.objects[old_name].name = name + 'C0' + str(count)
                                            
            else:
                        
                bpy.data.objects[old_name].name = name + 'C' + str(count)

    
def WordsAndItsCharsAlignedWithNewMesh(names_lst):    
    """
    This will duplicate the original text (the single text object of a collection with some chars 
    in that colection too--presumably all the chars of the text object), and convert the dupicate into
    a mesh, offset from original by .5 along the y-axis, and then remeshed with octree of 10, separated
    by loose parts, its character pieces joined together so only separate characters remain 
    (my join_char_pieces() fn), and then all chars of the original text aligned to each mesh character
    in order, and then offset .5 from the mesh along the y-axis. 
    
    The end result of this upon the correct pieces should be the original text object, the mesh object
    broken into characters and properly formatted .5 along the y-axis from the original, and then the text object characters 
    properly formatted .5 along the y-axis from the mesh characters.
    
    Note: I used to remesh the object too, but surprisingly when separated by loose parts, even touching characters
    will usually be a separate mesh object, but remeshing the whole text beforehand will get rid of the vertices
    that cross one anothers space and will make it into a non-separated mesh.
    """
    
    for name in names_lst:
        
        print('Converting ', name, ' to a MESH; separating it by loose parts.')
                
        for ob in bpy.context.selected_objects: #First deselect any selected objects
            
            bpy.data.objects[ob.name].select_set(False)
            
        bpy.data.objects[name].select_set(True) #Needed or else weird result: Select word obj
        bpy.context.view_layer.objects.active = bpy.data.objects[name] #Set word obj to active
        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, .5, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":True, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
                
        """Mesh code"""
        bpy.ops.object.convert(target='MESH') #Convert active to mesh
        bpy.ops.mesh.separate(type='LOOSE') #Probably does this to the active object
            
    
def LeftmostVerticesOfMeshesOfCol(col):    
    """
    Returns list of 2 lists of (properties of) mesh objects of the same collection: 1st has objects' names, and
    2nd has objects' leftmost verteces. Properties with the same indeces in the lists are of the same object. 
    """

    names_with_verts = []
    leftmost_verts = []            
    
    for obj in col.objects: #Iterate through objects
                                   
        if obj.type == 'MESH':
                    
            names_with_verts += [obj.name] #Add name to name lst
            
            if len(obj.data.vertices) == 0: #This also allows for blank spaces, with little added cost, besides several more assignments; better here in case this is called in the future                

                continue
                                                                          
            obj_start_vert = obj.data.vertices[0].co[0]  #Vertices[0] is just the first vertice, and .co[0] signifies location value of the x-axis               
            leftmost_vert = obj_start_vert #Starting data to compare
                                  
            for vert in obj.data.vertices: #Update leftmost verts that are found more left
    
                if vert.co[0] < leftmost_vert:
                            
                    leftmost_vert = vert.co[0]
                    
            leftmost_verts += [leftmost_vert] #Add to the lst
                                               
    return  [names_with_verts, leftmost_verts]                
        

def PiecesFinder(name, content):
    """ Checks how many lose parts are made per char mesh by 
    duplicating all char objects, converting them to a Mesh and breaking them apart and 
    counting how many there are by using Blender naming conventions. Returns a dictionary of
    chars with there number of loose parts if 2 or 3."""
    
    print('Checking how many loose parts there are per char of ', name)
    visited = []
    chars_loose_parts = {}
    char_count = 1
    
    for char in content:
        
        if char in visited:
            
            char_count += 1
            
            continue
        
        if char == ' ':
            
            continue
        
        visited += [char]
        
        if char_count > 99:
            
            char_str = str(char_count)
        
        if char_count < 100 and char_count > 9:
            
            char_str = '0' + str(char_count)
            
        if char_count < 10:
            
            char_str = '00' + str(char_count)
            
        char_name = name + 'C' + char_str        
        
        for ob in bpy.context.selected_objects: #First deselect any selected objects
            
            bpy.data.objects[ob.name].select_set(False)
            
        bpy.data.objects[char_name].select_set(True) #Needed or else weird result: Select char obj
        bpy.context.view_layer.objects.active = bpy.data.objects[char_name] #Set char obj to active
        
        """Duplicate Char, convert it to Mesh and break it into loose parts"""        
        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, .5, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":True, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
        bpy.ops.object.convert(target='MESH') #Convert active to mesh
        bpy.ops.mesh.separate(type='LOOSE') #Probably does this to the active object
        
        """How many loose parts?"""
        names_loose_parts = []
        
        for ob in bpy.context.selected_objects: #Rely on just new parts being selected
            
            names_loose_parts = [ob.name]
        
        names_loose_parts.sort() #Highest num at end of lst
        num_loose_parts = int(names_loose_parts[-1:][0][-3:]) #Brilliant
        
        if num_loose_parts > 1:
            
            chars_loose_parts[char] = num_loose_parts
        
        print('Deleting discovery piece(s) of ', char)
        bpy.ops.object.delete(use_global=False) #Deletes all selected, which is just all new loose mesh pieces
    
        char_count += 1
    
    return chars_loose_parts
        
def JoinCharsAndName(names_lst):    
    """Joins chars that need to be joined, and names the mesh chars in order.
    
    No more guessing or manually finding out how many pieces there are per character, now
    we use the dedicated fn above to make a dictionary of its discoveries on this.
    
    One FEL char's, 'ē', top bar ends up very stretched leftward, but this happens after it is bevelled.
    """
    
    for name in names_lst:
                        
        word_obj = bpy.data.objects[name]   
        col = bpy.data.objects[name].users_collection[0] #Recall that names_lst has only those names of text objects of one collection        
        content = word_obj.data.body           
        chars_loose_parts = PiecesFinder(name, content) #Dict of chars and how many pieces they have                           
        names_and_leftmost = LeftmostVerticesOfMeshesOfCol(col)              
        names = names_and_leftmost[0]
        leftmost_verts = names_and_leftmost[1]        
        ordered_leftmost_verts = leftmost_verts[:] #Duplicate since .sort() is destructive
        ordered_leftmost_verts.sort()       
        char_index = 0
        mesh_char_count = 0 #For naming mesh objs in order
        
        for char in content:
                       
            if char == ' ': #There are no individual space chars
                
                continue
                       
            ordered_char = ordered_leftmost_verts[char_index] #Find ordered char in unordered lsts                
            ordered_char_index = leftmost_verts.index(ordered_char)               
            leftmost_verts[ordered_char_index] = '' #Needed for vertices that have the same location, so the index returns a different index next time
            
            if char in chars_loose_parts and chars_loose_parts[char] == 2:
                
                print('Joining two pices of ', char, ' together')
                                
                for ob in bpy.context.selected_objects: #First deselect any selected objects
                    
                    bpy.data.objects[ob.name].select_set(False)
                
                ordered_char_plus_one = ordered_leftmost_verts[char_index + 1]                     
                ordered_char_index_plus_one = leftmost_verts.index(ordered_char_plus_one)                
                leftmost_verts[ordered_char_index_plus_one] = '' #Needed for vertices that have the same location, so the index returns a different index next time          
                
                """Needed to guarantee pieces are joined in correct order"""                
                char_piece_names = [names[ordered_char_index], names[ordered_char_index_plus_one]]
                char_piece_names.sort()                          
                piece_name = char_piece_names[0]
                piece_name_plus_one = char_piece_names[1]
                                                
                bpy.data.objects[piece_name].select_set(True)
                bpy.data.objects[piece_name_plus_one].select_set(True)
                bpy.context.view_layer.objects.active = bpy.data.objects[piece_name]                
                bpy.ops.object.join()
                
                ordered_char_index = names.index(piece_name)
                                
                char_index += 1
            
            if char in chars_loose_parts and chars_loose_parts[char] == 3:
                
                print('Joining three pices of ', char, ' together')                
                                
                """Joins 1st and 2nd pieces"""
                for ob in bpy.context.selected_objects: #First deselect any selected objects
                    
                    bpy.data.objects[ob.name].select_set(False)
                    
                ordered_char_plus_one = ordered_leftmost_verts[char_index + 1]
                ordered_char_plus_two = ordered_leftmost_verts[char_index + 2]                
                ordered_char_index_plus_one = leftmost_verts.index(ordered_char_plus_one)
                leftmost_verts[ordered_char_index_plus_one] = '' #Needed for vertices that have the same location, so the index returns a different index next time                
                ordered_char_index_plus_two = leftmost_verts.index(ordered_char_plus_two)                
                leftmost_verts[ordered_char_index_plus_two] = '' #Needed for vertices that have the same location, so the index returns a different index next time                
                
                """Needed to guarantee pieces are joined in correct order"""                
                char_piece_names = [names[ordered_char_index], names[ordered_char_index_plus_one], names[ordered_char_index_plus_two]]
                char_piece_names.sort()                                
                piece_name = char_piece_names[0]
                piece_name_plus_one = char_piece_names[1]
                piece_name_plus_two = char_piece_names[2]
                                                
                bpy.data.objects[piece_name].select_set(True)
                bpy.data.objects[piece_name_plus_one].select_set(True)
                bpy.context.view_layer.objects.active = bpy.data.objects[piece_name]
                bpy.ops.object.join()
                                
                """Joins 1st and 3rd pieces"""
                for ob in bpy.context.selected_objects: #First deselect any selected objects
                    
                    bpy.data.objects[ob.name].select_set(False)
                                                        
                bpy.data.objects[piece_name].select_set(True)
                bpy.data.objects[piece_name_plus_two].select_set(True)
                bpy.context.view_layer.objects.active = bpy.data.objects[piece_name]
                bpy.ops.object.join()
                
                ordered_char_index = names.index(piece_name)
                
                char_index += 2
                
            if char in chars_loose_parts and chars_loose_parts[char] > 3:
                
                raise RuntimeError('You have found the fabled char with over 3 parts!!! Delete ', char, ' from text file and rerun the script!')                        
            
            char_index += 1
                        
            """Let's name Mesh objs in order here. Note that using char_index instead of mesh_char_count
            leads to gaps in numbers since char_index is incremented more above when char pieces are joined"""
                       
            mesh_char_count += 1            
           
            obj = bpy.data.objects[names[ordered_char_index]]
                 
            if mesh_char_count < 10:
                       
                obj.name =  name + 'M00' + str(mesh_char_count)
                        
            elif mesh_char_count < 100:
                        
                obj.name = name + 'M0' + str(mesh_char_count)
                                            
            else:
                        
                obj.name = name + 'M' + str(mesh_char_count)


def SetOriginToGeometry(names_lst):    
    """
    For collections with equal amounts mesh and text chars (See: MeshCharsInColsWithTexrChars()--does
    not count the original text object, unles that is one character, which I won't ever do.             
    """
    
    for name in names_lst:
        
        print('Giving ', name, ' chars their origins.')
               
        col = bpy.data.objects[name].users_collection[0] #Recall that names_lst has only those names of text objects of one collection
        
        for obj in col.objects:
            
            if obj.type == 'MESH' or (obj.type == 'FONT' and len(obj.data.body) == 1):
                
                for ob in bpy.context.selected_objects: #Deselect any selected objects
                    
                    bpy.data.objects[ob.name].select_set(False)
                
                obj.select_set(True) #Select obj                
                bpy.context.view_layer.objects.active = obj #Sets the active object to be obj, needed below for setting origin        
                bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN') #Same as in console: sets origin of active object to geometry

             
def PlaceChars(names_lst):
    """
    We can easily do this due to our naming conventions of 'C' or 'M' + '###' for the tail of the names of 
    characters. 'M' is for mesh, 'C' is for plain (text) character.
    """
    
    for name in names_lst:
               
        print('Placing chars of ', name)
        
        col = bpy.data.objects[name].users_collection[0] #Recall that names_lst has only those names of text objects of one collection
         
        for obj in col.objects:
            
            if len(obj.name) < 5 or (obj.name[-3:].isnumeric() is False or obj.name[-4:-3] != 'C'):
                    
                continue
            
            c_obj = bpy.data.objects[obj.name]          
            prefix = obj.name[:-4]
            suffix = obj.name[-3:]          
            m_obj = bpy.data.objects[prefix + 'M' + suffix]          
            loc_x = m_obj.location[0]
            loc_y = m_obj.location[1] + 0.5           
            c_obj.location[0] = loc_x
            c_obj.location[1] = loc_y
            
            
def DeleteObjs(names_lst):
    
    for name in names_lst:
                
        del_obj = bpy.data.objects[name]
                
        for ob in bpy.context.selected_objects: #First deselect any selected objects
            bpy.data.objects[ob.name].select_set(False)
        del_obj.select_set(True) #Needed or else weird results: set del_obj to selected
        bpy.context.view_layer.objects.active = del_obj #Set del_obj to active    
        bpy.ops.object.delete(use_global=False) #Delete del_obj

        
def NewLines(names_lst, z_offset=0.85):    
    """Formats newlines separated by .85 as default along the z-axis."""
    
    for name in names_lst:
            
        text_obj = bpy.data.objects[name]
        content = text_obj.data.body 
        
        if len(content) < 5 or content[-5:] != 'NEWL*':
            
            continue
        
        print(name, " is a line, so let's stack it with its other lines!")

        """We assume the text is in order along the y-axis
        Do stuff to all lines of same name and update body so it no longet has 'NEWL*' at the end,
        and therefore later lines will be skipped when called later        
        """        
        max_line_name = name + 'L02'
        
        while max_line_name in names_lst:
            
            if int(max_line_name[-2:]) > 9:
                
                max_line_name = max_line_name[:-2] + str(int(max_line_name[-2:]) + 1)
                         
                continue
            
            max_line_name = max_line_name[:-1] + str(int(max_line_name[-1:]) + 1)        
        
        """Need to setback max_line_name back one because current version was not found in the names_lst"""        
        
        if int(max_line_name[-2:]) == 10: 
            
            max_line_name = max_line_name[:-2] + '09'                
        
        if int(max_line_name[-2:]) > 10:
                
            max_line_name = max_line_name[:-2] + str(int(max_line_name[-2:]) - 1)                
                        
        if  int(max_line_name[-2:]) < 10:
                      
            max_line_name = max_line_name[:-1] + str(int(max_line_name[-1:]) - 1)   
        
        """Relocate lines in order"""
        
        get_y = text_obj.location[1]
        get_z = text_obj.location[2]        
        lines = int(max_line_name[-2:])
        z_multiplier = lines - 1        
        
        for line in range(1, lines + 1):
            
            if line == 1:
                
                line_name = name                
                col = text_obj.users_collection[0]
                
            elif line < 10:
                
                line_name = name + 'L0' + str(line)                                
                col = bpy.data.objects[line_name].users_collection[0]
                
            elif line > 9:
                
                line_name = name + 'L' + str(line)                
                col = bpy.data.objects[line_name].users_collection[0]
                
            char_count = 0 #for eliminating 'NEWL*' ending from mesh and text chars
            mesh_count = 0
            
            for obj in col.objects:
                            
                if obj.type == 'FONT' and len(obj.data.body) == 1:
                    
                    char_count += 1
                    
                    obj.location[2] = obj.location[2] + (z_multiplier * z_offset) #Move z location
                    obj.location[1] = obj.location[1] - (line + line - 2) #Move y location
                
                    continue
            
                if obj.type == 'MESH': #Can remove if we assume that mesh chars = text chars; i.e. no mistakes in joining
                    
                    mesh_count += 1
                    
                    obj.location[2] = obj.location[2] + (z_multiplier * z_offset) #Move z location
                    obj.location[1] = obj.location[1] - (line + line - 2) #Move y location
                
                    continue            
                
                obj.location[2] = obj.location[2] + (z_multiplier * z_offset) #Move z location
                obj.location[1] = obj.location[1] - (line + line - 2) #Move y location
                            
            z_multiplier -= 1
            
            """To re-center text chars when 'NEWL*' is removed"""
            
            char_count_str = char_count
            char_count_min_five_str = char_count - 5
            
            if char_count_str < 100 and char_count_str > 9:
                
                char_count_str = '0' + str(char_count_str)
                
            elif char_count_str < 10:
                
                char_count_str = '00' + str(char_count_str)
                
            if char_count_min_five_str < 100 and char_count_min_five_str > 9:
                
                char_count_min_five_str = '0' + str(char_count_min_five_str)
                
            elif char_count_min_five_str < 10:
                
                char_count_min_five_str = '00' + str(char_count_min_five_str)                
                                    
            x_loc_pre = bpy.data.objects[line_name + 'C001'].location[0]
            
            if char_count_min_five_str == '000': #This conditional allows for blank lines
                
                char_count_min_five_str = '001'
                        
            x_loc_post = bpy.data.objects[line_name + 'C' + char_count_min_five_str].location[0]            
            x_mid = abs(x_loc_pre - x_loc_post) / 2            
            x_offset = x_mid - x_loc_post            
                                    
            """No more 'NEWL*' new method: this preserves style formatting"""                
                        
            for ob in bpy.context.selected_objects: #First deselect any selected objects
                
                bpy.data.objects[ob.name].select_set(False)
                
            line_text_obj = bpy.data.objects[line_name]
            line_text_obj.select_set(True) #Needed or else weird results may occur: set line_text_obj to selected
            bpy.context.view_layer.objects.active = line_text_obj #Set line_text_obj to active
                          
            bpy.ops.object.editmode_toggle()
            bpy.ops.font.move(type='LINE_END')
            bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION') #Deletes 'N'
            bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION') #'E'
            bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION') #'W'
            bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION') #'L'
            bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION') #'*'
            bpy.ops.object.editmode_toggle()           
                       
            """Delete all chars that form 'NEWL*' and then move over (re-center) all chars as if 'NEWL*' were never there"""              
                      
            chars_del_lst = []
            
            for num in range(char_count - 4, char_count + 1):
                
                if num > 99:
                    
                    c_del_name = line_name + 'C' + str(num)
                    m_del_name = line_name + 'M' + str(num)
                    chars_del_lst += [c_del_name] + [m_del_name]
                    
                    continue
                
                if num > 9:
                    
                    c_del_name = line_name + 'C0' + str(num)
                    m_del_name = line_name + 'M0' + str(num)
                    chars_del_lst += [c_del_name] + [m_del_name]
                    
                    continue                  
                    
                c_del_name = line_name + 'C00' + str(num)
                m_del_name = line_name + 'M00' + str(num)
                chars_del_lst += [c_del_name] + [m_del_name]
            
            print("Deleting lines signifier 'NEWL*' Mesh and Text Chars named in", chars_del_lst)
                            
            DeleteObjs(chars_del_lst)
                                    
            for obj in col.objects:               
            
                #if obj.type == 'MESH' or (obj.type == 'FONT' and len(obj.data.body) == 1): #OLD: this did not avoid original txt obj if it has just one char after 'NEWL*' is deleted
                if obj.name == line_text_obj.name:
                    
                    continue                
                    
                obj.location[0] = obj.location[0] + x_offset
                    

def ExtrudeBevelSetOriginOfTextObjs(names_lst, extrude=0.01, bevel_depth=0.01, bevel_res=0):
    
    """In addition to what's in the title, it converts the new character duplicates into meshes.
    
    Note: the origin of the mesh char will correspond with that of the text char.
    
    Add a bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN') to the end if desired; however,
    at a minimum, the mesh should probably be remeshed before doing this anyway, so leave it to further
    modification.
    
    """
    
    for name in names_lst:
        
        print('3Ding ', name, 'and its chars, then duplicating and converting them to MESH')
        
        col = bpy.data.objects[name].users_collection[0]        
        col_obj_names = [] #Need to use a names lst or duplicating objs will go on forever since they are updated to col.objects lst
        
        
        for obj in col.objects:
            
            col_obj_names += [obj.name]
            
        for obj_name in col_obj_names:
            
            obj = bpy.data.objects[obj_name]
            
            if obj.type == 'FONT':
                                       
                """Extrude and bevel"""
                obj.data.extrude = extrude #Default 0.01
                obj.data.bevel_depth = bevel_depth #Default 0.01
                obj.data.bevel_resolution = bevel_res #Default 0

                for ob in bpy.context.selected_objects: #Deselect any selected objects
                    
                    bpy.data.objects[ob.name].select_set(False)
                    
                obj.select_set(True) #Select obj                
                bpy.context.view_layer.objects.active = obj #Sets the active object to be obj, needed below for setting origin                
                bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN') #Same as in console: sets origin of active object to geometry
                              
                if len(obj.data.body) == 1:
                    
                                        
                    bpy.ops.object.duplicate()                    
                    bpy.context.active_object.location[1] -= 0.5
                    bpy.ops.object.convert(target='MESH')


def DeleteOldMeshCharsRenameNewOnes(names_lst):
    
    """This fn very much relies on Blender naming conventions when duplicating the char text objs
    above (as well as my own 'M##' naming convention for mesh chars. So if those conventions change, 
    this fn will definitely be broken. But they shouldn't really be expected to change. """
    
    for name in names_lst:
        
        col = bpy.data.objects[name].users_collection[0]        
        mesh_char_names_to_del = []
            
        for obj in col.objects:
        
            if obj.type != 'MESH':
            
                continue
            
            if obj.name[-4:-3] == 'M' and obj.name[-3:].isnumeric():
            
                mesh_char_names_to_del += [obj.name]
                
        for mesh_char_name in mesh_char_names_to_del:  
            
            print('Deleting old MESH obj ', mesh_char_name, 'and renaming new MESH obj to match')      
            
            obj = bpy.data.objects[mesh_char_name]
        
            for ob in bpy.context.selected_objects: #Deselect any selected objects
                
                bpy.data.objects[ob.name].select_set(False)
                
            obj.select_set(True) #Select obj                
            bpy.context.view_layer.objects.active = obj #Sets the active object to be obj, needed for deleting it
            bpy.ops.object.delete(use_global=False)
            
            """Rename new mesh char. This will eventually rename every new mesh obj;
            even out of order. If picks out the corresponding text char name to its mesh """
            
            new_mesh_old_name = mesh_char_name[:-4] + 'C' + mesh_char_name[-3:] + '.001'
            new_mesh_new_name = mesh_char_name            
            bpy.data.objects[new_mesh_old_name].name = new_mesh_new_name
                   


            
def MoveMeshCharsToOwnCol(names_lst, hide_mesh=True):
    
    """"""
    
    for name in names_lst:
        
        col = bpy.data.objects[name].users_collection[0]        
        mesh_char_names_to_move = []        
        
        for obj in col.objects:
            
            """New Lines Attempting to Clear Rotation
            Doesn't work! Cannot apply rotation"""
            """
            for ob in bpy.context.selected_objects: #Deselect any selected objects
            
                bpy.data.objects[ob.name].select_set(False)
            
            obj.select_set(True) #Select text_obj                
            bpy.context.view_layer.objects.active = obj #Sets the active object to be obj, needed below for setting origin   
            #New line, clears rotation so z-axis lines up with Blender z-axis
            bpy.ops.object.transform_apply(rotation=True)
            """
                        
            
            if obj.type != 'MESH':
            
                continue
            
            if obj.name[-4:-3] == 'M' and obj.name[-3:].isnumeric():
            
                mesh_char_names_to_move += [obj.name]
                        
                
        """Make Collection For Mesh Chars & Move Them There"""
        
        new_col_name = name + ' Ms' #Same name as text col but with ' Ms' appended
        new_col = bpy.data.collections.new(name=new_col_name)
        bpy.context.scene.collection.children.link(new_col) #add new collection to the scene
        
        for name_to_move in mesh_char_names_to_move:
                
            obj_old_col = bpy.data.objects[name_to_move].users_collection #list of all collections the txt_obj is in, the main scene by default
            new_col.objects.link(bpy.data.objects[name_to_move]) #link txt_obj to new_col
        
            for ob in obj_old_col: #unlink from all previous collections
            
                ob.objects.unlink(bpy.data.objects[name_to_move])  
                    
        #Hide this Mesh Char Col if ticked    
        if hide_mesh:
        
            for view_layer in bpy.context.scene.view_layers:
                
                for child in view_layer.layer_collection.children:
                
                    if child.name == new_col.name:
                
                        child.exclude = True
                        
                    
#Complete order
names_lst = GetText("/home/paul/Documents/Blender/Godel1formulas.txt")
SetText(names_lst)
IndividuateCharsOfText(names_lst)
StylizeText(names_lst)
NameChars(names_lst)
WordsAndItsCharsAlignedWithNewMesh(names_lst)
JoinCharsAndName(names_lst)
SetOriginToGeometry(names_lst)
PlaceChars(names_lst)
NewLines(names_lst)
ExtrudeBevelSetOriginOfTextObjs(names_lst)
DeleteOldMeshCharsRenameNewOnes(names_lst)
MoveMeshCharsToOwnCol(names_lst, True)
print('Text successfully added and formatted!')





