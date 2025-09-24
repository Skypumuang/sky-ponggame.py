import streamlit as st
import time
import numpy as np

# Game constants
WIDTH, HEIGHT = 800, 400
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 80
BALL_RADIUS = 10
PLAYER_X = 20
AI_X = WIDTH - PADDLE_WIDTH - 20

# Initialize session state
if "player_y" not in st.session_state:
    st.session_state.player_y = (HEIGHT - PADDLE_HEIGHT) // 2
if "ai_y" not in st.session_state:
    st.session_state.ai_y = (HEIGHT - PADDLE_HEIGHT) // 2
if "ball" not in st.session_state:
    st.session_state.ball = {
        "x": WIDTH // 2,
        "y": HEIGHT // 2,
        "vx": 5 * np.random.choice([-1, 1]),
        "vy": 3 * np.random.choice([-1, 1]),
    }
if "score" not in st.session_state:
    st.session_state.score = [0, 0]  # [player, AI]

def reset_ball():
    st.session_state.ball = {
        "x": WIDTH // 2,
        "y": HEIGHT // 2,
        "vx": 5 * np.random.choice([-1, 1]),
        "vy": 3 * np.random.choice([-1, 1]),
    }

def update_ball():
    ball = st.session_state.ball
    ball["x"] += ball["vx"]
    ball["y"] += ball["vy"]

    # Top/bottom wall collision
    if ball["y"] - BALL_RADIUS < 0:
        ball["y"] = BALL_RADIUS
        ball["vy"] *= -1
    if ball["y"] + BALL_RADIUS > HEIGHT:
        ball["y"] = HEIGHT - BALL_RADIUS
        ball["vy"] *= -1

    # Left paddle (player) collision
    if (
        ball["x"] - BALL_RADIUS < PLAYER_X + PADDLE_WIDTH and
        st.session_state.player_y < ball["y"] < st.session_state.player_y + PADDLE_HEIGHT
    ):
        ball["x"] = PLAYER_X + PADDLE_WIDTH + BALL_RADIUS
        ball["vx"] *= -1
        ball["vy"] += (ball["y"] - (st.session_state.player_y + PADDLE_HEIGHT / 2)) * 0.1

    # Right paddle (AI) collision
    if (
        ball["x"] + BALL_RADIUS > AI_X and
        st.session_state.ai_y < ball["y"] < st.session_state.ai_y + PADDLE_HEIGHT
    ):
        ball["x"] = AI_X - BALL_RADIUS
        ball["vx"] *= -1
        ball["vy"] += (ball["y"] - (st.session_state.ai_y + PADDLE_HEIGHT / 2)) * 0.1

    # Score and reset when ball goes off left/right edge
    if ball["x"] < 0:
        st.session_state.score[1] += 1
        reset_ball()
    if ball["x"] > WIDTH:
        st.session_state.score[0] += 1
        reset_ball()

def update_ai():
    center = st.session_state.ai_y + PADDLE_HEIGHT / 2
    ball_y = st.session_state.ball["y"]
    # Move AI paddle towards the ball
    if center < ball_y - 10:
        st.session_state.ai_y += 4
    elif center > ball_y + 10:
        st.session_state.ai_y -= 4
    # Clamp inside canvas
    st.session_state.ai_y = max(0, min(HEIGHT - PADDLE_HEIGHT, st.session_state.ai_y))

def draw_game():
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(WIDTH/100, HEIGHT/100))
    ax.set_facecolor('black')
    ax.set_xlim(0, WIDTH)
    ax.set_ylim(0, HEIGHT)
    # Draw paddles
    ax.add_patch(plt.Rectangle((PLAYER_X, st.session_state.player_y), PADDLE_WIDTH, PADDLE_HEIGHT, color='white'))
    ax.add_patch(plt.Rectangle((AI_X, st.session_state.ai_y), PADDLE_WIDTH, PADDLE_HEIGHT, color='white'))
    # Draw ball
    ax.add_patch(plt.Circle((st.session_state.ball["x"], st.session_state.ball["y"]), BALL_RADIUS, color='white'))
    ax.axis('off')
    st.pyplot(fig)

st.title("Pong Game")
st.subheader("make by ai")
st.markdown("Use the slider to move your paddle (left). The right paddle is controlled by AI.")

player_y_new = st.slider("Player Paddle Position", 0, HEIGHT - PADDLE_HEIGHT, st.session_state.player_y)
st.session_state.player_y = player_y_new

if st.button("Restart Game"):
    st.session_state.player_y = (HEIGHT - PADDLE_HEIGHT) // 2
    st.session_state.ai_y = (HEIGHT - PADDLE_HEIGHT) // 2
    reset_ball()
    st.session_state.score = [0, 0]

draw_game()
st.write(f"**Score:** You {st.session_state.score[0]} : AI {st.session_state.score[1]}")

if st.button("Next Frame"):
    update_ball()
    update_ai()
    draw_game()
    st.write(f"**Score:** You {st.session_state.score[0]} : AI {st.session_state.score[1]}")
    st.experimental_rerun()

# Optionally, auto-play frames for demo (not real-time, but animates)
if st.checkbox("Auto Play"):
    for _ in range(50):  # play 50 frames
        update_ball()
        update_ai()
        draw_game()
        time.sleep(0.05)
        st.experimental_rerun()

