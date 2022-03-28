import glfw
import numpy as np
from OpenGL.GL import *

key_input_list = list()

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    # draw coordinate
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0., 0.]))
    glVertex2fv(np.array([1., 0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0., 0.]))
    glVertex2fv(np.array([0., 1.]))
    glEnd()

    glColor3ub(255 ,255, 255)

    #########################
    # implement here
    #########################
    global key_input_list
    for i in reversed(key_input_list):
        if i == glfw.KEY_Q:
            glTranslatef(-0.1, 0., 0.)
        elif i == glfw.KEY_E:
           glTranslatef(0.1, 0., 0.)
        elif i == glfw.KEY_A:
           glRotatef(10., 0., 0., 1.)
        elif i == glfw.KEY_D:
           glRotatef(-10., 0., 0., 1.)
        elif i == glfw.KEY_1:
            glLoadIdentity()
            key_input_list.clear()
            break

    drawTriangle()

def key_callback(window, key, scancode, action, mods):
    global key_input_list
    if action==glfw.PRESS or action==glfw.REPEAT:
        key_input_list.append(key)

def drawTriangle():
    # draw triangle
    glBegin(GL_TRIANGLES)
    glVertex2fv(np.array([0., .5]))
    glVertex2fv(np.array([0., 0.]))
    glVertex2fv(np.array([.5, 0.]))
    glEnd()


def main():
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(480, 480, "2019007901", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window,key_callback)
    # Make the window's context current
    glfw.make_context_current(window)
    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Poll events
        glfw.poll_events()

        render()

        # Swap front and back buffers
        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()


