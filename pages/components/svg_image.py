from nicegui import ui

def svg_image(svg_path: str):
    with open(svg_path, 'r') as file:
        svg_content = file.read()
    
    return ui.html(svg_content)