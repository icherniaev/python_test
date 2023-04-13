from dataclasses import dataclass, field
import pandas as pd


@dataclass
class DataSet:
    """
    Data class to store the data recieved on the fly and calculated

    Attributes
    ---------
    time_s: list
        List of timestamps

    x_mm: list
        List of x coordinates

    y_mm: list
        List of y coordinates

    roll_deg: list
        List of degrees of roll

    pitch_def: list
        List if degrees of pitch

    angle: list[tuple]
        list of tuple with rotation angles. 0: angle of x-axis,
        1: angle of y-axis

    shift: list[tuple]
        list of shifts. 0: along x-axis, 1: along y-axis

    adj_x: list
        list of corrected values of x coordinate
    adj_y: list
        list of corrected values of y coordinate

    Methods
    ----------
    add_data(time_s: float,
                x_mm: float,
                y_mm: float,
                roll_deg: float,
                pitch_deg: float,
                angle:tuple = (),
                shift:tuple = (),
                adj_x: float = 0,
                adj_y: float = 0)
        Adds data to the dataset
    """

    time_s: list[float] = field(default_factory=list)
    x_mm: list[float] = field(default_factory=list)
    y_mm: list[float] = field(default_factory=list)
    roll_deg: list[float] = field(default_factory=list)
    pitch_deg: list[float] = field(default_factory=list)

    angle: list[tuple] = field(default_factory=list)
    shift: list[tuple] = field(default_factory=list)
    adj_x: list[float] = field(default_factory=list)
    adj_y: list[float] = field(default_factory=list)

    def add_data(self,
                 time_s: float,
                 x_mm: float,
                 y_mm: float,
                 roll_deg: float,
                 pitch_deg: float,
                 angle: tuple = (),
                 shift: tuple = (),
                 adj_x: float = 0,
                 adj_y: float = 0) -> None:
        """
        Adds data to the dataset

        Parameters
        ----------
        time_s: float
            Timestamp

        x_mm: float
            x coordinate

        y_mm: float
            y-coordinate

        roll_deg: float
            degree of roll

        pitch_deg: float
            degree of pitch

        angle: tuple
            angles between x and x', y'

        shift: tuple
            shifts along x' and y' axes

        adj_x: float
            adjusted values of x

        adj_y: float
            adjusted value of y
        """

        self.time_s.append(time_s)
        self.x_mm.append(x_mm)
        self.y_mm.append(y_mm)
        self.roll_deg.append(roll_deg)
        self.pitch_deg.append(pitch_deg)

        self.angle.append(angle)
        self.shift.append(shift)
        self.adj_x.append(adj_x)
        self.adj_y.append(adj_y)


def make_new_df(dataset: DataSet) -> pd.DataFrame:
    """
    Creates new pandas dataframe from an instance of class DataSet

    Parameters
    ----------
    dataset: DataSet object
        Dataset with calculated values after transformation

    Returns
    ----------
    df_new: pandas.DataFrame
        Dataframe with values from dataset
    """

    df_new = pd.DataFrame(data={'time_s': dataset.time_s,
                                'x_mm': dataset.x_mm,
                                'y_mm': dataset.y_mm,
                                'roll_deg': dataset.roll_deg,
                                'pitch_deg': dataset.pitch_deg,
                                'angle': dataset.angle,
                                'shift': dataset.shift,
                                'adj_x': dataset.adj_x,
                                'adj_y': dataset.adj_y})

    return df_new


def extract_angles(dataset: DataSet) -> list:
    """
    Extract angles of rotation between x-axis of global reference frame
    and x-axis of local reference frame
    """

    angles = []

    for angle in dataset.angle:
        angles.append(angle[0])

    return angles
