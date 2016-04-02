from ecs import System

class RenderSystem(System):

    def __init__(self, surface):
        super(RenderSystem, self).__init__();
        self.requirements = ('PositionComponent', 'DrawableComponent')
        self.surface = surface

    def process(self, entities):
        self.surface.fill((0, 0, 0))
        images = []
        for entity in entities:
            drawable = entity.getComponent('DrawableComponent')
            position = entity.getComponent('PositionComponent')
            images.append((drawable.image, position.value, drawable.layer))

        sortedImages = sorted(images, key=lambda image: image[2])
        for surface, position, layer in sortedImages:
            self.surface.blit(surface, position)
