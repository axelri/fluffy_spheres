from Sphere import *
from Image import *

def init_main():
    "Initiate pygame, initiate OpenGL, create a window, setup OpenGL"
    pygame.init()
    pygame.display.set_mode((640,480), OPENGL|DOUBLEBUF)
    pygame.display.set_caption("Fluffy spheres") 

    pygame.mouse.set_visible(0)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_COLOR_MATERIAL)

    glShadeModel(GL_SMOOTH)
    glDisable(GL_CULL_FACE)
    glColorMaterial(GL_FRONT, GL_DIFFUSE)

    glClearColor(0.1, 0, 0.1, 0)
    
            #Setup the camera
    glMatrixMode(GL_PROJECTION)

            #For the smaller window
    gluPerspective(45.0,640/480.0,0.1,10.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def Check_Clear():
    """Clear the window, check if user has closed the window or pressed escape,
    if so, return 0"""
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    for event in pygame.event.get():
        if event.type == QUIT or \
            (event.type == KEYDOWN and event.key == K_ESCAPE):
                return False
    return True

def createsphere():
    "Compile the drawing of a sphere for faster rendering"
    glColor3f(1, 1, 0)  #It won't change color...
    spheredisplay = glGenLists(1)
    glNewList(spheredisplay, GL_COMPILE)
    glutSolidSphere(1, 20, 20)
    glEndList()
    return spheredisplay

# Begin main routine
init_main()
# Create a Clock object to maintain framerate
clock = pygame.time.Clock()
displayListIndex = createsphere()
sphere = Sphere(displayListIndex)

run = True
while run:

    run = Check_Clear()
    glLoadIdentity()
    gluLookAt(0, 0, 3, 
            0, 0 ,0,
            0, 1, 0)

    sphere.update()
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
