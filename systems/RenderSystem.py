from ecs import System
import pygame
from newvector import Vector2

DEBUG = False
colors = [(255, 255, 255, 255), (255, 0, 255, 255), (0, 255, 255, 255), (255, 255, 0, 255)]

class RenderSystem(System):

    def __init__(self, surface):
        super(RenderSystem, self).__init__();
        self.requirements = ('Position', 'Drawable')
        self.surface = surface

    def process(self, entities, dt):
        self.surface.fill((0, 0, 0))
        images = []
        for entity in entities:
            drawable = entity.getComponent('Drawable')
            position = entity.getComponent('Position').value + drawable.offset

            # if DEBUG, we can draw hitboxes
            if DEBUG and entity.hasComponent('Dimension'):
                dimension = entity.getComponent('Dimension').value
                debugImage = pygame.Surface(dimension)
                debugImage.fill(colors[entity.id % 4])
                images.append((debugImage, position - drawable.offset, drawable.layer + 2))
            images.append((drawable, position, drawable.layer))

        sortedImages = sorted(images, key=lambda image: image[2])
        for drawable, position, layer in sortedImages:
            image = pygame.transform.flip(drawable.sprite.current(), drawable.flipped, False)
            self.surface.blit(image, position)
