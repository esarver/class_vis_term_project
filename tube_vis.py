#!/usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import math
import pandas as pd
from typing import List, Tuple, Union, Optional, Generator


class Tube:
    """
    Representation of the measurements taken on a tube.
    """

    def __init__(self, row: int, assembly: int, ideal_value: float, left: Optional[float], center: Optional[float],
                 right: Optional[float]):
        """
        Construct a new tube with the given parameters
        :param row: The row where the tube is found
        :param assembly: The assembly in which the tube is found
        :param ideal_value: the "ideal" wall thickness for this tube
        :param left: the measured thickness of the tube wall on the left side of the tube (if facing the tube from the
                     hot-side)
        :param center: the measured thickness of the tube wall on the side of the tube facing the hot-side.
        :param right: the measured thickness of the tube wall on the right side of the tube (if facing the tube from the
                      hot-side)
        """
        self.left = ideal_value - left
        self.center = ideal_value - center
        self.right = ideal_value - right
        self.row = row
        self.assembly = assembly


class Frh:
    """
    The Frh is the Final ReHeater. It contains all the tubes that are to be visualized.
    """

    def __init__(self, num_assemblies: int, num_rows: int, sub_grid: int = 3, margin: int = 1):
        """
        Construct a Final ReHeater object
        :param num_assemblies: The number of assemblies the Final ReHeater has
        :param num_rows: The number of tubes each assembly contains
        :param sub_grid: The number of cells a tube should be represented by (value is one side of a square)
        :param margin: The number of cells around each tube
        """
        self.num_assemblies = num_assemblies
        self.num_rows = num_rows
        self.sub_grid = sub_grid
        self.margin = margin
        self.fac = sub_grid + 2 * margin
        self.assembly_ticks: List[int] = list(range(self.num_assemblies))
        self.assembly_map: List[int] = list(range(int(math.floor(self.fac / 2)),
                                                  int((self.fac * self.num_assemblies) - math.floor(self.fac / 2)),
                                                  int(self.fac)))
        self.row_ticks: List[int] = list(range(self.num_rows))
        self.row_map: List[int] = list(range(int(math.floor(self.fac / 2)),
                                             int((self.fac * self.num_rows) - math.floor(self.fac / 2)),
                                             int(self.fac)))
        self.grid = np.zeros((num_rows * self.fac, num_assemblies * self.fac))
        for i in range(num_rows):
            for j in range(num_assemblies):
                self.grid[i * self.fac] = np.zeros((num_assemblies * self.fac))
                self.grid[(i * self.fac) + (self.fac - 1)] = np.zeros((num_assemblies * self.fac))
                for s in range(sub_grid):
                    self.grid[(i * self.fac) + margin + s][(j * self.fac)] = 0
                    self.grid[(i * self.fac) + margin + s][(j * self.fac) + (self.fac - 1)] = 0

    def add_tube(self, tube: Tube) -> None:
        """
        Add a tube to the Final ReHeater.

        :param tube: The tube to add
        :return: None
        """
        if tube.left:
            self.grid[self.row_map[tube.row]][self.assembly_map[tube.assembly] + 1] = tube.left
            self.grid[self.row_map[tube.row] - 1][self.assembly_map[tube.assembly] + 1] = tube.left
            self.grid[self.row_map[tube.row] + 1][self.assembly_map[tube.assembly] + 1] = tube.left

        if tube.right:
            self.grid[self.row_map[tube.row]][self.assembly_map[tube.assembly] - 1] = tube.right
            self.grid[self.row_map[tube.row] - 1][self.assembly_map[tube.assembly] - 1] = tube.right
            self.grid[self.row_map[tube.row] + 1][self.assembly_map[tube.assembly] - 1] = tube.right

        if tube.center:
            self.grid[self.row_map[tube.row] - 1][self.assembly_map[tube.assembly]] = tube.center
            self.grid[self.row_map[tube.row] - 1][self.assembly_map[tube.assembly] - 1] = tube.center
            self.grid[self.row_map[tube.row] - 1][self.assembly_map[tube.assembly] + 1] = tube.center

    def show(self) -> None:
        """
        Configure and plot the visual representation of the Final ReHeater

        :return: None
        """
        fig, ax = plt.subplots()
        plt.yticks(self.row_map, [x + 1 for x in self.row_ticks])
        plt.xticks(self.assembly_map, [x + 1 for x in self.assembly_ticks])
        image = ax.imshow(self.grid, interpolation='none', cmap='afmhot')
        plt.title('Hot Side', color='red')
        plt.xlabel("Assemblies")
        plt.ylabel("Rows")
        fig.colorbar(image, ax=ax, orientation='horizontal', fraction=0.1)
        plt.gcf().canvas.set_window_title("Tube Wall Degradation Visualizer for Final Re-Heater")
        plt.tight_layout()

        for row in self.row_ticks:
            for assembly in self.assembly_ticks:
                rect = patches.Rectangle((self.assembly_map[assembly] - 1.5, self.row_map[row] - 1.5),
                                         width=self.sub_grid, height=self.sub_grid, fill=False)
                rect.set_color('grey')
                ax.add_patch(rect)

        plt.show()


def read_file(file_path: str, sheet_name: str, year: int, label: str, ideal_value: float) -> Generator[
    Tube, None, None]:
    """
    Read the given sheet in an excel file. The file must be formatted in a database style with one entry per tube.

    :param ideal_value: The ideal value for each tube
    :param file_path: The path the the Excel file
    :param sheet_name: The name of the sheet in which the data is an acceptable format
    :param year: The year the data points were taken
    :param label: the label associated with the data points.
    :return: A list of tubes created from the data
    """
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    df = df[(df.Year == year) & (df.Label == label)]  # filter to only required values

    for _, tube in df.iterrows():
        row = (tube.Row - 1)
        assembly = (tube.Assembly - 1)
        left = tube.Left if pd.notna(tube.Left) else ideal_value
        center = tube.Center if pd.notna(tube.Center) else ideal_value
        right = tube.Right if pd.notna(tube.Right) else ideal_value
        yield Tube(row=row, assembly=assembly, left=left, center=center,
                   right=right, ideal_value=ideal_value)


def main(file_info: Tuple[str, str, int, str], ideal_value: float, num_assemblies: int, num_rows: int) -> None:
    """
    Run the application
    :return: None
    """
    ideal_value = ideal_value
    frh = Frh(num_assemblies=num_assemblies, num_rows=num_rows)
    for tube in read_file(*file_info, ideal_value=ideal_value):
        frh.add_tube(tube)

    frh.show()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="The Excel file to open", type=str)
    parser.add_argument("sheet", help="The sheet in the Excel file that contains a DB-style record", type=str)
    parser.add_argument("year", help="The year the data was taken", type=int)
    parser.add_argument("label", help="The label of the data", type=str)
    parser.add_argument("ideal_value", help="The ideal value for the data", type=float)
    parser.add_argument("num_assemblies", help="The number of assemblies.", type=int)
    parser.add_argument("num_rows", help="The number of rows in each assembly", type=int)
    args = parser.parse_args()

    main((args.file, args.sheet, args.year, args.label), ideal_value=args.ideal_value,
         num_assemblies=args.num_assemblies, num_rows=args.num_rows)
