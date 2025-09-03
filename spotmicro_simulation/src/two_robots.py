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
urdf_path = "/home/neuron/projects/spotmicro_simulation/spotmicroai.urdf"

# Load Robot 1
start_pos1 = [0, 0, 0.3]  # Robot 1 position
start_orientation = p.getQuaternionFromEuler([0, 0, 0])
robot1_id = p.loadURDF(urdf_path, start_pos1, start_orientation, useFixedBase=False)

# Load Robot 2
start_pos2 = [0.5, 0, 0.3]  # Robot 2 position (offset to avoid collision)
robot2_id = p.loadURDF(urdf_path, start_pos2, start_orientation, useFixedBase=False)

# Print joint info for both robots
print("=== Robot 1 ===")
for i in range(p.getNumJoints(robot1_id)):
    joint_info = p.getJointInfo(robot1_id, i)
    print(f"Joint {i}: {joint_info[1].decode()} ({joint_info[2]})")

print("=== Robot 2 ===")
for i in range(p.getNumJoints(robot2_id)):
    joint_info = p.getJointInfo(robot2_id, i)
    print(f"Joint {i}: {joint_info[1].decode()} ({joint_info[2]})")

# Simulate
while True:
    p.stepSimulation()
    time.sleep(1. / 240.)
