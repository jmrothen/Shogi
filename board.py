from piece import *
import matplotlib.pyplot as plt


# let's create a nice reference df so it's easy to visualize the board positions
def boardref():
    board_ref = pd.DataFrame([[1, 2, 3, 4, 5, 6, 7, 8, 9],
                              [10, 11, 12, 13, 14, 15, 16, 17, 18],
                              [19, 20, 21, 22, 23, 24, 25, 26, 27],
                              [28, 29, 30, 31, 32, 33, 34, 35, 36],
                              [37, 38, 39, 40, 41, 42, 43, 44, 45],
                              [46, 47, 48, 49, 50, 51, 52, 53, 54],
                              [55, 56, 57, 58, 59, 60, 61, 62, 63],
                              [64, 65, 66, 67, 68, 69, 70, 71, 72],
                              [73, 74, 75, 76, 77, 78, 79, 80, 81]],
                             columns=['9', '8', '7', '6', '5', '4', '3', '2', '1'])
    board_ref.index = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    return board_ref


def draw_shogi_board(piece_array=None, save_path=None):
    fig, ax = plt.subplots(figsize=(9, 9))

    if not piece_array:
        piece_array = create_piece_array()

    # Draw grid lines
    for i in range(10):
        ax.plot([0, 9], [i, i], color='black')
        ax.plot([i, i], [0, 9], color='black')

    # Set the x and y axis limits
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 9)

    # Remove the ticks
    ax.set_xticks([])
    ax.set_yticks([])

    # Add labels for columns
    col_labels = list(range(1, 10))[::-1]
    row_labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'][::-1]

    for i, label in enumerate(col_labels):
        ax.text(i + 0.5, 9.5, label, ha='center', va='center')

    # Add labels for rows
    for i, label in enumerate(row_labels):
        ax.text(-0.5, i + 0.5, label, ha='center', va='center')

    # Add text to each tile
    for i in piece_array:
        row, col = pos_to_xy(i.pos)
        ax.text(col + .5, 8.5 - row, i.shorthand(), ha='center', va='center', fontsize=10)

    # Add grid background
    ax.set_facecolor('beige')

    # Draw the board border
    ax.plot([0, 9], [0, 0], color='black', linewidth=2)
    ax.plot([0, 9], [9, 9], color='black', linewidth=2)
    ax.plot([0, 0], [0, 9], color='black', linewidth=2)
    ax.plot([9, 9], [0, 9], color='black', linewidth=2)

    plt.gca().set_aspect('equal', adjustable='box')

    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)

    plt.show()

# draw_shogi_board(save_path='shogiboard.jpeg')
