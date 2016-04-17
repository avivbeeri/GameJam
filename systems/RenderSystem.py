from ecs import System
import pygame
from newvector import Vector2

DEBUG = False

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
            position = entity.getComponent('Position') .value + drawable.offset
            flippedImage = pygame.transform.flip(drawable.image, drawable.flipped, False)
            if DEBUG and entity.hasComponent('Dimension'):
                dimension = entity.getComponent('Dimension').value
                debugImage = pygame.Surface(dimension)
                debugImage.fill((10 * entity.id, 20 * entity.id, 30 * entity.id, 255))
                images.append((debugImage, position - drawable.offset, drawable.layer + 2))
            images.append((flippedImage, position, drawable.layer))

        sortedImages = sorted(images, key=lambda image: image[2])
        for surface, position, layer in sortedImages:
            self.surface.blit(surface, position)
