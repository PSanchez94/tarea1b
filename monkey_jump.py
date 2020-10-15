import sys
import glfw
from OpenGL.GL import *

import easy_shaders as es
import scene_graph as sg
import transformations as tr

import monkey
import controller

controller = controller.Controller()


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
        elif key == glfw.KEY_SPACE and controller.jumpKeyOn:
            controller.jumpKeyOn = False


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 800
    height = 800

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
    main_scene_translate = sg.SceneGraphNode("main_scene")
    main_scene_translate.transform = tr.translate(-2.5, -2.5, 0)
    main_scene = sg.SceneGraphNode("main_scene")
    main_scene.transform = tr.uniformScale(0.4)
    main_scene.childs += [main_scene_translate]

    controller.createMonkey()

    cube = controller.monkey.createMonkey()
    main_scene_translate.childs += [cube]
    main_scene_translate.childs += [controller.drawStage()]

    # Our shapes here are always fully painted
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # Main window loop
    last_rot = 0

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        theta = 0.4*glfw.get_time()
        # Modifying only a specific node in the scene graph
        curr_time = glfw.get_time()+1
        past_time = curr_time - 0.05
        curr_i = int(curr_time)

        if controller.jumpKeyOn and controller.monkey.is_falling is False:
            controller.monkey.start_jump()

        controller.moveMonkey()

        cube.transform = tr.translate(controller.monkey.x, controller.monkey.y, 0)

        # Drawing
        sg.drawSceneGraphNode(main_scene, pipeline, "transform")

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()
