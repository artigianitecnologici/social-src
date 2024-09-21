define front model
(
  size [0.1 0.1 0.1]

  block(
       points 4
       point[0] [-0.1 0.1]
       point[1] [-0.1 -0.1]
       point[2] [0.1 -0.1]
       point[3] [0.1 0.1]
       z [0 1]
  )
  
  color "black"
)


define body model
(
  size [0.25 0.5 0.5]

  block(
       points 8
       point[0] [-0.2 0.12]
       point[1] [-0.2 -0.12]
       point[2] [-0.12 -0.2555]
       point[3] [0.12 -0.2555]
       point[4] [0.2 -0.12]
       point[5] [0.2 0.12]
       point[6] [0.12 0.2555]
       point[7] [-0.12 0.2555]
       z [0 1]
  )
  
  color "gray"
)

# must be a ranger because number of positions and number of lasers must be equal!!!

define head ranger (

  size [0.2 0.2 0.2]

  sensor(
    range [ 0.0  0.1 ]
    fov 30
    samples 10
  )

  block(
       points 8
       point[0] [-0.2 0.12]
       point[1] [-0.2 -0.12]
       point[2] [-0.12 -0.2555]
       point[3] [0.12 -0.2555]
       point[4] [0.2 -0.12]
       point[5] [0.2 0.12]
       point[6] [0.12 0.2555]
       point[7] [-0.12 0.2555]
       z [0 1]
  )
  
  color "brown"
  gui_nose 1

)

define person position
(
  size [0.20 0.40 0.6]
  origin [0 0 0 0]
  gui_nose 1
  drive "diff"    
  bitmap "include/legs.bmp"
  color "pink"

  # set in person object to choose a different color (does not work as default)
  #body(pose [ 0 0 0 0 ] color "grey")

  front(pose [0.11 0 0.25 0] size [0.1 0.2 0.2] color "black")

  head(pose [ 0 0 0.5 0 ])
  front(pose [0.07 0 0.55 0] size [0.1 0.1 0.1] color "pink")

  cam16(pose [ 0.0 0 0 0 ])
)

