import pybullet as p
import pybullet_data
import time
import os

# Start PyBullet with GUI
physicsClient = p.connect(p.GUI)
p.setGravity(0, 0, -9.81)
p.setRealTimeSimulation(0)

# Optionally add default search path for plane.urdf
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# Load ground plane
p.loadURDF("plane.urdf")

# Path to your URDF
urdf_path = "../spotmicroai_fixed.urdf"

# Load SpotMicro
start_pos = [0, 0, 0.3]  # Elevate slightly above ground
start_orientation = p.getQuaternionFromEuler([0, 0, 0])
robot_id = p.loadURDF(urdf_path, start_pos, start_orientation, useFixedBase=False)

# Print joint info
num_joints = p.getNumJoints(robot_id)
for i in range(num_joints):
    joint_info = p.getJointInfo(robot_id, i)
    print(f"Joint {i}: {joint_info[1].decode()} ({joint_info[2]})")

# Simulate
while True:
    p.stepSimulation()
    time.sleep(1. / 240.)
