from ecs import System
import pygame
from newvector import Vector2
import component

DEBUG = False
colors = [ \
    (255, 255, 255, 255), \
    (255, 0, 255, 255), \
    (0, 255, 255, 255), \
    (255, 255, 0, 255) \
]

class RenderSystem(System):

    def __init__(self, surface):
        super(RenderSystem, self).__init__();
        self.requirements = ('Position', 'Drawable')
        self.surface = surface

    def process(self, entities, dt):
        self.surface.fill((0, 0, 0))
        # Get the camera or use the default
        if self.world is not None:
            cameraEntities = self.world.getEntitiesWithComponents(['Camera'])
            if len(cameraEntities) == 0:
                cameraEntities = [createCamera(self.world, self.surface.get_size())]
        else:
            return

        cameras = []
        for cameraEntity in cameraEntities:
            camera = cameraEntity.getComponent('Camera')
            cameraPosition = cameraEntity.getComponent('Position').value
            cameras.append(camera)

            images = []
            for entity in entities:
                if not isOnCamera(cameraEntity, entity):
                    continue

                drawable = entity.getComponent('Drawable')
                position = entity.getComponent('Position').value + drawable.offset

                image = pygame.transform.flip(drawable.sprite.current(), drawable.flipped, False)
                images.append((image, position, drawable.layer))

                # if DEBUG, draw hitboxes
                if DEBUG and entity.hasComponent('Dimension'):
                    dimension = entity.getComponent('Dimension').value
                    debugImage = pygame.Surface(dimension)
                    debugImage.fill(colors[entity.id % 4])
                    images.append((debugImage, position - drawable.offset, drawable.layer + 2))

            viewport = camera.getViewport()
            viewport.fill((0, 0, 0))
            sortedImages = sorted(images, key=lambda image: image[2])
            for image, position, layer in sortedImages:
                renderPosition = position - cameraPosition
                renderPosition = Vector2(round(renderPosition.x), round(renderPosition.y))
                viewport.blit(image, renderPosition)

        # Render individual viewports to the screen surface display
        sortedCameras = sorted(cameras, key=lambda camera: camera.layer)
        for camera in sortedCameras:
            cameraView = camera.getViewport()
            cameraPosition = camera.viewportPosition
            self.surface.blit(cameraView, cameraPosition)

def isOnCamera(camera, entity):
    position = entity.getComponent('Position').value
    dimension = getDrawableEntityDimension(entity)

    cameraPosition = camera.getComponent('Position').value
    cameraDimension = Vector2(camera.getComponent('Camera').getViewport().get_size())

    return (int(position.x) < int(cameraPosition.x) + cameraDimension.x) and \
        (int(position.x) + dimension.x > int(cameraPosition.x)) and \
        (int(position.y) < int(cameraPosition.y) + cameraDimension.y) and \
        (int(position.y) + dimension.y > int(cameraPosition.y))

def getDrawableEntityDimension(entity):
    return Vector2(entity.getComponent('Drawable').sprite.current().get_size())

def createCamera(world, size):
    camera = world.createEntity()
    camera.addComponent(component.Position())
    camera.addComponent(component.Velocity())
    camera.addComponent(component.Acceleration())
    camera.addComponent(component.Camera(size))
    world.addEntity(camera)
    return camera
