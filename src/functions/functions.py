import numpy as np
import pandas as pd
from src.data.make_dataset import DataSet


def calc_rot_angle(x0: float,
                   y0: float,
                   x1: float,
                   y1: float) -> tuple[float, float]:
    """
    Calculates rotation angle to switch to vehicle local reference frame

    Parameters
    ----------
    x0, y0: float
        Coordinates of the point at time t-1

    x1, y1: float
        Coordinates of the point at time t

    Returns
    ----------
    alpha_x: float
        Angle of rotation to switch from global to local reference frame

    alpha_ y: float
    """

    y_delta = y1-y0
    x_delta = x1-x0
    alpha_x = np.arctan2(y_delta, x_delta)
    alpha_y = alpha_x + np.deg2rad(90)
    return alpha_x, alpha_y


def caluclate_shifts(roll_deg: float,
                     pitch_deg: float,
                     height: float = 1500) -> tuple[float, float]:
    """
    Calculates values and directions of shifts along the axes of vehicle
    local reference frame for tilt compensation.

    Parameters
    ----------
    roll_deg: float
        Tilt along y-axis of the vehicle local reference frame in degrees.
        Positive roll corresponds to the orientation when the right side of
        the vehicle is being lower than the left side.

    pitch_deg: float
        Tilt along x-axis of the vehicle local reference frame in degrees.
        Positive pitch corresponds to the orientation when the front part of
        the vehicle is being lower than the rear part.

    height: float
        Height of GNSS module installation in mm.

    Returns
    ----------
    x_shift: float
        shift along x-axis of local frame in mm.

    y_shift: float
        shift along y-axis of local frame in mm.
    """

    y_shift = np.abs(height * np.sin(np.deg2rad(roll_deg)))
    height_adjusted = np.abs(height * np.cos(np.deg2rad(roll_deg)))
    x_shift = np.abs(height_adjusted * np.sin(np.deg2rad(pitch_deg)))
    return x_shift, y_shift


def calculate_backroll(roll_deg: float, height: float = 1500) -> float:
    """
    Calculates shift along y-axis in the backward direction
    """

    y_shift = -np.abs(height * np.sin(np.deg2rad(roll_deg)))

    return y_shift


def apply_shifts(x: float,
                 y: float,
                 alpha_x: float,
                 alpha_y: float,
                 shift_x: float = 0,
                 shift_y: float = 0) -> tuple[float, float]:
    """
    Shifts point of xy-plane along local reference frame
    of the vehicle for tils compensation

    Parameters
    ----------
    x, y: float
        Coordinates of the point in global reference frame

    alpha_x, alpha_y: float
        Angles of rotation to switch from global to local reference frames

    shift_x, shift_y:
        Shifts along axis of local reference frame for tilt compensation
        Default: 0

    Retruns
    ----------
    x_adj, y_adj: float
        Coordinates of the point adjusted for tilt
    """

    # Shift along x-axis of local reference frame
    x = x + np.cos(alpha_x) * shift_x
    y = y + np.sin(alpha_x) * shift_x

    # Shft along y-axis of local reference frame
    x_adj = x + np.cos(alpha_y) * shift_y
    y_adj = y + np.sin(alpha_y) * shift_y

    return x_adj, y_adj


def add_zero_element(df: pd.DataFrame,
                     dataset: DataSet,
                     i: int) -> None:
    """
    Adds zero element to the dataset wihtout corections

    Parameters
    ----------
    df: pd.DataFrame
        Initial pandas DataFrame

    dataset: DataSet
        Instance of class DataSet where the data will be stored

    i: int
        The step of iteration
    """

    curr_row = df.iloc[i]
    shift_x, shift_y = caluclate_shifts(curr_row['roll_deg'],
                                        curr_row['pitch_deg'])
    dataset.add_data(*curr_row[:5],
                     shift=(shift_x, shift_y))


