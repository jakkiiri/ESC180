def predict_intersection(ball_pos, prev_ball_pos, paddle_x, table_size):
    """
    Predict where ball will intersect paddle plane using both position and velocity
    """
    # Calculate ball velocity
    ball_vel = (ball_pos[0] - prev_ball_pos[0], 
                ball_pos[1] - prev_ball_pos[1])
    
    # Check if ball is moving towards paddle
    is_moving_towards = ((paddle_x < ball_pos[0] and ball_vel[0] < 0) or 
                        (paddle_x > ball_pos[0] and ball_vel[0] > 0))
    
    if not is_moving_towards:
        return ball_pos[1]  # Follow ball's current position if not moving towards paddle
    
    # Use velocity to predict rough position
    if ball_vel[0] != 0:
        time = (paddle_x - ball_pos[0]) / ball_vel[0]
        vel_prediction = ball_pos[1] + (ball_vel[1] * time)
    else:
        vel_prediction = ball_pos[1]
    
    # Use position to predict trajectory
    dx = paddle_x - ball_pos[0]
    dy = ball_pos[1] - prev_ball_pos[1]
    if dx != 0:
        slope = dy / dx
        pos_prediction = ball_pos[1] + (slope * dx)
    else:
        pos_prediction = ball_pos[1]
    
    # Combine predictions (weighted towards velocity prediction)
    y_intersect = (2 * vel_prediction + pos_prediction) / 3
    
    # Handle bounces
    while y_intersect < 0 or y_intersect > table_size[1]:
        if y_intersect < 0:
            y_intersect = -y_intersect
        else:
            y_intersect = 2 * table_size[1] - y_intersect
    
    return min(max(y_intersect, 30), table_size[1] - 30)

# Global state
prev_ball_pos = None

def pong_ai(paddle_frect, other_paddle_frect, ball_frect, table_size):
    """
    AI that uses both velocity and position for prediction
    """
    global prev_ball_pos
    
    # Get positions
    ball_pos = (ball_frect.pos[0] + ball_frect.size[0]/2, 
                ball_frect.pos[1] + ball_frect.size[1]/2)
    paddle_y = paddle_frect.pos[1] + paddle_frect.size[1]/2
    paddle_x = paddle_frect.pos[0]
    center_y = table_size[1]/2
    
    # Initialize previous ball position
    if prev_ball_pos is None:
        prev_ball_pos = ball_pos
        return None
    
    # Predict ball position
    predicted_y = predict_intersection(ball_pos, prev_ball_pos, paddle_x, table_size)
    prev_ball_pos = ball_pos
    
    # Always move to predicted position with a small threshold
    if abs(paddle_y - predicted_y) > 1:  # Reduced threshold for more responsive movement
        return "down" if paddle_y < predicted_y else "up"
    
    # Return to center only when ball is very far
    if abs(ball_pos[0] - paddle_x) > 100:  # Increased distance threshold
        if abs(paddle_y - center_y) > 2:
            return "down" if paddle_y < center_y else "up"
    
    return None 