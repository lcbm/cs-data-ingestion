import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

import frontend.constants as constants


def generate_3d_line_graph_gif(df, column, line_a, line_b=None):
    """ Generates 3d, animated, line graphs. """

    def rotate(angle):
        ax.view_init(azim=angle)

    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")

    df_1 = df.loc[df[column] == line_a]
    ax.plot(
        df_1[constants.REPORT_COLUMN_X],
        df_1[constants.REPORT_COLUMN_Z],
        zs=df_1[constants.REPORT_COLUMN_Y],
    )
    ax.text(0.05, 0.3, 0.8, f"{column} {line_a}", size=10, zorder=1, color="blue")

    if line_b is not None:
        df_2 = df.loc[df[column] == line_b]
        ax.plot(
            df_2[constants.REPORT_COLUMN_X],
            df_2[constants.REPORT_COLUMN_Z],
            zs=df_2[constants.REPORT_COLUMN_Y],
        )
        ax.text(
            0.05, 0.3, 0.82, f"{column} {line_b}", size=10, zorder=1, color="orange"
        )

    ax.set_xlabel(constants.REPORT_COLUMN_X)
    ax.set_ylabel(constants.REPORT_COLUMN_Z)
    ax.set_zlabel(constants.REPORT_COLUMN_Y)

    file_name = (
        f"{constants.STATIC_DIR_PATH}/line_3d_{column}_{line_a}_{column}_{line_b}.gif"
    )
    rot_animation = animation.FuncAnimation(
        fig, rotate, frames=np.arange(0, 362, 2), interval=100
    )
    rot_animation.save(file_name, dpi=80, writer="imagemagick")


def genered_2d_line_graph_png(df, column, column_value):
    """
    Generates 2d line graphs comparing the ideal movement with the one
    executed by the patient.
    """
    ax = plt.axes()

    df = df.loc[df[column] == column_value]
    ax.plot(df[constants.REPORT_COLUMN_X], df[constants.REPORT_COLUMN_Y], color="blue")

    x_perfect_line = [
        min(df[constants.REPORT_COLUMN_X]),
        max(df[constants.REPORT_COLUMN_X]),
    ]
    y_perfect_line_1 = [
        min(df[constants.REPORT_COLUMN_Y]),
        max(df[constants.REPORT_COLUMN_Y]),
    ]
    y_perfect_line_2 = [
        max(df[constants.REPORT_COLUMN_Y]),
        min(df[constants.REPORT_COLUMN_Y]),
    ]

    ax.plot(x_perfect_line, y_perfect_line_1, color="red")
    ax.plot(x_perfect_line, y_perfect_line_2, color="red")

    plt.suptitle("Paciente (azul) vs Perfeito (vermelho)")
    plt.savefig(f"{constants.STATIC_DIR_PATH}/line_2d_{column}_{column_value}.png")
