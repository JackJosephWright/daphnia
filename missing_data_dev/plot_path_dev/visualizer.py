import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

class DaphniaAnimation:
    """ 
    Animates the movement of a Daphnia using clean data from an NPZ file

    Functions:
    ----------
    __init__:
        Initializes the DaphniaAnimation class with the given NPZ file and start index
    load_data:
        Loads data from NPZ file into dataframes and removes missing data if needed
    plot_detail:
        Sets the title and labels for the plot
    init_animation:
        Initializes the animation by setting the line data to empty
    animate:
        Updates the animation frame by frame
    create_animation:
        Creates and displays the animation of the Daphnia's movements
    """
    def __init__(self, df, start_index=0):
        """ 
        Initializes the DaphniaAnimation class with the given NPZ file and start index

        Parameters:
        -----------
        npz_path: str/source_dir
            Clean npz file to be used for animation 
        start_index: int, optional
            Index declaring what frame you want the animation to start (default is 0)
        """
        self.df = df
        self.start_index = start_index
        self.df_subset = self.df.iloc[self.start_index:]

        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], 'b-')

    def plot_detail(self, title, xlabel, ylabel):
        """ 
        Sets the title and labels for the plot

        Parameters:
        -----------
        title: str
            Title of the plot
        xlabel: str
            The label for the X-axis
        ylabel: str
            The label for the Y-axis
        """
        csfont = {'fontname': 'Comic Sans MS', 'color': 'blue', 'size': 20}
        hfont = {'fontname': 'Helvetica', 'color': 'blue', 'size': 12}
        plt.title(title, fontdict=csfont)
        plt.xlabel(xlabel, fontdict=hfont)
        plt.ylabel(ylabel, fontdict=hfont)

    def init_animation(self):
        """ 
        Initializes the animation by setting the line data to empty

        Returns:
        --------
        A tuple containing the line object to be animated
        """
        self.line.set_data([], [])
        return self.line,

    def animate(self, i):
        """ 
        Updates the animation frame by frame

        Parameters:
        -----------
        i: int
            The current frame index
        """
        x = self.df_subset['X'].iloc[:i]
        y = self.df_subset['Y'].iloc[:i]
        self.line.set_data(x, y)
        return self.line,

    def create_animation(self):
        """ 
        Creates and displays the animation of the Daphnia's movements

        The function sets up the plot, removes missing data if needed, adds plot details, and then runs the animation
        """
            # Ensure there are no NaN or Inf values in the columns used for limits
        valid_x = self.df_subset['X'].replace([np.inf, -np.inf], np.nan).dropna()
        valid_y = self.df_subset['Y'].replace([np.inf, -np.inf], np.nan).dropna()

        if valid_x.empty or valid_y.empty:
            raise ValueError("No valid data points available to set axis limits.")

        # Set up plot limits using the cleaned data
        self.ax.set_xlim(valid_x.min(), valid_x.max())
        self.ax.set_ylim(valid_y.min(), valid_y.max())

        # Add plot details
        self.plot_detail("Single Fish Data", "X value", "Y value")

        # Call the animator
        ani = FuncAnimation(self.fig, self.animate, init_func=self.init_animation,frames=len(self.df_subset), interval=50, blit=True)

        plt.show()