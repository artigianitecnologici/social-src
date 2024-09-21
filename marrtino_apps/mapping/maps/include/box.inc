include "include/lights.inc"

define box model
(
  size [0.400 0.400 0.5]
  gui_nose 0
)

define tag circle
(
  size [0.1 0.1 0.01]
  gui_nose 0
  obstacle_return 0
  ranger_return 0
)


define boxcircle circle
(
  size [0.1 0.1 0.01]
  gui_nose 0
  obstacle_return 1
  ranger_return 1
)



define door model
(
  size [1.000 0.200 1.00]
  gui_nose 0
)

define circle model
(
  size [0.600 0.300 0.80]
  
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
       z [0 1.0]
  )
  
  obstacle_return 1
  ranger_return 1
  gui_outline 1
  gui_nose 0
)

define circle16 model
(
  size [0.600 0.300 0.80]
  
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

  gui_nose 0
)

define lightbox model
(
  size [0.400 0.400 0.5]
  light()
  gui_nose 0
)



define tag0 model
(
  size [0.1 0.1 0.1]
  bitmap "include/0.bmp"
  color "red"
  obstacle_return 0
  ranger_return 0
)


define tag1 model
(
  size [0.1 0.1 0.1]
  bitmap "include/1.bmp"
  color "red"
  obstacle_return 0
  ranger_return 0
)


define tag2 model
(
  size [0.1 0.1 0.1]
  bitmap "include/2.bmp"
  color "red"
  obstacle_return 0
  ranger_return 0
)

define tag3 model
(
  size [0.1 0.1 0.1]
  bitmap "include/3.bmp"
  color "red"
  obstacle_return 0
  ranger_return 0
)

define tag4 model
(
  size [0.1 0.1 0.1]
  bitmap "include/4.bmp"
  color "red"
  obstacle_return 0
  ranger_return 0
)

define tag5 model
(
  size [0.1 0.1 0.1]
  bitmap "include/5.bmp"
  color "red"
  obstacle_return 0
  ranger_return 0
)

define tag6 model
(
  size [0.1 0.1 0.1]
  bitmap "include/6.bmp"
  color "red"
  obstacle_return 0
  ranger_return 0
)

define tag7 model
(
  size [0.1 0.1 0.1]
  bitmap "include/7.bmp"
  color "red"
  obstacle_return 0
  ranger_return 0
)

define tag8 model
(
  size [0.1 0.1 0.1]
  bitmap "include/8.bmp"
  color "red"
  obstacle_return 0
  ranger_return 0
)

define tag9 model
(
  size [0.1 0.1 0.1]
  bitmap "include/9.bmp"
  color "red"
  obstacle_return 0
  ranger_return 0
)

define tag10 model
(
  size [0.1 0.1 0.1]
  bitmap "include/10.bmp"
  color "red"
  obstacle_return 0
  ranger_return 0
)

define tagline1 model
(
  size [1.0 0.1 0.1]
  bitmap "include/line1.bmp"
  color "red"
  obstacle_return 0
  ranger_return 0
)


define tagN model
(
  size [0.1 0.1 0.1]
  bitmap "include/N.bmp"
  color "red"
  obstacle_return 0
  ranger_return 0
)

define tagS model
(
  size [0.1 0.1 0.1]
  bitmap "include/S.bmp"
  color "red"
  obstacle_return 0
  ranger_return 0
)

define tagE model
(
  size [0.1 0.1 0.1]
  bitmap "include/E.bmp"
  color "red"
  obstacle_return 0
  ranger_return 0
)

define tagO model
(
  size [0.1 0.1 0.1]
  bitmap "include/O.bmp"
  color "red"
  obstacle_return 0
  ranger_return 0
)


define tagdi model
(
  size [0.1 0.1 0.1]
  bitmap "include/di.bmp"
  color "red"
  obstacle_return 0
  ranger_return 0
)


define tagil model
(
  size [0.1 0.1 0.1]
  bitmap "include/il.bmp"
  color "red"
  obstacle_return 0
  ranger_return 0
)

define tagla model
(
  size [0.1 0.1 0.1]
  bitmap "include/la.bmp"
  color "red"
  obstacle_return 0
  ranger_return 0
)

define tagdel model
(
  size [0.1 0.1 0.1]
  bitmap "include/del.bmp"
  color "red"
  obstacle_return 0
  ranger_return 0
)

define tagdella model
(
  size [0.1 0.1 0.1]
  bitmap "include/della.bmp"
  color "red"
  obstacle_return 0
  ranger_return 0
)

define tagapple model
(
  size [0.1 0.1 0.1]
  bitmap "include/apple.bmp"
  color "red"
  obstacle_return 0
  ranger_return 0
)

define tagmela model
(
  size [0.1 0.1 0.1]
  bitmap "include/mela.bmp"
  color "red"
  obstacle_return 0
  ranger_return 0
)

define tagdog model
(
  size [0.1 0.1 0.1]
  bitmap "include/dog.bmp"
  color "red"
  obstacle_return 0
  ranger_return 0
)

define tagcane model
(
  size [0.1 0.1 0.1]
  bitmap "include/cane.bmp"
  color "red"
  obstacle_return 0
  ranger_return 0
)

define tagcat model
(
  size [0.1 0.1 0.1]
  bitmap "include/cat.bmp"
  color "red"
  obstacle_return 0
  ranger_return 0
)

define taggatto model
(
  size [0.1 0.1 0.1]
  bitmap "include/gatto.bmp"
  color "red"
  obstacle_return 0
  ranger_return 0
)


define tagI model
(
  size [0.1 0.1 0.1]
  bitmap "include/I.bmp"
  color "blue"
  obstacle_return 0
  ranger_return 0
)

define taggo model
(
  size [0.1 0.1 0.1]
  bitmap "include/go.bmp"
  color "red"
  obstacle_return 0
  ranger_return 0
)

define tagto model
(
  size [0.1 0.1 0.1]
  bitmap "include/to.bmp"
  color "red"
  obstacle_return 0
  ranger_return 0
)

define tagschool model
(
  size [0.1 0.1 0.1]
  bitmap "include/school.bmp"
  color "red"
  obstacle_return 0
  ranger_return 0
)

define tagstar model
(
  size [0.1 0.1 0.1]
  bitmap "include/star.bmp"
  color "red"
  obstacle_return 0
  ranger_return 0
)

define tagcandy model
(
  size [0.1 0.1 0.1]
  bitmap "include/candy.bmp"
  color "red"
  obstacle_return 0
  ranger_return 0
)

define tagheart model
(
  size [0.1 0.1 0.1]
  bitmap "include/heart.bmp"
  color "red"
  obstacle_return 0
  ranger_return 0
)

define tagicecream model
(
  size [0.1 0.1 0.1]
  bitmap "include/icecream.bmp"
  color "red"
  obstacle_return 0
  ranger_return 0
)


