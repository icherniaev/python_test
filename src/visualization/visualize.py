import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_0() -> None:
    """
    Creates initial plot illustrating different reference frames
    """

    fig, ax = plt.subplots(figsize=(5, 5))

    ax.arrow(1.6, 1.4, -0.2, 0.2, width=0.01, color='black')
    ax.arrow(1.6, 1.6, -0.2, -0.2, width=0.01, color='black')

    ax.text(1.43, 1.6, "x'")
    ax.text(1.4, 1.35, "y'")

    ax.plot([1.4, 1.5, 1.6, 1.5, 1.4], [1.5, 1.4, 1.5, 1.6, 1.5])

    ax.set_xlim(1, 2)
    ax.set_ylim(1, 2)

    ax.set_title("Global and local reference frames")
    ax.set_xlabel('x')
    ax.set_xlabel('y')


def EDA(df: pd.DataFrame) -> None:
    """
    Creates exploratory data analysis visualisation

    Parameters
    ----------
    df: pd.Dataframe
        Initial DataFrame
    """

    fig, ax = plt.subplots(2, 2, figsize=(12, 10))

    # Position
    ax[0][0].scatter(df.x_mm,
                     df.y_mm,
                     s=20,
                     c='orangered')
    ax[0][0].plot(df.iloc[[0, -1]]['x_mm'],
                  df.iloc[[0, -1]]['y_mm'],
                  linewidth=1)
    ax[0][0].set_title('Position')
    ax[0][0].set_xlabel('x')
    ax[0][0].set_ylabel('y')

    # Update frequency
    ax[0][1].plot(df.timedelta)
    ax[0][1].hlines(df.timedelta.mean(),
                    xmin=0,
                    xmax=df.shape[0],
                    linestyles='dashed',
                    colors=['orangered'])
    ax[0][1].set_title('Update frequency')
    ax[0][1].set_ylabel('Seconds')
    ax[0][1].set_xlabel('Timestamp')

    # Roll
    ax[1][0].plot(df.roll_deg)
    ax[1][0].set_title('Roll')
    ax[1][0].set_ylabel('Degrees')
    ax[1][0].set_xlabel('Timestamp')
    ax[1][0].hlines(df.roll_deg.mean(),
                    xmin=0,
                    xmax=df.shape[0],
                    linestyles='dashed',
                    colors=['orangered'])

    # Pitch
    ax[1][1].plot(df.pitch_deg)
    ax[1][1].set_title('Pitch')
    ax[1][1].set_ylabel('Degrees')
    ax[1][1].set_xlabel('Timestamp')
    ax[1][1].hlines(df.pitch_deg.mean(),
                    xmin=0,
                    xmax=df.shape[0],
                    linestyles='dashed',
                    colors=['orangered'])

    fig.tight_layout()


