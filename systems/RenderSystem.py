from ecs import System
import pygame

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
            images.append((flippedImage, position, drawable.layer))

        sortedImages = sorted(images, key=lambda image: image[2])
        for surface, position, layer in sortedImages:
            self.surface.blit(surface, position)
