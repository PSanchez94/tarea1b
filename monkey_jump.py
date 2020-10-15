import sys
import csv
import glfw
from OpenGL.GL import *

import easy_shaders as es
import scene_graph as sg
import transformations as tr
import basic_shapes as bs

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

def createBackgroundScenes():
    sky1_texture = sg.SceneGraphNode("Sky 1 Texture")
    sky1_texture.transform = tr.translate(0.5, 0*4, 0)
    sky1_texture.childs += [es.toGPUShape(background(0.5, 0.5, 1.0))]

    sky2_texture = sg.SceneGraphNode("Sky 2 Texture")
    sky2_texture.transform = tr.translate(0.5, 1*4, 0)
    sky2_texture.childs += [es.toGPUShape(background(0.6, 0.6, 1.0))]

    sky3_texture = sg.SceneGraphNode("Sky 3 Texture")
    sky3_texture.transform = tr.translate(0.5, 2*4, 0)
    sky3_texture.childs += [es.toGPUShape(background(0.7, 0.7, 1.0))]

    sky4_texture = sg.SceneGraphNode("Sky 4 Texture")
    sky4_texture.transform = tr.translate(0.5, 3*4, 0)
    sky4_texture.childs += [es.toGPUShape(background(0.8, 0.8, 1.0))]

    forest_texture = sg.SceneGraphNode("Forest Texture")
    forest_texture.transform = tr.translate(0.5, -0.5, 0)
    forest_texture.childs += [es.toGPUShape(background(0.4, 0.4, 0.0))]

    trees_texture = sg.SceneGraphNode("Trees Texture")
    trees_texture.transform = tr.translate(0.5, -0.5, 0)
    trees_texture.childs += [es.toGPUShape(background(0.2, 0.2, 0.0))]

    sky = sg.SceneGraphNode("Sky")
    sky.childs += [sky1_texture] + [sky2_texture] + [sky3_texture] + [sky4_texture]

    forest = sg.SceneGraphNode("Forest")
    forest.childs += [forest_texture]

    trees = sg.SceneGraphNode("Trees")
    trees.childs += [trees_texture]

    return [sky] + [forest] + [trees]

def background(r, g, b):

    # Defining locations and colors for each vertex of the shape
    vertices = [
        #   positions        colors
        0.0, 0.0, 0.0, r, g, b,
        4.0, 0.0, 0.0, r, g, b,
        4.0, 4.0, 0.0, r, g, b,
        0.0, 4.0, 0.0, r, g, b]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2,
        2, 3, 0]

    return bs.Shape(vertices, indices)


if __name__ == "__main__":

    print(sys.argv[1])

    with open(sys.argv[1]) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            for i in range(3):
                if row[i] == "1":
                    controller.add_platform(i, line_count)
            line_count += 1

    controller.createBanana()
    print(controller.banana.y)

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
    main_scene_translate = sg.SceneGraphNode("Main Scene Translate")
    main_scene_translate.transform = tr.translate(-2.5, -2, 0)
    main_scene_translate.childs += createBackgroundScenes()

    main_scene_scale = sg.SceneGraphNode("Main Scene Scale")
    main_scene_scale.transform = tr.uniformScale(0.6)
    main_scene_scale.childs += [main_scene_translate]

    main_scene = sg.SceneGraphNode("Main Scene")
    main_scene.childs += [main_scene_scale]

    controller.createMonkey()

    cube = controller.monkey.createMonkey()
    main_scene_translate.childs += [cube]
    main_scene_translate.childs += [controller.drawStage()]

    scene_movement = -0.5
    scene_moving = False

    # Our shapes here are always fully painted
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

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

        if controller.monkey.y > controller.current_floor + 2 and scene_moving is False:
            scene_moving = True
            controller.current_floor = controller.monkey.y

        if scene_moving and scene_movement < controller.current_floor - 1.0:
            scene_movement += 0.05
            if scene_movement > controller.current_floor - 1.0:
                scene_moving = False

        if controller.banana.collidesWith(controller.monkey):
            sys.exit("Got da dude")

        cube.transform = tr.translate(controller.monkey.x, controller.monkey.y, 0)
        sg.findNode(main_scene_translate, "Sky").transform = tr.translate(0.0, scene_movement * 0.3, 0)
        sg.findNode(main_scene_translate, "Forest").transform = tr.translate(0.0, scene_movement * 0.6, 0)
        sg.findNode(main_scene_translate, "Trees").transform = tr.translate(0.0, scene_movement * 0.1, 0)
        main_scene.transform = tr.translate(0.0, -scene_movement*0.6, 0)

        # Drawing
        sg.drawSceneGraphNode(main_scene, pipeline, "transform")

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()
