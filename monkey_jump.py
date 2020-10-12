import sys
import glfw
from OpenGL.GL import *

import easy_shaders as es
import scene_graph as sg
import transformations as tr

import monkey


class Controller:
    def __init__(self):
        self.leftKeyOn = False
        self.rightKeyOn = False
        self.jumpKeyOn = False


controller = Controller()


def on_key(window, key, scancode, action, mods):

    if action == glfw.PRESS:
        if key == glfw.KEY_LEFT:
            controller.leftKeyOn = True
        elif key == glfw.KEY_RIGHT:
            controller.rightKeyOn = True
        elif key == glfw.KEY_SPACE and not controller.jumpKeyOn:
            controller.jumpKeyOn = True
        elif key == glfw.KEY_ESCAPE:
            sys.exit()

    elif action == glfw.RELEASE:
        if key == glfw.KEY_LEFT:
            controller.leftKeyOn = False
        elif key == glfw.KEY_RIGHT:
            controller.rightKeyOn = False
        elif key == glfw.KEY_SPACE and not controller.jumpKeyOn:
            controller.jumpKeyOn = False


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Monkey Jump", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Assembling the shader program (pipeline) with both shaders
    pipeline = es.SimpleTransformShaderProgram()

    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.9, 0.9, 0.9, 1.0)

    # Enabling transparencies
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Creating shapes on GPU memory
    a_monkey = monkey.Monkey()
    cube = monkey.createMonkey()


    # Our shapes here are always fully painted
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # Main window loop
    last_rot = 0
    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        theta = 0.3 * glfw.get_time()
        # Modifying only a specific node in the scene graph
        curr_time = glfw.get_time()+1
        past_time = curr_time - 0.05
        curr_i = int(curr_time)

        if controller.leftKeyOn or controller.rightKeyOn:
            a_monkey.x += a_monkey.x_speed*(controller.rightKeyOn - controller.leftKeyOn)

        if controller.jumpKeyOn:

            if a_monkey.is_jumping is False:
                a_monkey.is_jumping = True
                jump_start_time = theta

            a_monkey.y += a_monkey.jump_speed*(
                    controller.jumpKeyOn - 20*controller.jumpKeyOn*((theta - jump_start_time)**2))

        cube.transform = tr.translate(a_monkey.x, a_monkey.y, a_monkey.z)

        # Drawing
        sg.drawSceneGraphNode(cube, pipeline, "transform")

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()