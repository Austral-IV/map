import pygame
import geopandas as gpd
import numpy as np
from shapely.geometry import Point
import pandas as pd

# Initialize Pygame
pygame.init()

# Set up the display
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Interactive World Map")

# Load the world map data
url = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"
world = gpd.read_file(url)

# Sample data
data = {
    'COUNTRY': ['United States of America', 'Canada', 'Brazil', 'France', 'China'],
    'incidents': [100, 50, 75, 30, 200],
    'additional_info': ['Info USA', 'Info Canada', 'Info Brazil', 'Info France', 'Info China']
}
incidents_df = pd.DataFrame(data)

# Merge the data
world = world.merge(incidents_df, how='left', left_on=['NAME'], right_on=['COUNTRY'])

# Initialize zoom and pan variables
zoom = 1.0
pan_x = 0
pan_y = 0

def convert_coords(geometry, width, height, zoom, pan_x, pan_y):
    bounds = world.total_bounds  # [minx, miny, maxx, maxy]
    
    # Calculate center point for zooming
    center_x = width / 2
    center_y = height / 2
    
    x_scale = (width * zoom) / (bounds[2] - bounds[0])
    y_scale = (height * zoom) / (bounds[3] - bounds[1])
    
    all_coords = []
    # Handle both single polygons and multipolygons
    if hasattr(geometry, 'geoms'):  # MultiPolygon
        for polygon in geometry.geoms:
            coords = []
            for x, y in polygon.exterior.coords:
                # Calculate position relative to center
                px = ((x - bounds[0]) * x_scale)
                py = height - ((y - bounds[1]) * y_scale)
                
                # Apply zoom around center
                px = (px - center_x) * zoom + center_x
                py = (py - center_y) * zoom + center_y
                
                # Apply pan
                px += pan_x
                py += pan_y
                
                coords.append((int(px), int(py)))
            all_coords.append(coords)
    elif hasattr(geometry, 'exterior'):  # Single Polygon
        coords = []
        for x, y in geometry.exterior.coords:
            px = ((x - bounds[0]) * x_scale)
            py = height - ((y - bounds[1]) * y_scale)
            
            # Apply zoom around center
            px = (px - center_x) * zoom + center_x
            py = (py - center_y) * zoom + center_y
            
            # Apply pan
            px += pan_x
            py += pan_y
            
            coords.append((int(px), int(py)))
        all_coords.append(coords)
    return all_coords


def convert_coords(geometry, width, height, zoom, pan_x, pan_y):
    bounds = world.total_bounds  # [minx, miny, maxx, maxy]

    # Calculate the center of the bounds
    bounds_center_x = (bounds[2] + bounds[0]) / 2
    bounds_center_y = (bounds[3] + bounds[1]) / 2

    # Base scales without zoom
    x_scale = width / (bounds[2] - bounds[0])
    y_scale = height / (bounds[3] - bounds[1])
    
    all_coords = []
    # Handle both single polygons and multipolygons
    if hasattr(geometry, 'geoms'):  # MultiPolygon
        for polygon in geometry.geoms:
            coords = []
            for x, y in polygon.exterior.coords:
                # Center the coordinates around origin
                px = (x - bounds_center_x) * x_scale
                py = (y - bounds_center_y) * y_scale
                
                # Apply zoom
                px *= zoom
                py *= zoom
                
                # Move back to screen space
                px += width / 2
                py = height - (py + height / 2)
                
                # Apply pan
                px += pan_x
                py += pan_y
                
                coords.append((int(px), int(py)))
            all_coords.append(coords)
    elif hasattr(geometry, 'exterior'):  # Single Polygon
        coords = []
        for x, y in geometry.exterior.coords:
            # Center the coordinates around origin
            px = (x - bounds_center_x) * x_scale
            py = (y - bounds_center_y) * y_scale
            
            # Apply zoom
            px *= zoom
            py *= zoom
            
            # Move back to screen space
            px += width / 2
            py = height - (py + height / 2)
            
            # Apply pan
            px += pan_x
            py += pan_y
            
            coords.append((int(px), int(py)))
        all_coords.append(coords)
    return all_coords
