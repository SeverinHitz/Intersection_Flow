import os
import matplotlib.pyplot as plt
from IntersectionTrafficFlow import IntersectionTrafficFlow

# Initialize the traffic flow visualization
itf = IntersectionTrafficFlow()

# Sample data representing origin, destination, and traffic volume
od_matrix = [
    ('N', 'E', 500),
    ('N', 'SW', 300),
    ('N', 'N', 50),
    ('E', 'N', 500),
    ('E', 'E', 100),
    ('E', 'SW', 400),
    ('SW', 'N', 500),
    ('SW', 'E', 300),
    ('SW', 'SW', 30)
]

# Setup plot
fig, ax = plt.subplots(figsize=(10,10))
plt.tight_layout()
itf.plot(ax, od_matrix)

# Save plot
script_dir = os.path.dirname(__file__)
output_path = os.path.join(script_dir, 'basic_example.png')
fig.savefig(output_path, dpi=300)