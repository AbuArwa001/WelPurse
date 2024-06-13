import matplotlib.pyplot as plt
import numpy as np

# Define the figure and axis
fig, ax = plt.subplots(figsize=(6, 6))

# Define colors
primary_color = "#d0b997"
secondary_color = "#2a5b87"
accent_color = "#ab0000"

# Draw a circle for the background
circle = plt.Circle(
    (0.5, 0.5), 0.4, color=primary_color, ec=secondary_color, lw=5
)
ax.add_patch(circle)

# Draw a smaller circle for accent
inner_circle = plt.Circle(
    (0.5, 0.5), 0.3, color=secondary_color, ec=accent_color, lw=3
)
ax.add_patch(inner_circle)

# Draw semi-circles to represent hands
left_hand = plt.Circle(
    (0.3, 0.7), 0.15, color=accent_color, ec=accent_color, lw=3, alpha=0.5
)
right_hand = plt.Circle(
    (0.7, 0.7), 0.15, color=accent_color, ec=accent_color, lw=3, alpha=0.5
)
ax.add_patch(left_hand)
ax.add_patch(right_hand)

# Add text
ax.text(
    0.5,
    0.5,
    "WelPurse",
    horizontalalignment="center",
    verticalalignment="center",
    fontsize=30,
    color="white",
    fontweight="bold",
)

# Remove axes
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

# Save the logo
plt.savefig("WelPurse_logo.png", dpi=300, bbox_inches="tight")

# Show the logo
plt.show()
