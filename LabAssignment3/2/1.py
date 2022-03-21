import glfw
import math
import numpy as np
from OpenGL.GL import *


gComposedM = np.array([[1., 0., 0.],
                      [0., 1., 0.],
                      [0., 0., 1.]])

def render(T):
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
    # draw triangle
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex2fv((T @ np.array([.0, .5, 1.]))[:-1])
    glVertex2fv((T @ np.array([.0, .0, 1.]))[:-1])
    glVertex2fv((T @ np.array([.5, .0, 1.]))[:-1])
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global gComposedM
    if key == glfw.KEY_1:
        if action == glfw.PRESS or action == glfw.REPEAT:
            gComposedM = np.array([[1., 0., 0.],
                                   [0., 1., 0.],
                                   [0., 0., 1.]])
    elif key == glfw.KEY_W:
        if action == glfw.PRESS or action == glfw.REPEAT:
            newM = np.array([[.9, 0., 0.],
                          [0., 1., 0.],
                          [0., 0., 1.]])
            gComposedM = newM @ gComposedM
    elif key == glfw.KEY_E:
        if action == glfw.PRESS or action == glfw.REPEAT:
            newM = np.array([[1.1, 0., 0.],
                             [0., 1., 0.],
                             [0., 0., 1.]])
            gComposedM = newM @ gComposedM
    elif key == glfw.KEY_S:
        if action == glfw.PRESS or action == glfw.REPEAT:
            th = math.radians(10)
            newM = np.array([[np.cos(th), -np.sin(th), 0.],
                          [np.sin(th), np.cos(th), 0.],
                          [0., 0., 1.]])
            gComposedM = newM @ gComposedM
    elif key == glfw.KEY_D:
        if action == glfw.PRESS or action == glfw.REPEAT:
            th = math.radians(10)
            newM = np.array([[np.cos(-th), -np.sin(-th), 0.],
                          [np.sin(-th), np.cos(-th), 0.],
                          [0., 0., 1.]])
            gComposedM = newM @ gComposedM
    elif key == glfw.KEY_X:
        if action == glfw.PRESS or action == glfw.REPEAT:
            newM = np.array([[1., -.1, 0.],
                             [0., 1., 0.],
                             [0., 0., 1.]])
            gComposedM = newM @ gComposedM
    elif key == glfw.KEY_C:
        if action == glfw.PRESS or action == glfw.REPEAT:
            newM = np.array([[1., .1, 0.],
                             [0., 1., 0.],
                             [0., 0., 1.]])
            gComposedM = newM @ gComposedM
    elif key == glfw.KEY_R:
        if action == glfw.PRESS or action == glfw.REPEAT:
            newM = np.array([[1., .1, 0.],
                             [0., -1., 0.],
                             [0., 0., 1.]])
            gComposedM = newM @ gComposedM

def main():
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(480,480,"2019007901", None,None)
    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)
    # Make the window's context current
    glfw.make_context_current(window)
    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Poll events
        glfw.poll_events()

        render(gComposedM)

        # Swap front and back buffers
        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()


