import glfw
from OpenGL.GL import *

priTypes = [GL_POINTS, GL_LINES, GL_LINE_STRIP, GL_LINE_LOOP, GL_TRIANGLES,GL_TRIANGLE_STRIP, GL_TRIANGLE_FAN, GL_QUADS, GL_QUAD_STRIP, GL_POLYGON]

def render(type):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(type)
    glVertex2f(-0.5, 0.5)
    glVertex2f(-0.5, -0.5)
    glVertex2f(0.5, -0.5)
    glVertex2f(0.5, 0.5)
    glEnd()

def key_callback(window, key, scancode, action, mods):
    render(priTypes[key-49])

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
    render(priTypes[3])

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Poll events
        glfw.poll_events()

        #glfw.set_key_callback(window, key_callback)

        # Swap front and back buffers
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()


