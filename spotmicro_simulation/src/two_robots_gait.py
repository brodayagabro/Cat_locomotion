import pybullet as p
import pybullet_data
import time
import math
import os

def setup_simulation():
    p.connect(p.GUI)
    p.setGravity(0, 0, -9.81)
    p.setRealTimeSimulation(0)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.loadURDF("plane.urdf")

def load_spotmicro(urdf_path, position):
    orientation = p.getQuaternionFromEuler([0, 0, 0])
    robot_id = p.loadURDF(urdf_path, position, orientation, useFixedBase=False)
    return robot_id

def get_leg_joints(robot_id):
    movable_joints = [j for j in range(p.getNumJoints(robot_id)) if p.getJointInfo(robot_id, j)[2] != p.JOINT_FIXED]
    legs = [movable_joints[i:i+3] for i in range(0, len(movable_joints), 3)]
    return legs  # FL, FR, RL, RR order assumed

def apply_gait(robot_id, leg_joints, t, phase_offset=0.0):
    # Simple trot gait: swing hips & knees in/out of phase
    cycle_period = 1.0
    phase = 2 * math.pi * ((t % cycle_period) / cycle_period) + phase_offset
    hip_amp = 0.2
    knee_offset = 0.6
    knee_amp = 0.4

    for i, leg in enumerate(leg_joints):
        if len(leg) < 2:
            continue
        hip, mid, knee = leg
        leg_phase = phase + (math.pi if i % 2 == 0 else 0)  # alternate legs
        hip_target = hip_amp * math.cos(leg_phase)
        knee_target = knee_offset + knee_amp * math.cos(leg_phase)
        p.setJointMotorControl2(robot_id, hip, p.POSITION_CONTROL, hip_target, force=50)
        p.setJointMotorControl2(robot_id, knee, p.POSITION_CONTROL, knee_target, force=50)
        p.setJointMotorControl2(robot_id, mid, p.POSITION_CONTROL, 0.0, force=50)

# Main simulation
if __name__ == "__main__":
    setup_simulation()

    urdf_path = "/home/neuron/projects/spotmicro_simulation/spotmicroai.urdf"

    # Load two robots
    robot1_id = load_spotmicro(urdf_path, [0, -0.3, 0.3])
    robot2_id = load_spotmicro(urdf_path, [0.6, 0.3, 0.3])

    # Get joints
    robot1_legs = get_leg_joints(robot1_id)
    robot2_legs = get_leg_joints(robot2_id)

    t = 0
    dt = 1.0 / 240.0
    while True:
        apply_gait(robot1_id, robot1_legs, t, phase_offset=0.0)
        apply_gait(robot2_id, robot2_legs, t, phase_offset=math.pi)  # mirror phase
        p.stepSimulation()
        time.sleep(dt)
        t += dt