# Colors
BACKGROUND_COLOR = (50, 50, 50)
COUNTRY_COLOR = (100, 100, 100)
HIGHLIGHT_COLOR = (200, 200, 0)
TEXT_COLOR = (255, 255, 255)

# Font
font = pygame.font.Font(None, 36)

running = True
selected_country = None
hover_country = None
dragging = False
last_mouse_pos = None

while running:
    screen.fill(BACKGROUND_COLOR)
    
    # Get mouse position
    mouse_pos = pygame.mouse.get_pos()
    
    # Draw countries
    for idx, row in world.iterrows():
        if row.geometry is not None:
            try:
                all_coords = convert_coords(row.geometry, WINDOW_WIDTH, WINDOW_HEIGHT, zoom, pan_x, pan_y)
                color = COUNTRY_COLOR
                if row['NAME'] == hover_country:
                    color = HIGHLIGHT_COLOR
                
                # Draw each polygon in the country
                for coords in all_coords:
                    if len(coords) > 2:
                        pygame.draw.polygon(screen, color, coords, 1)
                        
                        # Check if mouse is over this polygon
                        if pygame.draw.polygon(screen, (0,0,0,0), coords).collidepoint(mouse_pos):
                            hover_country = row['NAME']
                            info_text = f"{row['NAME']}"
                            if pd.notnull(row['incidents']):
                                info_text += f" - Incidents: {row['incidents']}"
                            text_surface = font.render(info_text, True, TEXT_COLOR)
                            screen.blit(text_surface, (10, 10))
            except Exception as e:
                print(f"Error drawing {row['NAME']}: {e}")
                continue
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        #if pressing key: print the key
        elif event.type == pygame.KEYDOWN:
            # print(f"Key pressed: {event.key}")
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                dragging = True
                last_mouse_pos = pygame.mouse.get_pos()
        # key released
        elif event.type == pygame.KEYUP: 
            # print(f"Key released: {event.key}")
            if event.key == pygame.K_SPACE:
                dragging = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if hover_country:
                    selected_country = hover_country
                    print(f"Selected: {selected_country}")
            elif event.button == 2:  # Middle mouse button
                dragging = True
                last_mouse_pos = pygame.mouse.get_pos()
            elif event.button == 4:  # Mouse wheel up
                # Get mouse position before zoom
                mouse_x, mouse_y = pygame.mouse.get_pos()
                old_zoom = zoom
                
                # Apply zoom
                zoom *= 1.1
                zoom = min(zoom, 5.0)
                
                # Adjust pan to keep mouse position fixed
                if zoom != old_zoom:
                    scale_factor = 1 - (zoom / old_zoom)
                    pan_x += (mouse_x - WINDOW_WIDTH/2) * scale_factor
                    pan_y += (mouse_y - WINDOW_HEIGHT/2) * scale_factor
                
            elif event.button == 5:  # Mouse wheel down
                # Get mouse position before zoom
                mouse_x, mouse_y = pygame.mouse.get_pos()
                old_zoom = zoom
                
                # Apply zoom
                zoom /= 1.1
                zoom = max(zoom, 0.1)
                
                # Adjust pan to keep mouse position fixed
                if zoom != old_zoom:
                    scale_factor = 1 - (zoom / old_zoom)
                    pan_x += (mouse_x - WINDOW_WIDTH/2) * scale_factor
                    pan_y += (mouse_y - WINDOW_HEIGHT/2) * scale_factor
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 2:  # Middle mouse button
                dragging = False
                
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                current_mouse_pos = pygame.mouse.get_pos()
                if last_mouse_pos:
                    dx = current_mouse_pos[0] - last_mouse_pos[0]
                    dy = current_mouse_pos[1] - last_mouse_pos[1]
                    pan_x += dx
                    pan_y += dy
                last_mouse_pos = current_mouse_pos
    
    # Display zoom level
    zoom_text = f"Zoom: {zoom:.1f}x"
    zoom_surface = font.render(zoom_text, True, TEXT_COLOR)
    screen.blit(zoom_surface, (10, WINDOW_HEIGHT - 40))
    
    pygame.display.flip()

pygame.quit()