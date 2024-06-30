import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors
from matplotlib.lines import Line2D
import numpy as np
import random
from typing import List, Dict, Tuple
from collections import OrderedDict, defaultdict

class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

class IntersectionTrafficFlow:

    standard_compass_direction_angles: Dict[str, int] = {
            'N': 0,
            'NE': 45,
            'E': 90,
            'SE': 135,
            'S': 180,
            'SW': 225,
            'W': 270,
            'NW': 315
            }

    def __init__(self,
                 radius: float = 10,
                 custom_directions: Dict[str, int] = None,
                 left_hand_traffic: bool = False,
                 cmap_name: str = 'Set2',
                 cmap_edges_name: str = None,
                 nodes_alpha: float = 0.7,
                 edges_alpha: float = 0.7,
                 min_edge_width: float = 1,
                 max_edge_width: float = 15,
                 width_road: float = 3,
                 crossbar: bool = False,
                 width_crossbar: float = 20,
                 exit_arrow: bool = True,
                 centerline: bool = True,
                 roadside: bool = True,
                 text_offset: float = 3,
                 direction_text: bool = True,
                 font_size_direction: int = 20,
                 sum_movement_text: bool = True,
                 font_size_sum_movement: int = 10,
                 individual_movement_text: bool = True,
                 font_size_individual_movement: int = 5):
        """
        Initializes the IntersectionTrafficFlow visualization class.

        Parameters:
        - radius (float): The radius to use for node points on the visualization.
        - custom_directions (Dict[str, int], optional): Custom mapping of directions to angles.
        - left_hand_traffic (bool): Flag to set if traffic flows on the left.
        - cmap_name (str): Name of the Matplotlib colormap for node colors.
        - cmap_edges_name (str, optional): Name of the colormap for edge colors.
        - nodes_alpha (float): Alpha transparency for nodes.
        - edges_alpha (float): Alpha transparency for edges.
        - max_edge_width (float): Maximum width for edges.
        - width_road (float): Width of the road representations in the visualization.
        - crossbar (bool): Whether to draw a crossbar at nodes.
        - width_crossbar (float): Width of the crossbar.
        - exit_arrow (bool): Whether to draw an exit arrow at nodes.
        - centerline (bool): Whether to include a centerline in the visualization.
        - roadside (bool): Whether to draw roadside boundaries.
        - text_offset (float): Offset for direction labels from the nodes.
        - direction_text (bool): Whether to display direction labels.
        - font_size_direction (int): Font size for direction labels.
        - sum_movement_text (bool): Whether to display sum movement text.
        - font_size_sum_movement (int): Font size for sum movement text.
        - individual_movement_text (bool): Whether to display text for individual movements.
        - font_size_individual_movement (int): Font size for individual movement text.
        """
    
        
        self.radius = radius
        self.compass_direction_angles = custom_directions if custom_directions is not None else self.standard_compass_direction_angles
        self._left_hand_traffic = left_hand_traffic
        self.cmap_name = cmap_name
        self.cmap_edges_name = cmap_edges_name
        self.nodes_alpha = nodes_alpha
        self.edges_alpha = edges_alpha
        self.min_edge_width = min_edge_width
        self.max_edge_width = max_edge_width
        self.width_road = width_road
        self.crossbar = crossbar
        self.width_crossbar = width_crossbar
        self.exit_arrow = exit_arrow
        self.centerline = centerline
        self.roadside = roadside
        self.text_offset = text_offset
        self.direction_text = direction_text
        self.font_size_direction = font_size_direction
        self.sum_movement_text = sum_movement_text
        self.font_size_sum_movement = font_size_sum_movement
        self.individual_movement_text = individual_movement_text
        self.font_size_individual_movement = font_size_individual_movement

        # Initialization
        self.cartesian_angles = self.calculate_cartesian_angles()
        self.directions = self.calculate_direction_point()
        self.ordered_directions = self.order_directions()
        self.colors = self.generate_colors()

        # Traffic Settings
        self._left_hand_traffic = left_hand_traffic
        self.driving_side_factor = -1 if left_hand_traffic else 1

    @property
    def left_hand_traffic(self):
        return self._left_hand_traffic

    @left_hand_traffic.setter
    def left_hand_traffic(self, value: bool):
        self._left_hand_traffic = value
        self.driving_side_factor = -1 if value else 1

    def generate_colors(self):
        try:
            cmap = plt.get_cmap(self.cmap_name)
            return {direction: cmap(i / len(self.directions)) for i, direction in enumerate(self.directions)}
        except ValueError:
            if self.cmap_name in mcolors.CSS4_COLORS or self.cmap_name in mcolors.BASE_COLORS:
                return {direction: self.cmap_name for direction in self.directions}
            else:
                raise ValueError(f'{self.cmap_name} not in Matplotlibs cmap or colors')

    def calculate_cartesian_angles(self) -> Dict[str, float]:
        return {direction: (450 - angle) % 360 for direction, angle in self.compass_direction_angles.items()}

    def calculate_direction_point(self):
        angles_rad = np.deg2rad(list(self.calculate_cartesian_angles().values()))
        x_coords = self.radius * np.cos(angles_rad)
        y_coords = self.radius * np.sin(angles_rad)
        return {direction: Point(x, y) for direction, (x, y) in zip(self.compass_direction_angles.keys(), zip(x_coords, y_coords))}
    
    def order_directions(self):
        return [key for key, _ in sorted(self.compass_direction_angles.items(), key=lambda item: item[1])]
    
    # Main Functions

    def plot(
            self,
            ax: plt.Axes,
            od_matrix: List[Tuple[str, str, float]]
            ) -> plt.Axes:
        """
        Plots the traffic flow visualization on a given Axes.

        Parameters:
        - ax (plt.Axes): The matplotlib axes object where the visualization will be drawn.
        - od_matrix (List[Tuple[str, str, float]]): A list of tuples representing the origin, destination, and flow magnitude.

        Returns:
        - plt.Axes: The axes object with the traffic flow visualization plotted.
        """
        
        self.ax = ax

        od_matrix = self.sort_od_matrix(od_matrix)

        unique_directions = self.get_unique_directions(od_matrix)

        self.plot_edges(od_matrix, unique_directions)
        
        self.plot_nodes(od_matrix, unique_directions)

        self.customize_plot()
        return self.ax
    
    # Sub Functions
    
    def plot_edges(self, od_matrix: List[Tuple[str, str, float]], unique_directions: List[str]) -> None:
        edge_width_reduction_factor = self.calculate_edge_width_reduction_factor(od_matrix)
        min_value, max_value = self.calculate_min_max(od_matrix)
        if self.cmap_edges_name is not None:
            self.edge_cmap = plt.get_cmap(self.cmap_edges_name)
        
        for (origin, destination, value) in od_matrix:
            # Get Coordinates and Angle
            origin_point = self.directions[origin]
            destination_point = self.directions[destination]
            origin_angle = self.calculate_angle(origin)
            destination_angle = self.calculate_angle(destination)

            # Calculate Distance for Sequence of Edges along node bar
            circular_distance = self.calculate_circular_distance(unique_directions, origin, destination)+1

            # Calculate Offsets along node bar
            origin_offset = circular_distance/(len(unique_directions)+1) * self.width_road
            destination_offset = circular_distance/(len(unique_directions)+1) * self.width_road
            origin_delta_x = np.cos(origin_angle) * self.driving_side_factor * -origin_offset
            origin_delta_y = np.sin(origin_angle) * self.driving_side_factor * -origin_offset
            destination_delta_x = np.cos(destination_angle) * self.driving_side_factor * destination_offset
            destination_delta_y = np.sin(destination_angle) * self.driving_side_factor * destination_offset
            origin_x = origin_point.x + origin_delta_x
            origin_y = origin_point.y + origin_delta_y
            destination_x = destination_point.x + destination_delta_x
            destination_y = destination_point.y + destination_delta_y

            # Get angle for curved Line
            angleA = self.get_connection_angles(origin)
            angleB = self.get_connection_angles(destination)

            # Linewidth
            linewidth = self.get_linewidth(value, min_value, max_value)

            # Colors
            if self.cmap_edges_name is None:
                color = self.colors[origin]
            else:
                color = self.get_cmap_color(value, min_value, max_value)

            # Edges
            if origin == destination:
                armA = -self.radius*5
                armB = -self.radius*5
                self.ax.annotate('',
                                 xy=(destination_x, destination_y),
                                 xytext=(origin_x, origin_y),
                                 arrowprops=dict(arrowstyle="-", connectionstyle=f"arc,angleA={angleA},angleB={angleB},armA={armA},armB={armB},rad={0}",
                                            color=color, alpha=self.edges_alpha, linewidth=linewidth,
                                            linestyle='-', capstyle='butt'))
            elif (angleB - angleA) % 180 == 0:  # If directly opposite
                self.ax.annotate("",
                                 xy=(destination_x, destination_y),
                                 xytext=(origin_x, origin_y),
                                 arrowprops=dict(arrowstyle="-", color=color, alpha=self.edges_alpha, linewidth=linewidth,
                                            linestyle='-', capstyle='butt'))
            else:  # Curved Line
                self.ax.annotate('',
                                 xy=(destination_x, destination_y),
                                 xytext=(origin_x, origin_y),
                                 arrowprops=dict(arrowstyle="-", connectionstyle=f"angle3,angleA={angleA},angleB={angleB}",
                                            color=color, alpha=self.edges_alpha, linewidth=linewidth,
                                            linestyle='-', capstyle='butt'))
            
            if self.individual_movement_text:
            # Individual Movement
                origin_angle_deg = np.rad2deg(origin_angle)+90
                if origin_angle_deg < 270 and origin_angle_deg > 90: # If on the left hemisphere
                    text_angle_deg = origin_angle_deg - 180
                    ha = 'right'
                    va = 'center'
                else:   # If on the right hemisphere
                    text_angle_deg = origin_angle_deg
                    ha = 'left'
                    va = 'center'
                self.ax.text(x=origin_x, y=origin_y, s=f'{value}', # Small Text with traffic volume
                            fontsize=self.font_size_individual_movement, rotation=text_angle_deg, rotation_mode='anchor',
                            horizontalalignment=ha, verticalalignment=va)
            
    def plot_nodes(self, od_matrix: List[Tuple[str, str, float]], unique_directions: List[str]) -> None:
        origin_sums, destination_sums = self.sum_values_by_origin_and_destination(od_matrix)

        self.roadside_anchors: Dict = {}
        for key in unique_directions:
            # Get Coordinates and Angle
            point = self.directions[key]
            angle = self.calculate_angle(key)
            angle_deg = np.rad2deg(angle)

            # Crossbar
            road_delta_x = np.cos(angle) * self.width_road
            road_delta_y = np.sin(angle) * self.width_road
            if self.crossbar:
                crossbar = Line2D(
                    [point.x - road_delta_x, point.x + road_delta_x],
                    [point.y - road_delta_y, point.y + road_delta_y],
                    color=self.colors[key],
                    linewidth=self.width_crossbar,
                    alpha=self.nodes_alpha,
                    solid_capstyle='butt'
                )
                self.ax.add_line(crossbar)
            
            # Exit Arrow
            if self.exit_arrow:
                arrow_middle_delta_x = road_delta_x/2 + np.cos(angle+np.deg2rad(self.driving_side_factor*90))
                arrow_middle_delta_y = road_delta_y/2 + np.sin(angle+np.deg2rad(self.driving_side_factor*90))
                triangle = patches.Polygon(
                    [
                        [point.x, point.y],
                        [point.x + self.driving_side_factor*road_delta_x, point.y + self.driving_side_factor*road_delta_y],
                        [point.x + self.driving_side_factor*arrow_middle_delta_x, point.y + self.driving_side_factor*arrow_middle_delta_y]
                    ],
                    closed=True,
                    edgecolor=self.colors[key],
                    facecolor=self.colors[key],
                    alpha=self.nodes_alpha
                )
                self.ax.add_patch(triangle)

            # Text of Direction
            if self.direction_text:
                if angle_deg < 270 and angle_deg > 90: # If on the lower hemisphere
                    text_angle_deg = angle_deg - 180
                else:   # If on the upper hemisphere
                    text_angle_deg = angle_deg
                text_x = point.x + np.cos(angle+np.deg2rad(90)) * self.text_offset
                text_y = point.y + np.sin(angle+np.deg2rad(90)) * self.text_offset
                self.ax.text(x=text_x, y=text_y, s=key, color=self.colors[key], rotation=text_angle_deg,
                            fontsize=self.font_size_direction,
                            ha='center', va='center')

            # Centerline
            if self.centerline:
                centerline_delta_x = np.cos(angle+np.deg2rad(90))*2
                centerline_delta_y = np.sin(angle+np.deg2rad(90))*2
                self.ax.plot([point.x - centerline_delta_x, point.x],
                            [point.y - centerline_delta_y, point.y],
                            color='black', linewidth=2, linestyle='--') # Bar
                
            # Roadside collect data
            if self.roadside:
                right_side_anchor = Point(point.x - road_delta_x, point.y - road_delta_y)
                left_side_anchor = Point(point.x + road_delta_x, point.y + road_delta_y)
                connection_angle = self.get_connection_angles(key)
                self.roadside_anchors[key] = {'right': (right_side_anchor, connection_angle), 'left': (left_side_anchor, connection_angle)}

            # Sum of Movment
            if self.sum_movement_text:
                sum_out_text = f'∑ out: {destination_sums[key]}'
                sum_in_text = f'∑ in: {origin_sums[key]}'
                if angle_deg < 270 and angle_deg > 90: # If on the lower hemisphere
                    text_angle_deg = angle_deg - 180
                    if self.left_hand_traffic:
                        sum_text = '  ' + sum_in_text + ' | ' + sum_out_text
                    else:
                        sum_text = sum_out_text + ' | ' + sum_in_text + '  '
                else:   # If on the upper hemisphere
                    text_angle_deg = angle_deg
                    if self.left_hand_traffic:
                        sum_text = sum_out_text + ' | ' + sum_in_text + '  '
                    else:
                        sum_text = '  ' + sum_in_text + ' | ' + sum_out_text
                sum_movment_x = point.x + np.cos(angle+np.deg2rad(90)) * self.text_offset / 2
                sum_movment_y = point.y + np.sin(angle+np.deg2rad(90)) * self.text_offset / 2
                
                self.ax.text(x=sum_movment_x, y=sum_movment_y, s=sum_text, rotation=text_angle_deg,
                            fontsize=self.font_size_sum_movement,
                            horizontalalignment='center', verticalalignment='center')
        
        if self.roadside:
            for i, key in enumerate(unique_directions):
                i_next = (i+1) % len(unique_directions)
                left_side_anchor_point_current = self.roadside_anchors[key]['left'][0]
                right_side_anchor_point_next = self.roadside_anchors[unique_directions[i_next]]['right'][0]
                left_side_anchor_angle_current = self.roadside_anchors[key]['left'][1]
                right_side_anchor_angle_next = self.roadside_anchors[unique_directions[i_next]]['right'][1]
                # Roadside
                if (right_side_anchor_angle_next - left_side_anchor_angle_current) % 180 == 0:  # If directly opposite
                    self.ax.annotate("",
                                    xy=(right_side_anchor_point_next.x, right_side_anchor_point_next.y),
                                    xytext=(left_side_anchor_point_current.x, left_side_anchor_point_current.y),
                                                arrowprops=dict(arrowstyle="-", color='black', alpha=1, linewidth=2,
                                                    linestyle='-', capstyle='butt'))
                else:  # Curved Line
                    self.ax.annotate('',
                                    xy=(right_side_anchor_point_next.x, right_side_anchor_point_next.y),
                                    xytext=(left_side_anchor_point_current.x, left_side_anchor_point_current.y),
                                    arrowprops=dict(arrowstyle="-",
                                                    connectionstyle=f"angle3,angleA={left_side_anchor_angle_current},angleB={right_side_anchor_angle_next}",
                                                    color='black', alpha=1, linewidth=2,
                                                    linestyle='-', capstyle='butt'))
               
    # Helper Functions
    
    def get_unique_directions(self, od_matrix: List[Tuple[str, str, int]]) -> List[str]:
        unique_directions_dict = OrderedDict()
        for origin, destination, _ in od_matrix:
            unique_directions_dict[origin] = None
        for origin, destination, _ in od_matrix:
            unique_directions_dict[destination] = None
        unique_directions = list(unique_directions_dict.keys())
        return unique_directions
    
    def sort_od_matrix(self, od_matrix: List[Tuple[str, str, int]]) -> List[Tuple[str, str, int]]:
        directions = set()
        for origin, destination, _ in od_matrix:
            directions.add(origin)
            directions.add(destination)
        complete_od_matrix = defaultdict(int)
        for origin in directions:
            for destination in directions:
                complete_od_matrix[(origin, destination)] = 0
        for origin, destination, value in od_matrix:
            complete_od_matrix[(origin, destination)] = value
        completed_od_matrix = [(origin, destination, value) for (origin, destination), value in complete_od_matrix.items()]
        direction_index = {direction: index for index, direction in enumerate(self.ordered_directions)}
        return sorted(completed_od_matrix, key=lambda x: (direction_index[x[0]], direction_index[x[1]]))

    def calculate_min_max(self, od_matrix: List[Tuple[str, str, int]]) -> List[Tuple[float, float]]:
        values = [value for _, _, value in od_matrix]
        min_value = min(values)
        max_value = max(values)
        return min_value, max_value

    def calculate_edge_width_reduction_factor(self, od_matrix: List[Tuple[str, str, float]]) -> None:
        max_value = max(value for _, _, value in od_matrix)
        return max_value / self.max_edge_width
    
    def get_linewidth(self, value: float, min_value: float, max_value: float) -> int:
        scale = (self.max_edge_width - self.min_edge_width) / (max_value - min_value)
        return self.min_edge_width + (value - min_value) * scale

        
    def calculate_angle(self, key: str) -> float:
        return np.deg2rad(self.cartesian_angles[key]-90)

    def get_connection_angles(self, key: str) -> int:
        angle = self.cartesian_angles[key]
        return angle

    def calculate_circular_distance(self, directions: List[str], origin: str, destination: str):
        start_index = directions.index(origin)
        end_index = directions.index(destination)
        
        if self.driving_side_factor == 1:  # Clockwise
            if end_index >= start_index:
                distance = end_index - start_index
            else:
                distance = len(directions) - start_index + end_index
        elif self.driving_side_factor == -1:  # Anti Clockwise
            if start_index >= end_index:
                distance = start_index - end_index
            else:
                distance = len(directions) - end_index + start_index
        
        return distance 

    def sum_values_by_origin_and_destination(self, od_matrix: List[Tuple[str, str, int]]) -> Tuple[Dict[str, int], Dict[str, int]]:
        origin_sums = {}
        destination_sums = {}
        
        for origin, destination, value in od_matrix:
            if origin in origin_sums:
                origin_sums[origin] += value
            else:
                origin_sums[origin] = value
            
            if destination in destination_sums:
                destination_sums[destination] += value
            else:
                destination_sums[destination] = value
                
        return origin_sums, destination_sums
    
    # Styling Functions

    def get_cmap_color(self, value: float, min_value: int, max_value: int):
        normalized = (value - min_value) / (max_value - min_value)
        return self.edge_cmap(normalized)

    def customize_plot(self) -> None:
        lim = int(self.radius*1.5)
        self.ax.set_xlim([-lim, lim])
        self.ax.set_ylim([-lim, lim])
        self.ax.grid(True)
        self.ax.axis('off')
        self.ax.set_aspect('equal', adjustable='box')



