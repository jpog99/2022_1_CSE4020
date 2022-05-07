import os.path

import glfw
from OpenGL.GL import *
import numpy as np
from OpenGL.GLU import *

rmb_pressed = False
lmb_pressed = False

# ROTATE (default camera angle)
x_rotate = 45
y_rotate = 45

# PAN (default camera axes and target)
u = np.array([1, 0, 0])
v = np.array([0, 1, 0])
w = np.array([0, 0, 1])
target = np.array([0., 0., 0.])

# ZOOM (default camera distance)
zoom = 10

# last position of cursor in window
last_xpos = 0
last_ypos = 0

# mode toggles
projection_perspective = True
mode_wireframe = False
mode_singleMesh = True

# .obj parsing
varr = None #vertex array
narr = None #normal array
gVertexArraySeparate = np.empty((0, 3)) #index array for v and vn

#hierarchical models
global roadObj, heliObj, vanObj, treeObj, iceCreamObj, musicObj, birdObj, dogObj

I = np.identity(3)

def render():
    global gVertexArraySeparate
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    if mode_wireframe:
        glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
    else:
        glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    if projection_perspective:
        gluPerspective(45, 1, 1, 1000)
    else:
        glOrtho(-10, 10, -10, 10, -1000, 1000)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    rad_x_rotate = np.radians(x_rotate)
    rad_y_rotate = np.radians(y_rotate)
    dist = 30 * np.cos(rad_y_rotate)

    # set camera location according to last pan and rotate
    eye = np.array([target[0] + dist * np.sin(rad_x_rotate), target[1] + 30 * np.sin(rad_y_rotate),
                       target[2] + dist * np.cos(rad_x_rotate)])

    # rotation matrix about y axis
    M_azimuth = np.array([[np.cos(rad_x_rotate), 0., np.sin(rad_x_rotate)],
                   [0., 1., 0.],
                   [-np.sin(rad_x_rotate), 0., np.cos(rad_x_rotate)]])

    # rotation matrix about x axis
    M_elevation = np.array([[1., 0., 0.],
                   [0., np.cos(rad_y_rotate), np.sin(rad_y_rotate)],
                   [0., -np.sin(rad_y_rotate), np.cos(rad_y_rotate)]])

    M = M_azimuth @ M_elevation

    global u,v,w
    u = M @ I[0]
    v = M @ I[1]
    w = M @ I[2]

    u = u / np.sqrt(np.dot(u, u))
    v = v / np.sqrt(np.dot(v, v))
    w = w / np.sqrt(np.dot(w, w))

    #scale w vector (camera distance) with zoom
    eye += zoom * w

    Mv = np.array([[u[0], u[1], u[2], -np.dot(u, eye)],
                   [v[0], v[1], v[2], -np.dot(v, eye)],
                   [w[0], w[1], w[2], -np.dot(w, eye)],
                   [0, 0, 0, 1]])

    glMultMatrixf(Mv.T)

    glDisable(GL_LIGHTING)
    drawFrame()
    drawXZ()

    #### LIGHTINGS #####
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHT2)
    glEnable(GL_NORMALIZE)

    #light 0
    lightPos = (-10., -10., -10., 1)
    lightColor = (1., 0., 0., 1.)
    ambientLightColor = (.1, .0, .0, 1)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)

    #light 1
    lightPos = (10., 10., 10., 1)
    lightColor = (1., 1., 0., 1.)
    ambientLightColor = (.1, .1, .1, 1)
    glLightfv(GL_LIGHT1, GL_POSITION, lightPos)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT1, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLightColor)

    #light 2
    lightPos = (-10., 10., 10., 0)
    lightColor = (0., 0., 1., 1)
    ambientLightColor = (.0, .0, .1, 1)
    glLightfv(GL_LIGHT2, GL_POSITION, lightPos)
    glLightfv(GL_LIGHT2, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT2, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT2, GL_AMBIENT, ambientLightColor)

    objectColor = (.5, .5, .5, 1.)
    specularObjectColor = (1., 1., 1., 1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 5)

    if mode_singleMesh:
        drawObj(gVertexArraySeparate)
    else:
        animateHierarchicalModel()

