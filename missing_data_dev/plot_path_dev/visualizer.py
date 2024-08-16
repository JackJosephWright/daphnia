import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

class DaphniaAnimation:
    """ Animates the movement of a Daphnia using clean data from an NPZ file

        Functions:
        ----------
        __init__:
            Initializes the DaphniaAnimation class with the given NPZ file and start index
        load_data:
            Loads data from NPZ file into dataframes and removes missing data
        plot_detail:
            Sets the title and labels for the plot
        init_animation:
            Initializes the animation by setting the line data to empty
        animate:
            Updates the animation frame by frame
        create_animation:
            Creates and displays the animation of the Daphnia's movements

    """
    def __init__(self, npz_path, start_index=0):
        """ Initializes the DaphniaAnimation class with the given NPZ file and start index

        """
        self.npz_path = npz_path
        self.start_index = start_index
        self.df = self.load_data()
        self.df_subset = self.df.loc[self.start_index:]

        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], 'b-')

    def load_data(self):
        """ Loads data from NPZ file into dataframes and removes missing data

        """
        # Load the npz file
        data = np.load(self.npz_path)
        timestamp = data['timestamp']
        X = data['X']
        Y = -data['Y']  # Inverting Y

        df = pd.DataFrame(
            {
                "X": X,
                "Y": Y,
                "time": timestamp
            }
        )

        # Drop missing or infinite data
        df.replace(['', np.inf, -np.inf], np.nan, inplace=True)
        df.dropna(inplace=True)
        return df

    def plot_detail(self, title, xlabel, ylabel):
        """ Sets the title and labels for the plot
        
        """
        csfont = {'fontname': 'Comic Sans MS', 'color': 'blue', 'size': 20}
        hfont = {'fontname': 'Helvetica', 'color': 'blue', 'size': 12}
        plt.title(title, fontdict=csfont)
        plt.xlabel(xlabel, fontdict=hfont)
        plt.ylabel(ylabel, fontdict=hfont)

    def init_animation(self):
        """ Initializes the animation by setting the line data to empty

        """
        self.line.set_data([], [])
        return self.line,

    def animate(self, i):
        """ Updates the animation frame by frame
        
        """
        x = self.df_subset['X'][:i]
        y = self.df_subset['Y'][:i]
        self.line.set_data(x, y)
        return self.line,

    def create_animation(self):
        """ Creates and displays the animation of the Daphnia's movements
        
        """
        # Set up plot limits
        self.ax.set_xlim(self.df_subset['X'].min(), self.df_subset['X'].max())
        self.ax.set_ylim(self.df_subset['Y'].min(), self.df_subset['Y'].max())

        # Add plot details
        self.plot_detail("Single Fish Data", "X value", "Y value")

        # Call the animator
        ani = FuncAnimation(self.fig, self.animate, init_func=self.init_animation,frames=len(self.df_subset), interval=50, blit=True)

        plt.show()