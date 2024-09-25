
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
    
    # use cur_star as a boolean to check if the user
    # is elligible to use the star
    cur_star = False
    cur_star_activity = None
    # int variable to track the number of stars offered
    num_star = 0

    bored_with_stars = False
    
    # the user starts resting
    last_activity = "resting"
    last_activity_duration = 0
    
    # boolean to keep track if the user is tired
    tired = False

    cur_time = 0
    
    last_finished = -1000
    
# activity information

# running gives 3 health points (up to 180 minutes)
# 1 health per minute after this
# resting between running resets this timer

# Carrying textbooks always gives 2 health points per minute

# resting gives 0 hedons

# Running and carrying textbooks give -2 hedons/minute 
# if the user is tired and not using a star
# resting less than 2 hours will make the user tired 

# if user is not tired, running gives 2 hedons / minute
# for the first ten minutes, and -2 hedons/min for every 
# minute after the first 10

# if user is not tired, carrying textbooks gives 1 hedon/min
# for the first 20 mins, and -1 hedon / min after

# if star is offered and used right away, additional
# 3 hedons / min for at most 10 mins.  This effect only
# works for the first time the activity is performed
# right after

# if three stars are offered within the span of 2 hours
# user loses interests and stars do not function
# for the rest 
            

def star_can_be_taken(activity):
    pass

    
def perform_activity(activity, duration):
    
    global cur_star
    global cur_star_activity
    global cur_hedons

    # running conditions
    if (activity == "running"):
        # check duration for health
        if (duration <= 180):
            cur_health += duration * 3
        else:
            # get sum of the first 180 minutes
            # with the additional minutes
            cur_health += (180 * 3) + (duration - 180)
        # if user is tired
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

# this function returns the cur_hedons as an integer
def get_cur_hedons():
    global cur_hedons
    return cur_hedons
    
# this function returns the cur_health as an integer
def get_cur_health():
    global cur_health
    return cur_health
    
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
    
    
    