def drawObj(vertexArraySeparate):
    iarr = vertexArraySeparate
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_DOUBLE, 6*iarr.itemsize, iarr)
    glVertexPointer(3, GL_DOUBLE, 6*iarr.itemsize, ctypes.c_void_p(iarr.ctypes.data + 3*iarr.itemsize))
    glDrawArrays(GL_TRIANGLES, 0, int(iarr.size/6))

def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([1.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,1.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,1.]))
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global projection_perspective, mode_wireframe, mode_singleMesh
    if key == glfw.KEY_V and action == glfw.PRESS:
        projection_perspective = not projection_perspective
    if key == glfw.KEY_Z and action == glfw.PRESS:
        mode_wireframe = not mode_wireframe
    if key == glfw.KEY_H and action == glfw.PRESS:
        mode_singleMesh = False
        createHierarchicalModel()

def cursor_callback(window, xpos, ypos):
    global x_rotate, y_rotate, last_ypos, last_xpos,target
    if lmb_pressed == True:
        x_rotate -= xpos - last_xpos
        y_rotate += ypos - last_ypos

    elif rmb_pressed == True:
        target += (last_xpos - xpos)/100 * u
        target += (ypos - last_ypos)/100 * v
    last_xpos = xpos
    last_ypos = ypos

def button_callback(window, button, action, mod):
    global lmb_pressed, rmb_pressed
    if button == glfw.MOUSE_BUTTON_LEFT:
        if action == glfw.PRESS:
            lmb_pressed = True
        elif action == glfw.RELEASE:
            lmb_pressed = False
    elif button == glfw.MOUSE_BUTTON_RIGHT:
        if action == glfw.PRESS:
            rmb_pressed = True
        elif action == glfw.RELEASE:
            rmb_pressed = False

def scroll_callback(window, xoffset, yoffset):
    global zoom
    zoom -= yoffset
    # stops zooming when at maximum zoom
    # if zoom <= 0:
    #     zoom = 0

def drop_callback(window, paths):
    global varr,narr,gVertexArraySeparate,mode_singleMesh
    #clear previous .obj render
    mode_singleMesh = True
    varr = np.empty((0, 3))
    narr = np.empty((0, 3))
    gVertexArraySeparate = np.empty((0, 3))
    parseObjFile(paths[0])

def parseObjFile(paths):
    global varr,narr,gVertexArraySeparate
    face_total = 0
    face3v_count = 0
    face4v_count = 0
    faceManyV_count = 0

    f = open(paths,'r')
    while True:
        temp = []
        line = f.readline()
        if not line:
            break #eof
        words = line.split()
        if len(words) == 0: continue  # blank line
        if words[0] == 'v':
            for i in words:
                if i == 'v': continue
                else: temp.append(float(i))
            varr = np.append(varr, np.array([temp]), axis=0)
        elif words[0] == 'vn':
            for i in words:
                if i == 'vn': continue
                else: temp.append(float(i))
            narr = np.append(narr, np.array([temp]), axis=0)
        elif (words[0] == 'f'):
            face_total += 1
            if len(words) == 4:
                face3v_count += 1
            elif len(words) == 5:
                face4v_count += 1
            elif len(words) > 5:
                faceManyV_count += 1

            #append face to gVertexArraySeperate + triangulation algorithm
            #src: https://stackoverflow.com/questions/23723993/converting-quadriladerals-in-an-obj-file-into-triangles
            if len(words) >= 4:
                vertices = words[1:]
                for i in range(1, len(vertices)-1):
                    # split quads into triangles (bc render only using GL_TRIANGLES)
                    face = [vertices[0], vertices[i], vertices[i+1]]
                    for j in face:
                        arr = j.split('/') #only append normal (2nd element) and vertice (0th element) info of 'f' in obj file (which seperated by '//')
                        gVertexArraySeparate = np.append(gVertexArraySeparate, np.array([narr[int(arr[2])-1]]), axis=0)
                        gVertexArraySeparate = np.append(gVertexArraySeparate, np.array([varr[int(arr[0])-1]]), axis=0)

    print("File Name: ", paths.split('\\')[-1])
    print("Total number of faces: ", face_total)
    print("Number of faces with 3 vertices: ", face3v_count)
    print("Number of faces with 4 vertices: ", face4v_count)
    print("Number of faces with more than 4 vertices: ", faceManyV_count)

    return gVertexArraySeparate

