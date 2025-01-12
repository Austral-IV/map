import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image

def split_uniques_and_intersection(list1, list2):
    unique1 = list(set(list1) - set(list2))
    unique2 = list(set(list2) - set(list1))
    intersection = list(set(list1) & set(list2))
    return unique1, unique2, intersection
def plot_countries(country_list, background=None, world=None):
    if world is None: world = pd.read_file("https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip")
    countries = world[
    world["NAME"].isin(country_list)
    ]
    # Calculate the bounding box of the countries
    bounds = countries.total_bounds  # [minx, miny, maxx, maxy]

    # Initialize the figure
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot()

    if background is None:
        ax.set_facecolor('lightgray')  # Light turquoise color for the ocean
    else:
        # Load the .avif image
        ax.set_facecolor('darkgreen')  # Light turquoise color for the ocean
        background = Image.open("C:\\Users\\juvar\\Documents\\personal\\Autamating\\map\\background.avif")

        
        # bounds = [bounds[0], bounds[1] + 30, bounds[2] - 50, bounds[3]] #min x, max x, top y, bottom y
        w = abs(bounds[1] - bounds[0])
        h = abs(bounds[3] - bounds[2])
        
        # background = background.resize((int(w), int(h)))
        # Plot the background image with adjusted extent
        # ax.set_xlim(bounds[0], bounds[2])
        # ax.imshow(background, extent=[bounds[0], bounds[2], bounds[3], bounds[1]], aspect='auto')
        ax.imshow(background, extent=[bounds[0], bounds[2], bounds[1], bounds[3] ], aspect='auto',
                  alpha=0.8)

    # Plot the countries
    countries.plot(
        ax=ax,
        cmap="Set3",
        edgecolor="black",
        alpha=0.8
    )
    bounds = list(ax.get_window_extent().bounds); 

    # Turn off axis ticks
    ax.set_xticks([])
    ax.set_yticks([])

    # Set the plot title
    plt.title("Countries I've visited")
    plt.show()

def plot_countries_combined(country_list_1, country_list_2, background=None, world=None):
    if world is None: world = pd.read_file("https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip")
    countries_lsit_1, countries_lsit_2, intersection = split_uniques_and_intersection(country_list_1, country_list_2)
    
    countries1 = world[
    world["NAME"].isin(countries_lsit_1)
    ]
    countries2 = world[
    world["NAME"].isin(countries_lsit_2)
    ]
    shared_countries = world[
        world["NAME"].isin(intersection)
    ]
    all_countries = pd.concat([countries1, countries2])
    # Calculate the bounding box of the countries
    bounds = all_countries.total_bounds  # [minx, miny, maxx, maxy]

    # Initialize the figure
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot()

    if background is None:
        ax.set_facecolor('lightgray')  # Light turquoise color for the ocean
    else:
        # Load the .avif image
        ax.set_facecolor('darkgreen')  # Light turquoise color for the ocean
        background = Image.open("C:\\Users\\juvar\\Documents\\personal\\Autamating\\map\\background.avif")

        
        # bounds = [bounds[0], bounds[1] + 30, bounds[2] - 50, bounds[3]] # min x, min x, max x, top y
                                                    # in imshow, this is: minx, maxx, bottomy, top y
        w = abs(bounds[1] - bounds[0])
        h = abs(bounds[3] - bounds[2])
        
        # background = background.resize((int(w), int(h)))
        # Plot the background image with adjusted extent
        # ax.set_xlim(bounds[0], bounds[2])
        # ax.imshow(background, extent=[bounds[0], bounds[2], bounds[3], bounds[1]], aspect='auto')
        ax.imshow(background, extent=[bounds[0], bounds[2]*1.3, bounds[1], bounds[3] ], aspect='auto',
                  alpha=0.8)

    # Plot the countries
    countries1.plot( ax=ax, edgecolor="black", color="pink", alpha=0.8)
    countries2.plot( ax=ax, edgecolor="black", color="lightblue", alpha=0.8)
    shared_countries.plot( ax=ax, edgecolor="black", color="purple", alpha=0.9)

    bounds = list(ax.get_window_extent().bounds); 

    # Turn off axis ticks
    ax.set_xticks([])
    ax.set_yticks([])

    # Set the plot title
    plt.title("Countries We've visited")
    plt.show()