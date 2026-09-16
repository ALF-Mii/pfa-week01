import math

import maya.cmds as cmds

WIN = "SimpleStairWindow"  # Name of the tool window.
STEP_WIDTH = 100.0  # How wide each step is.
STEP_DEPTH = 30.0  # How deep each step is.
STEP_HEIGHT = 4.0  # How thick each step is.


def build_straight(steps, height):
    """Build a straight staircase going up the X axis."""
    rise = height / steps  # Height gained per step.
    for i in range(steps):
        step = cmds.polyCube(w=STEP_WIDTH, h=STEP_HEIGHT, d=STEP_DEPTH)[0]  # Create one step.
        cmds.move(i * STEP_DEPTH, i * rise, 0, step)  # Move it up and forward.


def build_spiral(steps, height):
    """Build a circular staircase around the origin."""
    rise = height / steps  # Height gained per step.
    radius = 60.0  # Distance of the steps from the center.
    for i in range(steps):
        angle = 360.0 * i / steps  # Angle of this step in degrees.
        rad = math.radians(angle)  # Same angle in radians for math functions.
        step = cmds.polyCube(w=STEP_DEPTH, h=STEP_HEIGHT, d=STEP_WIDTH)[0]  # Create one step.
        cmds.move(radius * math.cos(rad), i * rise, radius * math.sin(rad), step)  # Place on the circle.
        cmds.rotate(0, -angle, 0, step)  # Turn the step to follow the circle.


def build(*_):
    """Read the UI and build the chosen staircase."""
    steps = int(cmds.intSliderGrp("steps", query=True, value=True))  # Number of steps.
    height = cmds.floatSliderGrp("height", query=True, value=True)  # Total height.
    kind = cmds.optionMenu("kind", query=True, value=True)  # Chosen stair type.
    if kind == "Straight":
        build_straight(steps, height)
    else:
        build_spiral(steps, height)


def clear(*_):
    """Delete previously generated steps."""
    for obj in cmds.ls("step*"):
        cmds.delete(obj)


def build_ui():
    """Create the tool window."""
    if cmds.window(WIN, exists=True):
        cmds.deleteUI(WIN)  # Close an old window first.
    cmds.window(WIN, title="Stair Generator", widthHeight=(300, 260))  # Make the window.
    cmds.columnLayout(adjustableColumn=True, rowSpacing=8)  # Stack controls vertically.

    cmds.optionMenu("kind", label="Stair type")  # Dropdown for stair type.
    cmds.menuItem(label="Straight")  # First option.
    cmds.menuItem(label="Circular")  # Second option.

    cmds.intSliderGrp("steps", label="Number of steps",
                      minValue=1, maxValue=50, value=10, field=True)  # Steps slider.
    cmds.floatSliderGrp("height", label="Total height",
                        minValue=10, maxValue=1000, value=250, field=True)  # Height slider.

    cmds.button(label="Build Stairs", command=build)  # Build button.
    cmds.button(label="Clear", command=clear)  # Clear button.

    cmds.showWindow(WIN)  # Show the window.


if __name__ == "__main__":
    build_ui()