def add_first_element(df: pd.DataFrame,
                      dataset: DataSet,
                      i: int) -> None:
    """
    Adds first elements to the dataset
    Makes correction for zero and first elements

    Parameters
    ----------
    df: pd.DataFrame
        Initial pandas DataFrame

    dataset: DataSet
        Instance of class DataSet where the data will be stored

    i: int
        The step of iteration
    """

    prev_row = df.iloc[i-1]
    curr_row = df.iloc[i]
    # Calculate the angle between two points
    alpha_x, alpha_y = calc_rot_angle(prev_row.x_mm,
                                      prev_row.y_mm,
                                      curr_row.x_mm,
                                      curr_row.y_mm)
    # Calculate the shift for current row
    shift_x, shift_y = caluclate_shifts(curr_row.roll_deg,
                                        curr_row.pitch_deg)
    # Apply shift to current row
    x_adj, y_adj = apply_shifts(curr_row.x_mm,
                                curr_row.y_mm,
                                alpha_x, alpha_y,
                                shift_x, shift_y)
    # Record the results for current row
    dataset.add_data(*curr_row[:5],
                     angle=(alpha_x, alpha_y),
                     shift=(shift_x, shift_y),
                     adj_x=x_adj,
                     adj_y=y_adj)
    # Apply shift to previous row
    x_adj_prev, y_adj_prev = apply_shifts(prev_row.x_mm, prev_row.y_mm,
                                          alpha_x, alpha_y,
                                          dataset.shift[i-1][0],
                                          dataset.shift[i-1][1])
    # Recond the results for the previous row
    dataset.angle[i-1] = (alpha_x, alpha_y)
    dataset.adj_x[i-1] = x_adj_prev
    dataset.adj_y[i-1] = y_adj_prev


def recalc_prev_elements(df: pd.DataFrame,
                         dataset: DataSet,
                         correct_alpha_x: float,
                         correct_alpha_y: float,
                         i: int) -> None:
    """
    Recalualtes position for the previous points

    Parameters
    ----------
    df: pd.DataFrame
        Initial pandas DataFrame

    dataset: DataSet
        Instance of class DataSet where the data will be stored

    correct_alpha_x: float
        Correct angle of rotation for x-axis between two points with same roll

    correct_alpha_y: float
        Correct angle of rotation for y-axis between two points with same roll

    i: int
        The step of iteration
    """

    alpha_x, alpha_y = correct_alpha_x, correct_alpha_y

    for j in reversed(range(1, i)):
        prev_row = df.iloc[j-1]
        curr_row = df.iloc[j]
        # Get the shifts
        shift_x, shift_y = dataset.shift[j][0], dataset.shift[j][1]
        # Apply shifts with new roll
        x_adj, y_adj = apply_shifts(curr_row.x_mm,
                                    curr_row.y_mm,
                                    alpha_x,
                                    alpha_y,
                                    shift_x,
                                    shift_y)
        # Update the position
        dataset.adj_x[j], dataset.adj_y[j] = x_adj, y_adj
        # Update the angles for the current point in the dataframe
        # Those are the angles between current and next points
        dataset.angle[j] = (alpha_x, alpha_y)
        # Make a rollback (take roll from previous point)
        y_shift = calculate_backroll(dataset.roll_deg[j-1])
        x_curr_adj, y_curr_adj = apply_shifts(dataset.adj_x[j],
                                              dataset.adj_y[j],
                                              alpha_x=dataset.angle[j][0],
                                              alpha_y=dataset.angle[j][1],
                                              shift_y=y_shift)
        # Calculate the angle between current and previous point
        alpha_x, alpha_y = calc_rot_angle(prev_row.x_mm,
                                          prev_row.y_mm,
                                          x_curr_adj,
                                          y_curr_adj)
    # Update separately for t=0
    # Update the angle
    dataset.angle[0] = (alpha_x, alpha_y)  # type: ignore
    # Shift the points along that angle
    x_adj, y_adj = apply_shifts(dataset.x_mm[0],
                                dataset.y_mm[0],
                                dataset.angle[0][0],
                                dataset.angle[0][1],
                                dataset.shift[0][0],
                                dataset.shift[0][1])
    # Record adjusted points
    dataset.adj_x[0], dataset.adj_y[0] = x_adj, y_adj


