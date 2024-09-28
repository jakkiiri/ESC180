''' initializes global variables and sets them to their default values '''
def initialize():
    
    global cur_hedons, cur_health
    global cur_time
    global last_activity, last_activity_duration
    global cur_star
    # True or False
    global cur_star_activity
    # = 'running', 'textbooks'
    global num_star
    global star_time_1, star_time_2, star_time_3
    global last_finished
    global bored_with_stars
    global tired
    
    ''' hedons and health variables'''
    cur_hedons = 0
    cur_health = 0 
    
    ''' use cur_star as a boolean to check if the user is elligible to use the star '''
    cur_star = False
    cur_star_activity = None
    ''' int variable to track the number of stars offered '''
    num_star = 0
    star_time_1 = -1000
    star_time_2 = -1000
    star_time_3 = -1000

    bored_with_stars = False
    
    # the user starts resting
    last_activity = "resting"
    last_activity_duration = 0
    
    # boolean to keep track if the user is tired
    tired = False

    cur_time = 0
    
    last_finished = -1000
    
def perform_activity(activity, duration):
    global cur_hedons
    global cur_health
    global cur_time
    global tired
    global cur_star
    global last_finished
    global last_activity
    global last_activity_duration

    ''' check if the player will be tired for this activity '''
    is_tired()
    ''' update cur_time '''
    cur_time += duration
    total_duration = duration

    ''' checks which activity is being performed '''
    ''' For activity running '''
    if (activity == "running"):
        ''' updating health '''
        ''' check if last activity was also running '''
        if last_activity == activity:
            total_duration = last_activity_duration + duration

        ''' check if combined duration is under 180 minutes, add health accordingly '''
        if (total_duration <= 180):
            cur_health += duration * 3
        else:
            ''' account for if last_activity_duration greater than or less than 180 minutes '''
            if last_activity ==  activity:
                if last_activity_duration>180:
                    cur_health += duration
                else:
                    cur_health += (180-last_activity_duration) * 3 + (total_duration - 180)
            else:
                cur_health += 180*3 + (duration-180)

        ''' updating hedons'''
        ''' calculate initial hedons per minute '''
        hedons_per_min = 0
        if star_can_be_taken(activity):
            hedons_per_min += 3
        if tired:
            hedons_per_min -= 2
        if not tired:
            hedons_per_min +=2
        ''' check whether player is tired or has a star, and update hedons accordingly '''
        if duration > 10:
            if star_can_be_taken(activity):
                ''' Case 1: Star while not tired and Case 2: Star while tired'''
                if not tired:
                    cur_hedons += hedons_per_min*10
                    hedons_per_min -= 7
                    cur_hedons += hedons_per_min*(duration-10)
                else:
                    cur_hedons += hedons_per_min*10
                    hedons_per_min -= 3
                    cur_hedons += hedons_per_min*(duration-10)
            else:
                ''' Case 3: no Star while not tired and Case 4: no Star while tired'''
                if not tired:
                    cur_hedons += hedons_per_min*10
                    hedons_per_min -= 4
                    cur_hedons += hedons_per_min*(duration-10)
                else:
                    cur_hedons += hedons_per_min*duration
        else:
            cur_hedons += hedons_per_min*duration
        
        ''' resets cur_star, sets last_finished to cur_time '''
        cur_star = False
        last_finished = cur_time

    ''' for activity carrying textbooks '''
    if (activity == "textbooks"):
        ''' updating health '''
        cur_health += duration * 2

        ''' check whether player is tired or has a star, and update hedons accordingly '''
        if duration > 20:
            if star_can_be_taken(activity):
                ''' Case: has Star, duration > 20 minutes '''
                cur_hedons += 30
            if not tired:
                ''' Case: not tired, duration > 20 minutes '''
                cur_hedons += 1*20
                cur_hedons -= 1*(duration-20)
            else:
                ''' Case: tired '''
                cur_hedons -= 2*duration
        elif duration > 10:
            if star_can_be_taken(activity):
                ''' Case: has Star, duration > 10 minutes '''
                cur_hedons += 30
            if not tired:
                ''' Case: not tired, duration < 20 minutes '''
                cur_hedons += 1*duration
            else:
                ''' Case: tired '''
                cur_hedons -= 2*duration
        else:
            if star_can_be_taken(activity):
                ''' Case: has Star, duration <= 10 minutes '''
                cur_hedons += 3*duration
            if not tired:
                ''' Case: not tired, duration < 20 minutes'''
                cur_hedons += 1*duration
            else:
                ''' Case: tired '''
                cur_hedons -= 2*duration

        ''' resets cur_star and sets last_finished to cur_time '''
        cur_star = False
        last_finished = cur_time
        
        ''' for activity resting '''
        if (activity == "resting"):
            ''' no hedon or health awarded with the exception of Star '''
            if (star_can_be_taken(activity)):
                if (duration > 10):
                    cur_hedons += 30
                else:
                    cur_hedons += 3*duration
                ''' reset cur_star '''
                cur_star = False
    last_activity = activity
    last_activity_duration = duration
    


