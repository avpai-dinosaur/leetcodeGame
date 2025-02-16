import pygame

class Button:
	"""Represents a button on a game menu."""

	def __init__(self, image, pos, textInput, font, baseColor, hoveringColor):
		"""Constructor.
		
			image: Background image for the button.
			pos: Position of the button on screen.
			font: pygame.Font to use when rendering button text.
			baseColor: Default color to render button text in.
			hoveringColor: Color to render button text in during mouse over.
			textInput: Text to render on button.
		"""
		self.pos = pos

		self.font = font
		self.baseColor = baseColor
		self.hoveringColor = hoveringColor

		self.textInput = textInput
		self.text = self.font.render(self.textInput, True, self.baseColor)
		self.text_rect = self.text.get_rect(center=(self.pos))

		self.image = image
		# TODO: Fix this
		if self.image is None:
			self.image = self.text
		self.image_rect = self.image.get_rect(center=(self.pos))

	def checkMouseover(self, mousePosition):
		"""Change state of button based on mouse position.
		
		Returns True if the player's mouse is over the button.
		
			mousePosition: Current position of player's mouse.
		"""
		if mousePosition[0] in range(self.image_rect.left, self.image_rect.right) and mousePosition[1] in range(self.image_rect.top, self.image_rect.bottom):
			self.text = self.font.render(self.textInput, True, self.hoveringColor)
			return True
		
		self.text = self.font.render(self.textInput, True, self.baseColor)
		return False
	
	def action(self):
		"""Action to be executed for this button on click."""
		pass

	def update(self):
		"""Update state of the button."""
		mousePosition = pygame.mouse.get_pos()
		if self.checkMouseover(mousePosition):
			self.action()
	
	def draw(self, surface):
		"""Draw the button to the surface.
		
			surface: The pygame.Surface to blit the button on.
		"""
		if self.image is not None:
			surface.blit(self.image, self.image_rect)
		surface.blit(self.text, self.text_rect)