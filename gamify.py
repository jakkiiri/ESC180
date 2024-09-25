
# intialize function
# initialize all of the necessary values for the simulation
# returns none
def initialize():
    
    global cur_hedons, cur_health

    global cur_time
    global last_activity, last_activity_duration
    global cur_star
    global cur_star_activity
    global num_star
    
    global last_finished
    global bored_with_stars

    global tired
    
    cur_hedons = 0
    cur_health = 0 
    
    '''
    use cur_star as a boolean to check if the user
    is elligible to use the star
    '''
    cur_star = False
    cur_star_activity = None
    '''
    int variable to track the number of stars offered
    '''
    num_star = 0

    bored_with_stars = False
    
    # the user starts resting
    last_activity = "resting"
    last_activity_duration = 0
    
    # boolean to keep track if the user is tired
    tired = False

    cur_time = 0
    
    last_finished = -1000
    
'''activity information
The user starts out with 0 health points, and 0 hedons.
• The user is always either running, carrying textbooks, or resting.
• Running gives 3 health points per minute for up to 180 minutes, and 1 health point per minute for
every minute over 180 minutes that the user runs. (Note that if the user runs for 90 minutes, then
rests for 10 minutes, then runs for 110 minutes, the user will get 600 health points, since they rested
in between the times that they ran.)
• Carrying textbooks always gives 2 health points per minute.
• Resting gives 0 hedons per minute.
• Both running and carrying textbooks give -2 hedons per minute if the user is tired and isn’t using
a star (definition: the user is tired if they finished running or carrying textbooks less than 2 hours
before the current activity started.) For example, for the purposes of this rule, the user will be tired
if they run for 2 minutes, and then start running again straight away.
Engineering Science, University of Toronto Page 4 of 8
ESC 180 H1F Project # 1 — Gamification of Exercise Fall 2024
• If the user is not tired, running gives 2 hedons per minute for the first 10 minutes of running, and -2
hedons per minute for every minute after the first 10.
• If the user is not tired, carrying textbooks gives 1 hedon per minute for the first 20 minutes, and -1
hedon per minute for every minute after the first 20.
• If a star is offered for a particular activity and the user takes the star right away, the user gets an
additional 3 hedons per minute for at most 10 minutes. Note that the user only gets 3 hedons per
minute for the first activity they undertake, and do not get the hedons due to the star if they decide
to keep performing the activity:
offer_star("running")
perform_activity("running", 5) # gets extra hedons
perform_activity("running", 2) # no extra hedons
• If three stars are offered within the span of 2 hours, the user loses interest, and will not get additional
hedons due to stars for the rest of the simulation.
'''   
def perform_activity(activity, duration):
    
    global cur_star
    global cur_star_activity
    global cur_hedons
    global cur_health
    global cur_time
    global tired

    ''' check if the player will be tired for this activity '''
    
    total_duration = duration
    # running conditions
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
        ''' check whether player is tired, and update hedons accordingly '''
        hedons_per_min = 0
        if not bored_with_stars:
            if star_can_be_taken(activity):
                hedons_per_min += 3
        if tired:
            hedons_per_min -= 2
        

        if (tired):
            # check star
            # check if user used star 
            if (star_can_be_taken("running") and cur_star_activity == "running" and cur_star):
                if (duration < 10):
                    cur_hedons = duration * 3
                else:
                    cur_hedons += 30
                # reset cur_star
                cur_star = False
            else:
                cur_hedon -= duration * 2
        # if user is not tired
        else:
            if (duration <= 10):
                cur_hedon += duration * 2
            else:
                cur_hedon += 20 - ((duration-10) * 2)
            # check star
            # check if user used star 
            if (star_can_be_taken("running") and cur_star_activity == "running" and cur_star):
                if (duration < 10):
                    cur_hedons = duration * 3
                else:
                    cur_hedons += 30
                # reset cur_star
                cur_star = False

    # textbook conditions
    if (activity == "textbook"):
        # update health
        cur_health += duration * 2
        if (tired):
            # check star
            # check if user used star 
            if (star_can_be_taken("textbook") and cur_star_activity == "textbook" and cur_star):
                if (duration < 10):
                    cur_hedons = duration * 3
                else:
                    cur_hedons += 30
                # reset cur_star
                cur_star = False
            else:
                cur_hedon -= duration * 2
        # if user is not tired
        else:
            if (duration <= 20):
                cur_hedon += duration
            else:
                cur_hedon += 20 - (duration-20)
            # check star
            # check if user used star 
            if (star_can_be_taken("textbook") and cur_star_activity == "textbook" and cur_star):
                if (duration < 10):
                    cur_hedons = duration * 3
                else:
                    cur_hedons += 30
                # reset cur_star
                cur_star = False

        # resting conditions
        if (activity == "resting"):
            # no hedon or health awarded with the exception
            # of the star
            if (star_can_be_taken("resting") and cur_star_activity == "resting" and cur_star):
                if (duration < 10):
                    cur_hedons = duration * 3
                else:
                    cur_hedons += 30
                # reset cur_star
                cur_star = False

# update functions
def update_time(time):
    global cur_time
    cur_time += time

def update_health(health):
    global cur_health
    cur_health += health

def update_hedons(hedon):
    global cur_hedons
    cur_hedons += hedon

# this function returns the cur_hedons as an integer
def get_cur_hedons():
    global cur_hedons
    return cur_hedons
    
# this function returns the cur_health as an integer
def get_cur_health():
    global cur_health
    return cur_health
    
def star_can_be_taken(activity):
    if cur_star_activity == activity and cur_star:
        return True
    else:
        return False

def offer_star(activity):
    pass
        
def most_fun_activity_minute():
    pass
    
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
    
    
    