from ecs import System

class RenderSystem(System):

    def __init__(self, surface):
        super(RenderSystem, self).__init__();
        self.requirements = ('PositionComponent', 'DrawableComponent')
        self.surface = surface

    def process(self, entities):
        surface = self.surface
        surface.fill((0, 0, 0))
        for entity in entities:
            drawable = entity.getComponent('DrawableComponent')
            position = entity.getComponent('PositionComponent')
            surface.blit(drawable.image, position.value)
