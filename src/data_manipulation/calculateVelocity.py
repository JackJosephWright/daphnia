import numpy as np
import pandas as pd

def calculateVelocity(pi: pd.DataFrame, pf: pd.DataFrame) -> float:
    """
    Calculates the velocity between two points.
    
    Parameters:
    -----------
    pi : DataFrame
        The initial point of the entity, given as a section of a pandas DataFrame.
    pf : DataFrame
        The final position of the entity, given as a section of a pandas DataFrame.

    Returns:
    --------
    float
        The calculated velocity.
    """
    dx = pf["X"] - pi["X"]
    dy = pf["Y"] - pi["Y"]

    displacement = np.sqrt(dx**2 + dy**2)

    dtime = pf["time"] - pi["time"]

    velocity = displacement / dtime
    
    return velocity