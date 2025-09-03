import pybullet as p
import pybullet_data
import time, math, csv, argparse

def main():
    # Parse command-line arguments for logging
    parser = argparse.ArgumentParser(description="SpotMicroAI PyBullet Walking Simulation")
    parser.add_argument("--log", action="store_true", help="Enable logging of base pose and joint angles to CSV")
    parser.add_argument("--logfile", default="spotmicro_log.csv", help="CSV file path for logging data")
    args = parser.parse_args()
    
    logging_enabled = args.log
    log_filename = args.logfile

    # Connect to PyBullet (GUI mode) and initialize environment
    p.connect(p.GUI)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())  # for plane.urdf
    p.setGravity(0, 0, -9.81)
    p.loadURDF("plane.urdf")  # ground plane
    
    # Load SpotMicroAI robot URDF
    robot_id = p.loadURDF("spotmicroai.urdf", basePosition=[0, 0, 0.2])
    
    # Get all movable joint indices (exclude fixed joints)
    joint_indices = []
    for j in range(p.getNumJoints(robot_id)):
        joint_info = p.getJointInfo(robot_id, j)
        joint_type = joint_info[2]
        if joint_type != p.JOINT_FIXED:
            joint_indices.append(j)
    
    # Optionally, set initial joint positions (if needed, e.g., a slight knee bend to start)
    # Here we initialize all joints to 0. Adjust if a different default posture is desired.
    for j in joint_indices:
        p.resetJointState(robot_id, j, targetValue=0.0)
    
    # Prepare CSV logging if enabled
    if logging_enabled:
        log_file = open(log_filename, 'w', newline='')
        csv_writer = csv.writer(log_file)
        # Write header: time, base_x, base_y, base_z, base_qx, base_qy, base_qz, base_qw, plus joint angles
        header = ["time", "base_x", "base_y", "base_z", "base_qx", "base_qy", "base_qz", "base_qw"]
        header += [f"joint{j}_angle" for j in joint_indices]
        csv_writer.writerow(header)
    else:
        log_file = None
        csv_writer = None

    # Gait parameters
    cycle_period = 1.0        # seconds per full gait cycle
    hip_amp      = 0.2        # hip swing amplitude (radians)
    knee_offset  = 0.6        # base knee angle (radians)
    knee_amp     = 0.4        # knee bending amplitude (radians)
    phase_offset_A = math.pi  # phase offset for Group A (FL & RR)
    phase_offset_B = 0.0      # phase offset for Group B (FR & RL)
    
    # Determine joint groupings for legs (assuming 4 legs with equal joint count)
    num_legs = 4
    leg_joint_count = len(joint_indices) // num_legs if num_legs else 0
    # Default grouping (may need adjustment if URDF ordering is different)
    if leg_joint_count * num_legs == len(joint_indices):
        # Split joint_indices into 4 groups
        legs = [joint_indices[i*leg_joint_count:(i+1)*leg_joint_count] for i in range(num_legs)]
    else:
        # Fallback: if unexpected joint count, treat each 3 consecutive joints as a leg (common for quadrupeds)
        legs = [joint_indices[i:i+3] for i in range(0, len(joint_indices), 3)]
    # Assign leg groups (assuming order: FL, FR, RL, RR)
    if len(legs) >= 4:
        FL_joints, FR_joints, RL_joints, RR_joints = legs[0], legs[1], legs[2], legs[3]
    else:
        # In case grouping failed, assign sequentially (this is a fallback and may not match actual leg mapping)
        FL_joints = FR_joints = RL_joints = RR_joints = joint_indices

    # Simulation timing setup
    p.setRealTimeSimulation(0)           # use manual stepping
    time_step = 1.0/240.0               # simulation time step (240 Hz)
    p.setTimeStep(time_step)
    simulation_duration = 5.0           # (seconds) how long to run the simulation (set None or remove for infinite)
    steps = int(simulation_duration / time_step) if simulation_duration else float('inf')
    
    try:
        start_wall_time = time.time()
        for step in range(steps):
            # Compute current simulation time (in seconds)
            t = step * time_step
            # Compute normalized phase [0, 2π) for this time in the gait cycle
            phase = 2 * math.pi * ((t % cycle_period) / cycle_period)
            # Compute phase for each group
            phase_A = phase + phase_offset_A
            phase_B = phase + phase_offset_B

            # Compute target angles for each leg's hip and knee joints
            # Front-Left (FL) - Group A
            if FL_joints:
                # Assuming [hip, maybe shoulder, knee] order
                hip_index_FL = FL_joints[0]
                knee_index_FL = FL_joints[-1]  # last joint in group as knee
                hip_target_FL  = hip_amp * math.cos(phase_A)
                knee_target_FL = knee_offset + knee_amp * math.cos(phase_A)
                p.setJointMotorControl2(robot_id, hip_index_FL,  p.POSITION_CONTROL, hip_target_FL, force=50)
                p.setJointMotorControl2(robot_id, knee_index_FL, p.POSITION_CONTROL, knee_target_FL, force=50)
                # (Optional) set middle joint (if exists, e.g., shoulder) to a fixed offset for stability
                if len(FL_joints) == 3:
                    mid_index_FL = FL_joints[1]
                    p.setJointMotorControl2(robot_id, mid_index_FL, p.POSITION_CONTROL, 0.0, force=50)
            
            # Front-Right (FR) - Group B
            if FR_joints:
                hip_index_FR = FR_joints[0]
                knee_index_FR = FR_joints[-1]
                hip_target_FR  = hip_amp * math.cos(phase_B)
                knee_target_FR = knee_offset + knee_amp * math.cos(phase_B)
                p.setJointMotorControl2(robot_id, hip_index_FR,  p.POSITION_CONTROL, hip_target_FR, force=50)
                p.setJointMotorControl2(robot_id, knee_index_FR, p.POSITION_CONTROL, knee_target_FR, force=50)
                if len(FR_joints) == 3:
                    mid_index_FR = FR_joints[1]
                    p.setJointMotorControl2(robot_id, mid_index_FR, p.POSITION_CONTROL, 0.0, force=50)
            
            # Rear-Left (RL) - Group B
            if RL_joints:
                hip_index_RL = RL_joints[0]
                knee_index_RL = RL_joints[-1]
                hip_target_RL  = hip_amp * math.cos(phase_B)
                knee_target_RL = knee_offset + knee_amp * math.cos(phase_B)
                p.setJointMotorControl2(robot_id, hip_index_RL,  p.POSITION_CONTROL, hip_target_RL, force=50)
                p.setJointMotorControl2(robot_id, knee_index_RL, p.POSITION_CONTROL, knee_target_RL, force=50)
                if len(RL_joints) == 3:
                    mid_index_RL = RL_joints[1]
                    p.setJointMotorControl2(robot_id, mid_index_RL, p.POSITION_CONTROL, 0.0, force=50)
            
            # Rear-Right (RR) - Group A
            if RR_joints:
                hip_index_RR = RR_joints[0]
                knee_index_RR = RR_joints[-1]
                hip_target_RR  = hip_amp * math.cos(phase_A)
                knee_target_RR = knee_offset + knee_amp * math.cos(phase_A)
                p.setJointMotorControl2(robot_id, hip_index_RR,  p.POSITION_CONTROL, hip_target_RR, force=50)
                p.setJointMotorControl2(robot_id, knee_index_RR, p.POSITION_CONTROL, knee_target_RR, force=50)
                if len(RR_joints) == 3:
                    mid_index_RR = RR_joints[1]
                    p.setJointMotorControl2(robot_id, mid_index_RR, p.POSITION_CONTROL, 0.0, force=50)
            
            # Step the simulation
            p.stepSimulation()
            
            # Logging data if enabled
            if logging_enabled:
                # Get base position and orientation (orientation as quaternion)
                base_pos, base_orn = p.getBasePositionAndOrientation(robot_id)
                # Get joint angles for all joints in joint_indices (returns tuple of state for each joint)
                joint_states = p.getJointStates(robot_id, joint_indices)
                joint_angles = [state[0] for state in joint_states]  # state[0] is the joint position
                # Prepare log row: time, base_pos (3), base_orn (4), joint angles
                log_time = t
                row = [log_time, base_pos[0], base_pos[1], base_pos[2],
                       base_orn[0], base_orn[1], base_orn[2], base_orn[3]]
                row += joint_angles
                csv_writer.writerow(row)
            
            # (Optional) slow down the loop to real time speed:
            # time.sleep(time_step)  # Uncomment to run in approximately real-time
        # End of for-loop
    except KeyboardInterrupt:
        # Allow graceful exit on user interruption (Ctrl+C)
        print("Simulation interrupted by user.")
    finally:
        # Cleanup: close log file and disconnect from PyBullet
        if log_file:
            log_file.close()
        p.disconnect()

if __name__ == "__main__":
    main()