def correct_point(df: pd.DataFrame,
                  dataset: DataSet,
                  i: int,
                  flag: bool,
                  recalc=True) -> bool:
    """
    Calculates the angle between previous point (adjusted to the same roll
    as current) and current point

    Corrects coordintes of the current point

    If two points with same roll_deg are encountered,
    calculates the correct position of local reference frame

    Parameters
    ----------
    df: pd.DataFrame
        Initial pandas DataFrame

    dataset: DataSet
        Instance of class DataSet where the data will be stored

    i: int
        The step of iteration

    flag: bool
        flag = True if the points with the same roll have not yet
        been encountered, False otherwise

    recalc: bool, default = True
        recalculate previous points' coordinates after
        encountering points with the same roll

    Returns
    ----------
    flag: bool
        flag = True if the points with the same roll
        have not yet been encountered, False otherwise
    """

    prev_row = df.iloc[i-1]
    curr_row = df.iloc[i]

    if (curr_row.roll_deg == prev_row.roll_deg) & (flag):
        # Calculate correct angle
        alpha_x, alpha_y = calc_rot_angle(prev_row.x_mm,
                                          prev_row.y_mm,
                                          curr_row.x_mm,
                                          curr_row.y_mm)

        # Update the points for current row
        shift_x, shift_y = caluclate_shifts(curr_row.roll_deg,
                                            curr_row.pitch_deg)
        x_adj, y_adj = apply_shifts(curr_row.x_mm,
                                    curr_row.y_mm,
                                    alpha_x,
                                    alpha_y,
                                    shift_x,
                                    shift_y)
        dataset.add_data(*curr_row[:5],
                         angle=(alpha_x, alpha_y),
                         shift=(shift_x, shift_y),
                         adj_x=x_adj,
                         adj_y=y_adj)

        if recalc:
            recalc_prev_elements(df, dataset, alpha_x, alpha_y, i)
        flag = False

    else:
        # Get unrolled previous point
        y_shift = calculate_backroll(curr_row.roll_deg)
        x_prev_adj, y_prev_adj = apply_shifts(dataset.adj_x[i-1],
                                              dataset.adj_y[i-1],
                                              alpha_x=dataset.angle[i-1][0],
                                              alpha_y=dataset.angle[i-1][1],
                                              shift_y=y_shift)
        # Calculate angle
        alpha_x, alpha_y = calc_rot_angle(x_prev_adj,
                                          y_prev_adj,
                                          curr_row.x_mm,
                                          curr_row.y_mm)
        # Calculate the shift
        shift_x, shift_y = caluclate_shifts(curr_row.roll_deg,
                                            curr_row.pitch_deg)
        # Make the shift
        x_adj, y_adj = apply_shifts(curr_row.x_mm,
                                    curr_row.y_mm,
                                    alpha_x,
                                    alpha_y,
                                    shift_x,
                                    shift_y)
        # Record the changes
        dataset.add_data(*curr_row[:5],
                         angle=(alpha_x, alpha_y),
                         shift=(shift_x, shift_y),
                         adj_x=x_adj,
                         adj_y=y_adj)

    return flag


def transfrom(df: pd.DataFrame,
              dataset: DataSet,
              recalc: bool = True) -> None:
    """
    Iterates over the whole dataset imitating real time retrieval of data
    Updates points coordinates and calculates angles on the fly

    Parameters
    ----------

    df: pd.DataFrame
        Initial pandas DataFrame

    dataset: DataSet
        Instance of class DataSet where the data will be stored
    """

    flag = True

    for i in range(len(df)):
        if i == 0:
            add_zero_element(df, dataset, i)
        if i == 1:
            add_first_element(df, dataset, i)
        if i not in [0, 1]:
            flag = correct_point(df, dataset, i, flag, recalc=recalc)
