cmake_minimum_required(VERSION 2.8.3)
project(servo_drive)


find_package(catkin REQUIRED COMPONENTS
  duckietown_msgs
  geometry_msgs
  sensor_msgs
  rospy
  std_msgs
)


catkin_package()

include_directories(
  ${catkin_INCLUDE_DIRS}
)

catkin_install_python(PROGRAMS
   open_loop.py
   DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
