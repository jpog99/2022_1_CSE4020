import glfw
import numpy as np
from OpenGL.GL import *

key_input_list = list()

def render(M):
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

    T = np.array([[1., 0., .5],
                  [0., 1., 0.],
                  [0., 0., 1.]])

    R = np.array([[np.cos(M), -np.sin(M), 0.],
                  [np.sin(M), np.cos(M), 0.],
                  [0., 0., 1.]])

    G = R @ T
    # draw point p
    glBegin(GL_POINTS)
    # your implementation
    p = G @ np.array([.5, 0., 1.])
    glVertex2f(p[0],p[1])
    glEnd()

    # draw vector v
    glBegin(GL_LINES)
    # your implementation
    v1 = G @ np.array([0., 0., 1.])
    glVertex2f(0., 0.)
    glVertex2f(v1[0], v1[1])
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

    # Make the window's context current
    glfw.make_context_current(window)
    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Poll events
        glfw.poll_events()

        render(glfw.get_time())

        # Swap front and back buffers
        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()