def post_plot_1(df_new: pd.DataFrame) -> None:
    """
    Creates visualization for the first task

    Prameters
    ----------
    df_new: pd.DataFrame
        Dataframe with recalculated values
    """

    fig, ax = plt.subplots(3, 2, figsize=(12, 12))

    ax = ax.ravel()  # type: ignore

    # ax 0
    ax[0].scatter(df_new.x_mm,
                  df_new.y_mm,
                  s=10)
    ax[0].scatter(df_new.adj_x,
                  df_new.adj_y,
                  c='r',
                  s=10)

    for i in range(len(df_new.time_s)):
        ax[0].arrow(df_new.x_mm[i],
                    df_new.y_mm[i],
                    (df_new.adj_x[i]-df_new.x_mm[i]),
                    (df_new.adj_y[i]-df_new.y_mm[i]),
                    width=10,
                    head_width=30)

    for i in range(len(df_new)):
        ax[0].text(df_new.iloc[i]['x_mm'] + 30,
                   df_new.iloc[i]['y_mm'],
                   f"pitch: {df_new.iloc[i]['pitch_deg']}, roll: {df_new.iloc[i]['roll_deg']}", fontsize=7)

    ax[0].set_xlim([6250, 10200])
    ax[0].set_ylim([-35700, -31750])
    ax[0].set_title('Correction')
    ax[0].set_xlabel('x')
    ax[0].set_ylabel('y')

    # ax 1
    ax[1].scatter(df_new.x_mm,
                  df_new.y_mm,
                  s=30)
    ax[1].scatter(df_new.adj_x,
                  df_new.adj_y,
                  c='r',
                  s=30)
    ax[1].plot(df_new.iloc[[0, -1]].x_mm,
               df_new.iloc[[0, -1]].y_mm,
               c='orangered',
               linewidth=1)
    ax[1].plot(df_new.iloc[[0, -1]].adj_x,
               df_new.iloc[[0, -1]].adj_y,
               c='royalblue',
               linewidth=1)

    for i in range(len(df_new.time_s)):
        ax[1].arrow(df_new.x_mm[i],
                    df_new.y_mm[i],
                    (df_new.adj_x[i]-df_new.x_mm[i]),
                    (df_new.adj_y[i]-df_new.y_mm[i]),
                    width=5,
                    head_width=10)

    ax[1].set_xlim([8500, 9500])
    ax[1].set_ylim([-35000, -34000])
    ax[1].set_title('Correction zoomed')
    ax[1].set_xlabel('x')
    ax[1].set_ylabel('y')

    # ax 2 - 5
    x_shift = []
    y_shift = []
    for i in range(len(df_new)):
        x_shift.append(df_new['shift'][i][0])
        y_shift.append(df_new['shift'][i][1])

    ax[2].plot(x_shift)
    ax[2].set_title('Shift along x-axis')
    ax[2].set_xlabel('Timestamp')
    ax[2].set_xlabel('mm')

    ax[3].plot(df_new['pitch_deg'])
    ax[3].set_title('Pitch')
    ax[3].set_xlabel('Timestamp')
    ax[3].set_xlabel('Degrees')

    ax[4].plot(y_shift)
    ax[4].set_title('Shift along y-axis')
    ax[4].set_xlabel('Timestamp')
    ax[4].set_xlabel('mm')

    ax[5].plot(df_new['roll_deg'])
    ax[5].set_title('Roll')
    ax[5].set_xlabel('Timestamp')
    ax[5].set_xlabel('Degrees')

    fig.tight_layout()


def post_plot_2(df_new: pd.DataFrame, angles: list[float]) -> None:
    """
    Creates visualization for the second task

    Patameters
    ----------
    df_new: pd.DataFrame
        Dataframe with recalculated values

    angles: list[float]
        Angles between x and x'
    """

    x_mm = df_new.adj_x
    y_mm = df_new.adj_y
    # calculate headings
    dx = np.diff(x_mm)
    dy = np.diff(y_mm)
    headings = np.arctan2(dy, dx)
    # plot points and headings as lines with arrows
    fig, ax = plt.subplots(2, 1, figsize=(8, 12))
    ax[0].scatter(x_mm, y_mm, c='orangered', s=30)
    for i in range(len(headings)):
        x_start = x_mm[i]
        y_start = y_mm[i]
        x_end = x_start + 50*np.cos(headings[i])
        y_end = y_start + 50*np.sin(headings[i])
        ax[0].arrow(x_start,
                    y_start,
                    x_end-x_start,
                    y_end-y_start,
                    head_width=50,
                    head_length=50,
                    width=10,
                    fc='royalblue',
                    ec='royalblue')

    ax[0].set_xlim(6250, 10200)
    ax[0].set_ylim(-35700, -31750)

    ax[0].set_title('Vehicle heading')
    ax[0].set_xlabel('x')
    ax[0].set_ylabel('y')

    ax[1].plot(angles)
    ax[1].set_title("Vehicle heading (angle between $x$ and $x'$)")
    ax[1].set_xlabel('Timestamp')
    ax[1].set_ylabel('Angle(degrees)')

    fig.tight_layout()
