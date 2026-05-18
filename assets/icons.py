import customtkinter as ctk
from iconipy import IconFactory

# Cache para evitar re-generar iconos repetidos
_factories = {}

# Genera icono de lucide como CTkImage
def get_icon(name, color, size=20):
    key = (name, color, size)
    if key not in _factories:
        factory = IconFactory(icon_set="lucide", icon_size=size, font_color=color)
        _factories[key] = factory.asPil(name)
        
    pil_img = _factories[key]
    return ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(size, size))