if __name__ == '__main__':
    custom_directions = {'High Street': 0, 'Kings Road': 240, 'Park Avenue': 60, 'Main Street': 195, 'Green Lane': 300}

    itf = IntersectionTrafficFlow(
        custom_directions=None)
    
    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(12, 15))
    
    '''directions = ['N', 'S', 'W']'''
    '''directions = ['N', 'E', 'S', 'W']'''
    '''directions = ['N', 'NE', 'E', 'S', 'SW', 'NW']'''
    directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    '''directions = list(custom_directions.keys())'''
    for ax in axs.flat:
        max_val = 1000
        min_val = 0
        od_matrix = []
        for origin in directions:
            for destination in directions:
                od_matrix.append((origin, destination, random.randint(min_val, max_val)))

        '''od_matrix = [('N', 'N', 60), ('N', 'E', 696), ('N', 'S', 671), ('N', 'SW', 921), ('N', 'NW', 368),
                     ('NE', 'N', 498), ('NE', 'E', 61), ('NE', 'S', 665), ('NE', 'SW', 425), ('NE', 'NW', 469),
                     ('E', 'N', 606), ('E', 'E', 710), ('E', 'S', 506), ('E', 'SW', 322), ('E', 'NW', 752), 
                     ('S', 'N', 1), ('S', 'E', 128), ('S', 'S', 507), ('S', 'SW', 499), ('S', 'NW', 791), 
                     ('SW', 'N', 907), ('SW', 'E', 722), ('SW', 'S', 101), ('SW', 'SW', 374), ('SW', 'NW', 407), 
                     ('NW', 'N', 64), ('NW', 'E', 133), ('NW', 'S', 612), ('NW', 'SW', 284), ('NW', 'NW', 796)]'''
        
        ax = itf.plot(ax, od_matrix)
    fig.suptitle('Intersection Flow')
    plt.show()
