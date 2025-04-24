class TimeSync:
    def __init__(self) -> None:

        self.msg_queue = []         # append message of specific sensor to queue
        self.last_pose_key = None
        self.debug_mode = False

    def add_to_queue(self, msg):
        self.msg_queue.append(msg)

    def debug_print(self, thing_to_print):
        if self.debug_mode:
            print(thing_to_print)
        else:
            pass

    def get_factor_info(self, init_new_id, key_to_time, initialNode):
        ''''
        new_id = int, The agent posekey id that you will start searching at
        key_to_time = dict being tracked by factor graph. keys: poseKey values: corresponding timestamp

        '''

        # self.last_pose_key = initialNode

        # A flag to determine if all remaining measurements are in the future relative to the current pose key's time
        in_future = False
        new_id = init_new_id
        curr_time = key_to_time[new_id] 
        poseKey_to_add = None
        msg_to_add = None
        time_stamp = None

        # If measurement in queue and the oldest measurment is later than current posekey
        # Process the oldest measurements in self.msg_queue to decide if they are relevant for the current new_id
        while(len(self.msg_queue) > 1 and in_future is False):       

            oldest_measurement_time = self.msg_queue[0][1]
            next_measurement_time = self.msg_queue[1][1] 
            self.debug_print(f"\n\nBEGINNING another loop:\nTime of the node input to function: {curr_time}\nOldest: {oldest_measurement_time}\nNext: {next_measurement_time}\nTEST REUSLTS BELOW")

            self.debug_print(f"Checking if oldest is less than time of node")
            if(oldest_measurement_time < curr_time):
                self.debug_print('oldest measurement time is not in the future')
                newer_key_time = key_to_time[new_id] 
                self.debug_print(f"Time of new node: {newer_key_time}")
                older_key_time = key_to_time[new_id - 1]
                self.debug_print(f"Time of node right before new node: {older_key_time}")
                time_to_current = abs(newer_key_time - oldest_measurement_time) 
                # self.debug_print("time to current: %d\n"%time_to_current)
                time_to_previous = abs(older_key_time - oldest_measurement_time) 
                # self.debug_print("time to previous: %d\n"%time_to_previous)

                self.debug_print('Checking to see if oldest measurement time is closer to the newer node or the one previous (it is between two nodes, which one is it cloer to?)')
                if(time_to_current > time_to_previous):
                    # Meas in queue better suited to previous key, keep working on prev key
                    self.debug_print('The oldest measurement time actually is better suited to the older one, decrement the new_id')
                    # self.debug_print('new', new_id, ' prev', self.last_pose_key, ' init', init_new_id)
                    new_id -= 1


                    self.debug_print('Checking to see if this node has already had a unary factor added to it')
                    if(new_id == self.last_pose_key ):
                        self.debug_print('Looks like this node was the last node to have a unary factor added to it,\npop the measurement, and set the new_id back to the initial node we were trying to add to')
                        # self.debug_print('pop')
                        self.msg_queue.pop(0)
                        new_id = init_new_id
                        self.debug_print('Now that we popped that measurement, there is a new oldest measurement, and we will go back and go through tests again')
                    else:
                        self.debug_print(f'The new id decremented to {new_id} still could use a unary. We will do a nother loop, keeping the same oldest measurement')
                else:
                    self.debug_print('Looks like the oldest measurement is closer to the latest node we are checking')

                    self.debug_print('Checking to see if the oldest measurement or the newer measurement is closer to the node')
                    time_old_to_pose = abs(oldest_measurement_time - newer_key_time)
                    time_next_to_pose = abs(next_measurement_time - newer_key_time)

                    if(next_measurement_time < newer_key_time):
                    # Take care of where next measurement is not past next node
                        self.debug_print('Looks like the newer measurement is also earlier than the newer key time and therefore closer, pop!')
                        self.msg_queue.pop(0)
                    
                    elif(time_old_to_pose > time_next_to_pose):
                    # Take care of case where next measurement is better
                        self.debug_print('Looks like the time difference between the oldest measurement to the node is greater than the newer measurement to the pose, so pop!\nAlso set the new_id to be what it initially was to start over')
                        self.msg_queue.pop(0)
                        new_id = init_new_id

                    else:
                        # Actually add the factor
                        self.debug_print('The older measurement is closer than the newer measurement,\nand is therefore the closest, because we know that the two measurements are straddling the node')
                        self.debug_print('Popping and saving the pop as the measurement to add')
                        poseKey_to_add = new_id
                        msg_to_add, time_stamp = self.msg_queue.pop(0)                    
                        self.last_pose_key = new_id
                        # return poseKey_to_add, msg_to_add, time_stamp
            else:
                self.debug_print('The oldest measurement time is newer than the new_id, we are done\n')
                in_future = True

        return poseKey_to_add, msg_to_add, time_stamp
    