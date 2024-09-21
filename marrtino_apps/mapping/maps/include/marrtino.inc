include "include/hokuyo.inc"
include "include/camera.inc"
include "include/lights.inc"

# needed to communicate to clients that this position model is a robot
define robottype model (
  name "robot"
  size [ 0.01 0.01 0.01 ]
  pose [ 0 0 -0.1 0 ]
  color "white"
)

define marrtino position
(
  size [0.30 0.30 0.50]
  
  # This block approximates a circular shape of a Robot
  block( points 16
        point[0] [ 0.225 0.000 ]
        point[1] [ 0.208 0.086 ]
        point[2] [ 0.159 0.159 ]
        point[3] [ 0.086 0.208 ]
        point[4] [ 0.000 0.225 ]
        point[5] [ -0.086 0.208 ]
        point[6] [ -0.159 0.159 ]
        point[7] [ -0.208 0.086 ]
        point[8] [ -0.225 0.000 ]
        point[9] [ -0.208 -0.086 ]
        point[10] [ -0.159 -0.159 ]
        point[11] [ -0.086 -0.208 ]
        point[12] [ -0.000 -0.225 ]
        point[13] [ 0.086 -0.208 ]
        point[14] [ 0.159 -0.159 ]
        point[15] [ 0.208 -0.086 ]
        z [0 1]
  )
    
  origin [-0.050 0 0 0]
  gui_nose 1
  drive "diff"
  localization "odom"
  odom_error [ 0.01 0.01 0.0 0.1 ]
  utm30(pose [ 0.050 0 -0.4 0 ])
  cam160(pose [ 0.02 0 0 0 ])
  robottype()

)

