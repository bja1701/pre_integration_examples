class TimeSync:
    def __init__(self) -> None:

        self.msg_queue = []         # append message of specific sensor to queue
        self.last_pose_key = None

    def add_to_queue(self, msg):
        self.msg_queue.append(msg)

    def get_factor_info(self, init_new_id, poseKey_to_time):
        ''''
        new_id = int, The agent posekey id that you will start searching at
        poseKey_to_time = dict being tracked by factor graph. keys: poseKey values: corresponding timestamp
        '''

        # A flag to determine if all remaining measurements are in the future relative to the current pose key's time
        in_future = False

        new_id = init_new_id
        curr_time = poseKey_to_time[new_id] 
        poseKey_to_add = None
        msg_to_add = None

        # If measurement in queue and the oldest measurment is later than current posekey
        # Process the oldest measurements in self.msg_queue to decide if they are relevant for the current new_id
        while(len(self.msg_queue) > 1 and in_future is False):       

            oldest_measurement_time = (self.msg_queue[0].header.stamp.sec * 1_000_000_000 + self.msg_queue[0].header.stamp.nanosec) 
            next_measurement_time = (self.msg_queue[1].header.stamp.sec * 1_000_000_000 + self.msg_queue[1].header.stamp.nanosec) 
            # print("Curr", curr_time, "Oldest", oldest_measurement_time, "Next", next_measurement_time)

            if(oldest_measurement_time < curr_time):
                # print('oldest measurement time < curr time')
                
                newer_key_time = poseKey_to_time[int(new_id)] 
                # print("newer key time: %d\n"%newer_key_time)
                print("Timesync new id:", int(new_id - 1))
                older_key_time = poseKey_to_time[int(new_id - 1)]
                # print("older key time: %d\n"% older_key_time)
                time_to_current = abs(newer_key_time - oldest_measurement_time) 
                # print("time to current: %d\n"%time_to_current)
                time_to_previous = abs(older_key_time - oldest_measurement_time) 
                # print("time to previous: %d\n"%time_to_previous)

                if(time_to_current > time_to_previous):
                    # Meas in queue better suited to previous key, keep working on prev key
                    print('time to current is longer than time to prev')
                    print('new', new_id, ' prev', self.last_pose_key, ' init', init_new_id)
                    new_id -= 1
                    if(new_id == self.last_pose_key):
                        print('pop')
                        self.msg_queue.pop(0)
                        new_id = init_new_id
                else:
                    # print('time to current is shortest')

                    time_old_to_pose = abs(oldest_measurement_time - newer_key_time)
                    time_next_to_pose = abs(next_measurement_time - newer_key_time)

                    if(next_measurement_time < newer_key_time):
                    # Take care of where next measurement is not past next node
                        self.msg_queue.pop(0)
                    
                    elif(time_old_to_pose > time_next_to_pose):
                    # Take care of case where next measurement is better
                        self.msg_queue.pop(0)
                        new_id = init_new_id

                    else:
                        # Actually add the factor
                        poseKey_to_add = new_id
                        msg_to_add = self.msg_queue.pop(0)                    
                        self.last_pose_key = new_id
            else:
                in_future = True

        return poseKey_to_add, msg_to_add