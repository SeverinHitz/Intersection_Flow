import os
import random
import matplotlib.pyplot as plt
from IntersectionTrafficFlow import IntersectionTrafficFlow

fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(20,20))
plt.tight_layout()

# First Intersection
custom_1 = {'High Street': 0, 'Kings Road': 240, 'Park Avenue': 60, 'Main Street': 195, 'Green Lane': 300}
itf_1 = IntersectionTrafficFlow(
    radius = 10,
    custom_directions = custom_1,
    left_hand_traffic = False,
    cmap_name  = 'tab10',
    cmap_edges_name = None,
    nodes_alpha = 0.7,
    edges_alpha = 0.7,
    min_edge_width = 1,
    max_edge_width = 15,
    width_road = 3,
    crossbar = False,
    width_crossbar = 20,
    exit_arrow = True,
    centerline = True,
    roadside = True,
    text_offset = 3,
    direction_text = True,
    font_size_direction = 20,
    sum_movement_text = True,
    font_size_sum_movement = 10,
    individual_movement_text = True,
    font_size_individual_movement = 5
)

directions_1 = list(custom_1.keys())

max_val = 1000
min_val = 0
od_matrix = []
for origin in directions_1:
    for destination in directions_1:
        if origin == destination:
            od_matrix.append((origin, destination, random.randint(min_val, max_val/5)))
        else:
            od_matrix.append((origin, destination, random.randint(min_val, max_val)))

itf_1.plot(axs.flat[0], od_matrix)

# Second Intersection
itf_2 = IntersectionTrafficFlow(
    radius = 10,
    custom_directions = None,
    left_hand_traffic = True,
    cmap_name  = 'black',
    cmap_edges_name = 'viridis',
    nodes_alpha = 1,
    edges_alpha = 0.8,
    min_edge_width = 5,
    max_edge_width = 5,
    width_road = 3,
    crossbar = False,
    width_crossbar = 20,
    exit_arrow = True,
    centerline = False,
    roadside = False,
    text_offset = 3,
    direction_text = True,
    font_size_direction = 20,
    sum_movement_text = True,
    font_size_sum_movement = 10,
    individual_movement_text = False,
    font_size_individual_movement = 5
)

directions_2 = ['N', 'NE', 'E', 'S', 'SW', 'NW']

max_val = 1000
min_val = 0
od_matrix = []
for origin in directions_2:
    for destination in directions_2:
        if origin == destination:
            od_matrix.append((origin, destination, random.randint(min_val, max_val/5)))
        else:
            od_matrix.append((origin, destination, random.randint(min_val, max_val)))

itf_2.plot(axs.flat[1], od_matrix)


# Third Intersection
itf_3 = IntersectionTrafficFlow(
    radius = 10,
    custom_directions = None,
    left_hand_traffic = True,
    cmap_name  = 'Set2',
    cmap_edges_name = None,
    nodes_alpha = 0.7,
    edges_alpha = 0.6,
    min_edge_width = 1,
    max_edge_width = 15,
    width_road = 3,
    crossbar = True,
    width_crossbar = 20,
    exit_arrow = False,
    centerline = False,
    roadside = False,
    text_offset = 3,
    direction_text = True,
    font_size_direction = 20,
    sum_movement_text = False,
    font_size_sum_movement = 10,
    individual_movement_text = False,
    font_size_individual_movement = 5
)

directions_3 = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']

max_val = 1000
min_val = 0
od_matrix = []
for origin in directions_3:
    for destination in directions_3:
        if origin == destination:
            od_matrix.append((origin, destination, random.randint(min_val, max_val/5)))
        else:
            od_matrix.append((origin, destination, random.randint(min_val, max_val)))

itf_3.plot(axs.flat[2], od_matrix)


# Fourth Intersection
custom_4 = {'Sunset Boulevard': 0, 'River Road': 90, 'Orchard Lane': 180, 'Cedar Avenue': 270}
itf_4 = IntersectionTrafficFlow(
    radius = 10,
    custom_directions = custom_4,
    left_hand_traffic = False,
    cmap_name  = 'black',
    cmap_edges_name = 'RdYlGn',
    nodes_alpha = 0.7,
    edges_alpha = 0.7,
    min_edge_width = 1,
    max_edge_width = 10,
    width_road = 3,
    crossbar = False,
    width_crossbar = 20,
    exit_arrow = True,
    centerline = True,
    roadside = True,
    text_offset = 3,
    direction_text = True,
    font_size_direction = 20,
    sum_movement_text = True,
    font_size_sum_movement = 10,
    individual_movement_text = True,
    font_size_individual_movement = 5
)

directions_4 = list(custom_4.keys())

max_val = 100
min_val = -100
od_matrix = []
for origin in directions_4:
    for destination in directions_4:
        if origin == destination:
            od_matrix.append((origin, destination, random.randint(min_val/5, max_val/5)))
        else:
            od_matrix.append((origin, destination, random.randint(min_val, max_val)))

itf_4.plot(axs.flat[3], od_matrix)

# Save plot
script_dir = os.path.dirname(__file__)
output_path = os.path.join(script_dir, 'multi_example.png')
fig.savefig(output_path, dpi=300)
plt.show()