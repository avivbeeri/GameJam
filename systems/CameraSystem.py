import pygame
from ecs import System
from newvector import Vector2

class CameraSystem(System):

    def __init__(self):
        super(CameraSystem, self).__init__()
        self.requirements = ('Camera', 'Position')

    def process(self, entities, dt):
        for entity in entities:
            position = entity.getComponent("Position")
            camera = entity.getComponent("Camera")
            viewportSize = Vector2(camera.getViewport().get_size())

            # Assume the camera will center on a player entity

            # Get the player entity position/drawable
            # Camera following is inspired by this StackOverflow answer:
            # http://gamedev.stackexchange.com/a/44270
            if camera.type == 'follow':
                players = self.world.getManager('Group').get('player')
                player = next(iter(players))
                playerPosition = player.getComponent("Position").value
                if not player.hasComponent('Drawable'):
                    continue
                playerDrawable = player.getComponent("Drawable")
                newCameraPosition = \
                        playerPosition - viewportSize / 2 \
                                       + Vector2(playerDrawable.sprite.current().get_size()) / 2

                tileMap = self.world.getSystem('TileCollisionSystem').tileMap
                levelSize = Vector2(tileMap.mapSize[0] * tileMap.cellSize[0], tileMap.mapSize[1] * tileMap.cellSize[1])
                maxOffset = (levelSize - viewportSize)
                minOffset = Vector2(0, 0)
                if newCameraPosition.x > maxOffset.x:
                    newCameraPosition.x = maxOffset.x
                elif newCameraPosition.x < minOffset.x:
                    newCameraPosition.x = minOffset.x

                if newCameraPosition.y > maxOffset.y:
                    newCameraPosition.y = maxOffset.y
                elif newCameraPosition.y < minOffset.y:
                    newCameraPosition.y = minOffset.y

                position.value = newCameraPosition
