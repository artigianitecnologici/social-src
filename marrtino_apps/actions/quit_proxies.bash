#!/bin/bash

# quit all action proxies
rostopic pub pnp/action_str std_msgs/String "data: '%quit_server'" --once

