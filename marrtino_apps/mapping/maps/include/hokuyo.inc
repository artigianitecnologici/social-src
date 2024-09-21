define utm30 ranger
(
  sensor(
    range [ 0.0  20.0 ]
    fov 270.25
    samples 1081
  )

  # model properties
  color "orange"
  size [ 0.15 0.15 0.10 ]

  block( points 4
	point[0] [0 0]
	point[1] [0 1]
	point[2] [1 1]
	point[3] [1 0]
	z [0 1]
  )

)


define urg04 ranger
(
  sensor(
    range [ 0.0  4.0 ]
    fov 270.25
    samples 1081
  )

  # model properties
  color "blue"
  size [ 0.15 0.15 0.10 ]

  block( points 4
	point[0] [0 0]
	point[1] [0 1]
	point[2] [1 1]
	point[3] [1 0]
	z [0 1]
  )

)


define fakelaser ranger
(
  sensor(
    range [ 0.0  0.1 ]
    fov 60
    samples 10
  )

  # model properties
  color "brown"
  size [ 0.4 0.15 0.5 ]

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

)