def createHierarchicalModel():
    global narr, varr, gVertexArraySeparate, roadObj, vanObj, treeObj, iceCreamObj, musicObj, birdObj, dogObj
    dir = 'HierarchicalModelFiles'

    for filename in os.listdir(dir):
        path = os.path.join(dir, filename)
        varr = np.empty((0, 3))
        narr = np.empty((0, 3))
        gVertexArraySeparate = np.empty((0, 3))
        if path == os.path.join(dir, "road.obj"):
            roadObj = parseObjFile(path)
        elif path == os.path.join(dir, "van.obj"):
            vanObj = parseObjFile(path)
        elif path == os.path.join(dir, "tree.obj"):
            treeObj = parseObjFile(path)
        elif path == os.path.join(dir, "icecream.obj"):
            iceCreamObj = parseObjFile(path)
        elif path == os.path.join(dir, "music.obj"):
            musicObj = parseObjFile(path)
        elif path == os.path.join(dir, "bird.obj"):
            birdObj = parseObjFile(path)
        elif path == os.path.join(dir, "dog.obj"):
            dogObj = parseObjFile(path)

def animateHierarchicalModel():
    global roadObj, heliObj, vanObj, treeObj, iceCreamObj, musicObj, birdObj, dogObj
    t = glfw.get_time()

    #road
    glPushMatrix()
    glRotatef(t,0,1,0)
    glScalef(3., 3., 3.)
    drawObj(roadObj)

    #van
    glPushMatrix()
    glTranslatef(0,0,np.cos(t)*5)
    glScalef(.1,.1,.1)
    drawObj(vanObj)

    #ice cream
    glPushMatrix()
    glTranslatef(1,4,1)
    glScalef(.1,.1,.1)
    glRotatef(t*250,0,1,0)
    drawObj(iceCreamObj)
    glPopMatrix()

    #music
    glPushMatrix()
    glScalef(1,1,1)
    glRotatef(t*50,0,1,0)
    glTranslatef(10,3,0)
    drawObj(musicObj)
    glPopMatrix()
    glPopMatrix()

    #tree
    glPushMatrix()
    glScalef(.1,.1,.1)
    glTranslatef(20, 0, 20)
    glRotatef(t*5,0,1,0)
    drawObj(treeObj)

    #bird
    glPushMatrix()
    glRotatef(t*50,0,1,0)
    glTranslatef(10,20,10)
    glScalef(.1,.1,.1)
    drawObj(birdObj)
    glPopMatrix()

    #dog
    glPushMatrix()
    glTranslatef(np.cos(t)*5,0,3)
    glScalef(.5,.5,.5)
    drawObj(dogObj)
    glPopMatrix()

    glPopMatrix()
    glPopMatrix()

def drawXZ():
    glBegin(GL_LINES)
    glColor3ub(128,128,128)
    for i in range(-9,10):
        glVertex3fv(np.array([i,0,9]))
        glVertex3fv(np.array([i,0,-9]))
        glVertex3fv(np.array([9,0,i]))
        glVertex3fv(np.array([-9,0,i]))
    glEnd()

def main():
    global gVertexArraySeparate

    if not glfw.init():
        return
    window = glfw.create_window(800,800,"Wan's OpenGL Viewer", None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window,key_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_drop_callback(window, drop_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
