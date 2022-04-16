
# [Practice] Drawing Separate Triangles using Vertex Array
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

projection_perspective = True
I = np.identity(3)

def createVertexArraySeparate():
    varr = np.array([
            ( -1 ,  1 ,  1 ), # v0
            (  1 , -1 ,  1 ), # v2
            (  1 ,  1 ,  1 ), # v1

            ( -1 ,  1 ,  1 ), # v0
            ( -1 , -1 ,  1 ), # v3
            (  1 , -1 ,  1 ), # v2

            ( -1 ,  1 , -1 ), # v4
            (  1 ,  1 , -1 ), # v5
            (  1 , -1 , -1 ), # v6

            ( -1 ,  1 , -1 ), # v4
            (  1 , -1 , -1 ), # v6
            ( -1 , -1 , -1 ), # v7

            ( -1 ,  1 ,  1 ), # v0
            (  1 ,  1 ,  1 ), # v1
            (  1 ,  1 , -1 ), # v5

            ( -1 ,  1 ,  1 ), # v0
            (  1 ,  1 , -1 ), # v5
            ( -1 ,  1 , -1 ), # v4

            ( -1 , -1 ,  1 ), # v3
            (  1 , -1 , -1 ), # v6
            (  1 , -1 ,  1 ), # v2

            ( -1 , -1 ,  1 ), # v3
            ( -1 , -1 , -1 ), # v7
            (  1 , -1 , -1 ), # v6

            (  1 ,  1 ,  1 ), # v1
            (  1 , -1 ,  1 ), # v2
            (  1 , -1 , -1 ), # v6

            (  1 ,  1 ,  1 ), # v1
            (  1 , -1 , -1 ), # v6
            (  1 ,  1 , -1 ), # v5

            ( -1 ,  1 ,  1 ), # v0
            ( -1 , -1 , -1 ), # v7
            ( -1 , -1 ,  1 ), # v3

            ( -1 ,  1 ,  1 ), # v0
            ( -1 ,  1 , -1 ), # v4
            ( -1 , -1 , -1 ), # v7
            ], 'float32')
    return varr

def render():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glLoadIdentity()

    if projection_perspective:
        gluPerspective(45, 1, 1, 1000)
    else:
        glOrtho(-10, 10, -10, 10, -1000, 1000)

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

    # rotation matrix about z axis
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

    drawFrame()
    drawXZ()
    glColor3ub(255, 255, 255)

    # drawCube_glVertex()
    drawCube_glDrawArrays()


def drawCube_glDrawArrays():
    global gVertexArraySeparate
    varr = gVertexArraySeparate
    glEnableClientState(GL_VERTEX_ARRAY)  # Enable it to use vertex array
    glVertexPointer(3, GL_FLOAT, 3*varr.itemsize, varr)
    glDrawArrays(GL_TRIANGLES, 0, int(varr.size/3))

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
    global projection_perspective
    if key == glfw.KEY_V and action == glfw.PRESS:
        projection_perspective = not projection_perspective

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

def drawXZ():
    glBegin(GL_LINES)
    glColor3ub(128,128,128)
    for i in range(-9,10):
        glVertex3fv(np.array([i,0,9]))
        glVertex3fv(np.array([i,0,-9]))
        glVertex3fv(np.array([9,0,i]))
        glVertex3fv(np.array([-9,0,i]))
    glEnd()

gVertexArraySeparate = None
def main():
    global gVertexArraySeparate

    if not glfw.init():
        return
    window = glfw.create_window(640,640,"Wan's OpenGL Viewer", None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window,key_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_scroll_callback(window, scroll_callback)

    gVertexArraySeparate = createVertexArraySeparate()

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
