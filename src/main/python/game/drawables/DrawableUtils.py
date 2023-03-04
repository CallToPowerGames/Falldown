import pygame

def draw_text_in_rect(surface, text, color, font, rect, center=None, aa=False, colorkey=None):
    """Draws text in a rectangle

    :param text: The text
    :param color: The color
    :param font: The font
    :param rect: The rectangle
    :param center: The center rectangle
    :param aa: Anti-aliasing
    :param colorkey: The color key
    """
    rect = pygame.Rect(rect)
    y = rect.top

    # get the height of the font
    fontHeight = font.size('Tg')[1]

    i = 1

    # determine maximum width of line
    while font.size(text[:i+1])[0] < (rect.width - 5) and i < len(text):
        i += 1

    # render the line and blit it to the surface
    if colorkey:
        image = font.render(text[:i], 1, color, colorkey)
        image.set_colorkey(colorkey)
        image_rect = image.get_rect()
    else:
        image = font.render(text[:i], aa, color)
        image_rect = image.get_rect()
        if center:
            image_rect.center = center

    surface.blit(image, image_rect)
