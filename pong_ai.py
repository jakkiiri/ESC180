def predict_intersection(ball_pos, prev_ball_pos, paddle_x, table_size):
    """
    Predict where ball will intersect paddle plane with safety checks
    """
    # Calculate ball velocity
    ball_vel = (ball_pos[0] - prev_ball_pos[0], 
                ball_pos[1] - prev_ball_pos[1])
    
    # Check if ball is moving towards paddle
    is_moving_towards = ((paddle_x < ball_pos[0] and ball_vel[0] < 0) or 
                        (paddle_x > ball_pos[0] and ball_vel[0] > 0))
    
    if not is_moving_towards:
        return ball_pos[1]  # Stay at ball's height if not moving towards paddle
    
    # Simple velocity-based prediction
    if ball_vel[0] != 0:
        time = (paddle_x - ball_pos[0]) / ball_vel[0]
        predicted_y = ball_pos[1] + (ball_vel[1] * time)
    else:
        predicted_y = ball_pos[1]
    
    # Handle bounces
    while predicted_y < 0 or predicted_y > table_size[1]:
        if predicted_y < 0:
            predicted_y = -predicted_y
        else:
            predicted_y = 2 * table_size[1] - predicted_y
    
    return min(max(predicted_y, 30), table_size[1] - 30)

# Global state
prev_ball_pos = None

def pong_ai(paddle_frect, other_paddle_frect, ball_frect, table_size):
    """
    AI that won't dodge the ball
    """
    global prev_ball_pos
    
    # Get positions
    ball_pos = (ball_frect.pos[0] + ball_frect.size[0]/2, 
                ball_frect.pos[1] + ball_frect.size[1]/2)
    paddle_y = paddle_frect.pos[1] + paddle_frect.size[1]/2
    paddle_x = paddle_frect.pos[0]
    
    # Initialize previous ball position
    if prev_ball_pos is None:
        prev_ball_pos = ball_pos
        return None
    
    # Ball is very close - move directly to ball's height
    if abs(ball_pos[0] - paddle_x) < 20:
        if abs(paddle_y - ball_pos[1]) > 2:
            return "down" if paddle_y < ball_pos[1] else "up"
    else:
        # Predict ball position
        predicted_y = predict_intersection(ball_pos, prev_ball_pos, paddle_x, table_size)
        
        # Move to predicted position
        if abs(paddle_y - predicted_y) > 2:
            return "down" if paddle_y < predicted_y else "up"
    
    prev_ball_pos = ball_pos
    return None 