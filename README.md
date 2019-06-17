# Physics_Final-Project

For our final project, we have created a gravitational simulation that involves planetary motion (orbits) and conservation of momentum (fuel usage) using Processing. The gist of the game will be to begin on a planet with a customizable amount of fuel, and attempt to land safely on a predetermined target planet. 

While in space, the user can apply thrust to the 4 planar direction using the usual WASD keys to eject fuel: losing mass and gaining velocity at dictated by the conservation of momentum.

Things that were missed in the video:
    1) The fuel ejected is represented by small yellow circles that disappear upon touching the player or planet
    2) The player velocity is oriented the same way as the java coordinate system (4th quadrant): up is negative
    3) Player mass will not fully disappear. The fuel represents only a portion of the player's total mass and upon depletion, the player can no       apply input, meaning the ship would be allowed to "free-fall" into the gravitational sinks.

