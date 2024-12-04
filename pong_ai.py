def predict_ball_position(ball_pos, ball_vel, paddle_y, table_size):
    """Predict where the ball will intersect with the paddle's x position"""
    # If ball is moving away from paddle, return center position
    if ball_vel[0] < 0:
        return table_size[1] / 2

    # Calculate time until ball reaches paddle's x position
    distance_to_paddle = paddle_y - ball_pos[0]
    time_to_paddle = distance_to_paddle / ball_vel[0]
    
    # Calculate y position when ball reaches paddle
    future_y = ball_pos[1] + ball_vel[1] * time_to_paddle
    
    # Account for bounces
    while future_y < 0 or future_y > table_size[1]:
        if future_y < 0:
            future_y = -future_y
        elif future_y > table_size[1]:
            future_y = 2 * table_size[1] - future_y
            
    return future_y

def pong_ai(paddle_frect, other_paddle_frect, ball_frect, table_size):
    """
    Vector-based AI that properly responds to diagonal ball movement
    """
    # Ball position and dimensions
    ball_center = (ball_frect.pos[0] + ball_frect.size[0]/2,
                  ball_frect.pos[1] + ball_frect.size[1]/2)
    paddle_center = paddle_frect.pos[1] + paddle_frect.size[1]/2
    
    # Determine if we're the left or right paddle
    is_left_paddle = paddle_frect.pos[0] < table_size[0]/2
    paddle_x = paddle_frect.pos[0]
    
    # If ball is moving away, return to center
    if (is_left_paddle and ball_center[0] < paddle_x) or \
       (not is_left_paddle and ball_center[0] > paddle_x):
        return "up" if paddle_center > table_size[1]/2 else "down"
    
    # Calculate ball's y-position when it reaches paddle's x-position
    x_distance = abs(paddle_x - ball_center[0])
    y_distance = abs(paddle_center - ball_center[1])
    
    # Move paddle based on ball's position and vertical direction
    if ball_center[1] > paddle_center:
        # Ball is below paddle
        if y_distance > x_distance/8:  # Adjust this ratio to tune responsiveness
            return "down"
    elif ball_center[1] < paddle_center:
        # Ball is above paddle
        if y_distance > x_distance/8:
            return "up"
    
    return None 