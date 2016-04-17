import pygame

keys = {
	pygame.K_UP:"Up",
	pygame.K_DOWN:"Down",
	pygame.K_LEFT:"Left",
	pygame.K_RIGHT:"Right",
	pygame.K_ESCAPE:"Exit",
	pygame.K_SPACE:"Interact",
	pygame.K_LSHIFT:"Crouch",
	pygame.K_RSHIFT:"Crouch",
	pygame.K_LCTRL:"Camo",
	pygame.K_RCTRL:"Camo",
	pygame.K_RETURN:"Enter",
}

# User-defined Event values
USEREVENT     = pygame.USEREVENT
COLLISION     = USEREVENT + 1
GAMEOVER      = USEREVENT + 2
LEVELCOMPLETE = USEREVENT + 3
INTERACT      = USEREVENT + 4
SOUNDEVENT    = USEREVENT + 5