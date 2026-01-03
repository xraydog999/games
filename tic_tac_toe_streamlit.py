install streamlit
import streamlit as st

st.set_page_config(page_title="Tic Tac Toe", page_icon="🎮")

# --- Helper functions ---

def init_game():
    """Initialize or reset the game state."""
    st.session_state.board = [""] * 9  # 3x3 board flattened
    st.session_state.current_player = "X"
    st.session_state.winner = None
    st.session_state.game_over = False
    st.session_state.move_count = 0


def check_winner(board):
    """Return 'X' or 'Y' if there's a winner, 'Draw' if board full, or None otherwise."""
    winning_combos = [
        (0, 1, 2),  # rows
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),  # columns
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),  # diagonals
        (2, 4, 6),
    ]

    for a, b, c in winning_combos:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]

    if "" not in board:
        return "Draw"

    return None


def make_move(index):
    """Handle a move at the given board index."""
    if st.session_state.game_over:
        return

    if st.session_state.board[index] == "":
        st.session_state.board[index] = st.session_state.current_player
        st.session_state.move_count += 1

        winner = check_winner(st.session_state.board)
        if winner:
            st.session_state.winner = winner
            st.session_state.game_over = True
        else:
            st.session_state.current_player = "O" if st.session_state.current_player == "X" else "X"


# --- Initialize session state ---

if "board" not in st.session_state:
    init_game()

# --- UI ---

st.title("Tic Tac Toe")
st.write("Play a simple game of Tic Tac Toe. Two players share the same screen.")

# Status message
if st.session_state.game_over:
    if st.session_state.winner == "Draw":
        st.subheader("It's a draw!")
    else:
        st.subheader(f"Player {st.session_state.winner} wins! 🎉")
else:
    st.subheader(f"Player {st.session_state.current_player}'s turn")

# Board layout: 3 columns x 3 rows
for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        idx = row * 3 + col
        cell_value = st.session_state.board[idx]

        # Make each cell a button; disable if taken or game is over
        if cols[col].button(
            cell_value if cell_value != "" else " ",
            key=f"cell_{idx}",
            disabled=(cell_value != "" or st.session_state.game_over),
            use_container_width=True,
        ):
            make_move(idx)

# Reset button
st.markdown("---")
if st.button("Restart game 🔄"):
    init_game()
    st.experimental_rerun()