''' this function returns the cur_hedons as an integer '''
def get_cur_hedons():
    global cur_hedons
    return cur_hedons
    
''' this function returns the cur_health as an integer '''
def get_cur_health():
    global cur_health
    return cur_health
    
def star_can_be_taken(activity):
    global num_star
    global star_time_1, star_time_2, star_time_3
    if cur_star_activity == activity and cur_star:
        num_star += 1
        is_bored_with_stars()
        if bored_with_stars:
            return False
        else:
            star_time_1, star_time_2, star_time_3 = cur_time, star_time_1, star_time_2
            return True
    else:
        return False

def offer_star(activity):
    global cur_star
    global cur_star_activity
    cur_star = True
    cur_star_activity = activity

def is_tired():
    global last_finished
    global tired
    global cur_time
    if cur_time-last_finished < 120:
        tired = True
    else:
        tired = False

def is_bored_with_stars():
    global bored_with_stars
    if num_star >= 3:
        if cur_time-star_time_3 <= 120:
            bored_with_stars = True

def most_fun_activity_minute():

    '''calculate the amount of hedon you can earn per minute for each activity'''
    hedon_rest = 0
    hedon_textbook = 0
    hedon_running = 0

    '''check star condition'''
    if (cur_star and cur_star_activity == "resting"):
        hedon_rest += 3

    '''check star condition'''
    if (cur_star and cur_star_activity == "running"):
        hedon_running += 3

    '''check star condition'''
    if (cur_star and cur_star_activity == "textbook"):
        hedon_textbook += 3
    
    is_tired() # update tiredness
    '''check if user is tired'''
    if (tired):
        hedon_textbook -= 2
        hedon_running -= 2
    else:
        hedon_textbook += 1
        hedon_running += 2
    if max(max(hedon_textbook, hedon_running), hedon_rest) == hedon_rest:
        return 'resting'
    if max(max(hedon_textbook, hedon_running), hedon_rest) == hedon_running:
        return 'running'
    if max(max(hedon_textbook, hedon_running), hedon_rest) == hedon_textbook:
        return 'textbooks'
            

        
    
################################################################################
#These functions are not required, but we recommend that you use them anyway
#as helper functions

def get_effective_minutes_left_hedons(activity):
    '''Return the number of minutes during which the user will get the full
    amount of hedons for activity activity'''
    pass
    
def get_effective_minutes_left_health(activity):
    pass    

def estimate_hedons_delta(activity, duration):
    '''Return the amount of hedons the user would get for performing activity
    activity for duration minutes'''
    pass
            

def estimate_health_delta(activity, duration):
    pass
        
################################################################################
        
if __name__ == '__main__':
    initialize()
    perform_activity("running", 30)    
    print(get_cur_hedons())            # -20 = 10 * 2 + 20 * (-2)             # Test 1
    print(get_cur_health())            # 90 = 30 * 3                          # Test 2           		
    print(most_fun_activity_minute())  # resting                              # Test 3
    perform_activity("resting", 30)    
    offer_star("running")              
    print(most_fun_activity_minute())  # running                              # Test 4
    perform_activity("textbooks", 30)  
    print(get_cur_health())            # 150 = 90 + 30*2                      # Test 5
    print(get_cur_hedons())            # -80 = -20 + 30 * (-2)                # Test 6
    offer_star("running")
    perform_activity("running", 20)
    print(get_cur_health())            # 210 = 150 + 20 * 3                   # Test 7
    print(get_cur_hedons())            # -90 = -80 + 10 * (3-2) + 10 * (-2)   # Test 8
    perform_activity("running", 170)
    print(get_cur_health())            # 700 = 210 + 160 * 3 + 10 * 1         # Test 9
    print(get_cur_hedons())            # -430 = -90 + 170 * (-2)              # Test 10
    
    
    