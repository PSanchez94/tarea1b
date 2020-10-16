import math
import sys
import csv
import glfw
from OpenGL.GL import *

import easy_shaders as es
import scene_graph as sg
import transformations as tr
import basic_shapes as bs

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


def createTextureQuad(image_filename, x, y, nx=1, ny=1):

    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
    #   positions        texture
         0.0, 0.0, 0.0,  0, ny,
         x, 0.0, 0.0, nx, ny,
         x,  y, 0.0, nx, 0,
         0.0,  y, 0.0,  0, 0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
         0, 1, 2,
         2, 3, 0]

    textureFileName = image_filename

    return bs.Shape(vertices, indices, textureFileName)


def createBackgroundScenes():
    sky1_texture = sg.SceneGraphNode("Sky 1 Texture")
    sky1_texture.transform = tr.translate(0.5, 0*4, 0)
    sky1_texture.childs += [es.toGPUShape(createTextureQuad("textures/sky1.png", 4, 4, 1, 1), GL_REPEAT, GL_NEAREST)]

    sky2_texture = sg.SceneGraphNode("Sky 2 Texture")
    sky2_texture.transform = tr.translate(0.5, 1*4, 0)
    sky2_texture.childs += [es.toGPUShape(createTextureQuad("textures/sky2.png", 4, 4, 1, 1), GL_REPEAT, GL_NEAREST)]

    sky3_texture = sg.SceneGraphNode("Sky 3 Texture")
    sky3_texture.transform = tr.translate(0.5, 2*4, 0)
    sky3_texture.childs += [es.toGPUShape(createTextureQuad("textures/sky3.png", 4, 4, 1, 1), GL_REPEAT, GL_NEAREST)]

    sky4_texture = sg.SceneGraphNode("Sky 4 Texture")
    sky4_texture.transform = tr.translate(0.5, 3*4, 0)
    sky4_texture.childs += [es.toGPUShape(createTextureQuad("textures/sky4.png", 4, 4, 1, 1), GL_REPEAT, GL_NEAREST)]

    forest_texture = sg.SceneGraphNode("Forest Texture")
    forest_texture.transform = tr.translate(0.5, -0.5, 0)
    forest_texture.childs += [es.toGPUShape(createTextureQuad("textures/forest.png", 4, 4, 1, 1), GL_REPEAT, GL_NEAREST)]

    trees_texture = sg.SceneGraphNode("Trees Texture")
    trees_texture.transform = tr.translate(0.5, -0.5, 0)
    trees_texture.childs += [es.toGPUShape(createTextureQuad("textures/trees.png", 4, 4, 1, 1), GL_REPEAT, GL_NEAREST)]

    sky = sg.SceneGraphNode("Sky")
    sky.childs += [sky1_texture] + [sky2_texture] + [sky3_texture] + [sky4_texture]

    forest = sg.SceneGraphNode("Forest")
    forest.childs += [forest_texture]

    trees = sg.SceneGraphNode("Trees")
    trees.childs += [trees_texture]

    return [sky] + [forest] + [trees]


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
    pipeline = es.SimpleTextureTransformShaderProgram()

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

    monkey = controller.monkey.createMonkey()
    monkey.childs += [es.toGPUShape(controller.monkey.hitboxShape("textures/monkey.png"), GL_REPEAT, GL_NEAREST)]
    main_scene_translate.childs += [monkey]
    main_scene_translate.childs += [controller.drawStage()]

    scene_movement = -0.5
    scene_moving = False
    monkey_right = False
    monkey_left = False

    monkey_texture = es.toGPUShape(controller.monkey.hitboxShape("textures/monkey.png"), GL_REPEAT, GL_NEAREST)
    monkey_texture_left1 = es.toGPUShape(controller.monkey.hitboxShape("textures/left1.png"), GL_REPEAT, GL_NEAREST)
    monkey_texture_left2 = es.toGPUShape(controller.monkey.hitboxShape("textures/left2.png"), GL_REPEAT, GL_NEAREST)
    monkey_texture_right1 = es.toGPUShape(controller.monkey.hitboxShape("textures/right1.png"), GL_REPEAT, GL_NEAREST)
    monkey_texture_right2 = es.toGPUShape(controller.monkey.hitboxShape("textures/right2.png"), GL_REPEAT, GL_NEAREST)

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

        # Jump is key has been pressed and monkey is airborne
        if controller.jumpKeyOn and controller.monkey.is_falling is False:
            controller.monkey.start_jump()

        # Move scene upon reaching 2 floors above current one
        if controller.monkey.y > controller.current_floor + 2 and scene_moving is False:
            scene_moving = True
            controller.current_floor = controller.monkey.y

        # Move the scene smoothly
        if scene_moving and scene_movement < controller.current_floor - 1.0:
            scene_movement += 0.05
            if scene_movement > controller.current_floor - 1.0:
                scene_moving = False

        # Lose condition upon reaching base of scene
        if controller.monkey.y < scene_movement + 0.3 and controller.lost is False:
            controller.lost = True
            controller.end_game_time = theta

        # Lose animation start and end
        if controller.lost:
            controller.monkey.collision = False
            controller.monkey.start_jump()
            controller.monkey.is_falling = False
            if theta - controller.end_game_time > 0.35:
                sys.exit("You fell out.")

        # Win condition
        if controller.won is False and controller.monkey.has_banana:
            controller.won = True
            controller.end_game_time = theta
        elif controller.won:
            if theta - controller.end_game_time > 0.5:
                sys.exit("You won!")
        else:
            controller.moveMonkey()

        # Scene translation
        monkey.transform = tr.translate(controller.monkey.x, controller.monkey.y, 0)
        sg.findNode(main_scene_translate, "Sky").transform = tr.translate(0.0, scene_movement * 0.3, 0)
        sg.findNode(main_scene_translate, "Forest").transform = tr.translate(0.0, scene_movement * 0.6, 0)
        sg.findNode(main_scene_translate, "Trees").transform = tr.translate(0.0, scene_movement * 0.1, 0)
        main_scene.transform = tr.translate(0.0, -scene_movement*0.6, 0)

        if controller.leftKeyOn:
            if monkey_left is False:
                monkey_left = True
            else:
                if math.ceil(math.sin(theta*30)) == 1:
                    sg.findNode(main_scene_translate, "Monkey Texture").childs = \
                        [monkey_texture_left1]
                else:
                    sg.findNode(main_scene_translate, "Monkey Texture").childs = \
                        [monkey_texture_left2]
        elif controller.leftKeyOn is False and monkey_left is True:
            monkey_left = False
            sg.findNode(main_scene_translate, "Monkey Texture").childs = \
                [monkey_texture]

        if controller.rightKeyOn:
            if monkey_right is False:
                monkey_right = True
            else:
                if math.ceil(math.sin(theta*30)) == 1:
                    sg.findNode(main_scene_translate, "Monkey Texture").childs = \
                        [monkey_texture_right1]
                else:
                    sg.findNode(main_scene_translate, "Monkey Texture").childs = \
                        [monkey_texture_right2]
        elif controller.rightKeyOn is False and monkey_right is True:
            monkey_right = False
            sg.findNode(main_scene_translate, "Monkey Texture").childs = \
                [monkey_texture]

        # Drawing
        sg.drawSceneGraphNode(main_scene, pipeline, "transform")

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()
