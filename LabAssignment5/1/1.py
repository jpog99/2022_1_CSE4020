import glfw
import numpy as np
from OpenGL.GL import *

def drawFrame():
     glBegin(GL_LINES)
     glColor3ub(255, 0, 0)
     glVertex2fv(np.array([0.,0.]))
     glVertex2fv(np.array([1.,0.]))
     glColor3ub(0, 255, 0)
     glVertex2fv(np.array([0.,0.]))
     glVertex2fv(np.array([0.,1.]))
     glEnd()
def drawTriangle():
     glBegin(GL_TRIANGLES)
     glVertex2fv(np.array([0.,.5]))
     glVertex2fv(np.array([0.,0.]))
     glVertex2fv(np.array([.5,0.]))
     glEnd()
def drawBox():
    glBegin(GL_QUADS)
    glVertex2fv(np.array([0., .5]))
    glVertex2fv(np.array([0., 0.]))
    glVertex2fv(np.array([.5, 0.]))
    glVertex2fv(np.array([.5, .5]))
    glEnd()

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    # draw coordinate
    drawFrame()

    glColor3ub(255 ,255, 255)
    drawTriangle()

    glTranslatef(.6, 0, 0)
    glRotatef(30,0,0,1)
    drawFrame()
    glColor3ub(0, 0, 255)
    drawBox()

    glLoadIdentity()
    glRotatef(-90,0,0,1)
    glTranslatef(.3, 0, 0)
    drawFrame()
    glColor3ub(255, 0, 0)
    drawTriangle()

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

        render()

        # Swap front and back buffers
        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()


