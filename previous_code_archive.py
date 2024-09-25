'''
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
'''

'''
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
        '''