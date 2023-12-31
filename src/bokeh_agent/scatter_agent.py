import pandas as pd
from bokeh import models as models
from bokeh.models import CategoricalColorMapper, ColumnDataSource
from bokeh.palettes import (
    Category10,
    Cividis,
    Dark2,
    Inferno,
    Magma,
    Palette,
    Plasma,
    Turbo,
    Viridis,
)
from bokeh.plotting import figure, output_file, show


class BokehScatterAgent():
    """
    A class for creating bokeh scatter plot

    ...

    Attributes
    ----------
    data : pandas.DataFrame
        data to be plotted
    params : dict
        a dictionary of bokeh parameters
    tooltips : list
        list of tooltips for the scatter plot
    color_factors : list[str]
        list of values to be used for colorization of the plot

    Methods
    -------
    set_data(dataframe: pandas.DataFrame):
        Sets the plot data
    set_params(params: dict):
        Sets the bokeh parameters
    set_tooltips(tooltips: list):
        Sets the bokeh plot tooltips
    set_color_factors(color_factors: list):
        Sets the plot color factors
    display_plot():
        Displays the plot in the default browser
    """

    def __init__(self, data: pd.DataFrame = None, params: dict = None, tooltips: list = None, color_factors: list[str] = None):
        self.data = data
        self.params = params
        self.tooltips = tooltips
        self.color_factors = color_factors
        self.figure = None

    def _get_palette(self, palette_name: str) -> Palette:
        '''
        Returns a bokeh palette, corresponding to a given str palette name
        '''

        # Magma, Inferno, Plasma, Viridis, Cividis, Turbo
        if palette_name == 'Magma':
            return Magma
        elif palette_name == 'Inferno':
            return Inferno
        elif palette_name == 'Plasma':
            return Plasma
        elif palette_name == 'Viridis':
            return Viridis
        elif palette_name == 'Cividis':
            return Cividis
        elif palette_name == 'Turbo':
            return Turbo
        elif palette_name == 'Category10':
            return Category10
        elif palette_name == 'Dark2':
            return Dark2
        else:
            return Turbo

    def _create_graph(self):
        x_value = self.params['x_axis']
        y_value = self.params['y_axis']
        palette = self._get_palette(self.params['palette'])
        graph_point_size = self.params['point_size']
        color_mapper = CategoricalColorMapper(
            factors=self.color_factors, palette=palette[11])
        data = ColumnDataSource(data=self.data)

        self.figure.scatter(source=data, x=x_value, y=y_value, color={
                            'field': 'color_bucket', 'transform': color_mapper}, size=graph_point_size)
        hover = models.HoverTool(tooltips=self.tooltips)
        self.figure.add_tools(hover)

    def generate(self) -> None:
        '''
        Returns a figure with the provided parameters
        '''
        if self.data.empty == True:
            raise Exception('Dataframe not set')
        if self.params == None:
            raise Exception('Graph params not set')
        if self.tooltips == None:
            raise Exception('Tooltips not set')
        if self.color_factors == None:
            raise Exception('Color factors not set')

        title = self.params['title']
        y_axis_label = self.params['y_axis_label']
        width = self.params['width']
        height = self.params['height']

        output_file_path = self.params['output_file_path'] if self.params['output_file_path'] != '' else 'main.html'
        output_file_title = self.params['output_file_title'] if self.params['output_file_title'] != '' else 'Bokeh Plot'
        output_file(filename=output_file_path, title=output_file_title)

        self.figure = figure(title=title, x_axis_label='number',
                             y_axis_label=y_axis_label, width=width, height=height)

        self._create_graph()

    def set_data(self, dataframe: pd.DataFrame):
        self.data = dataframe

    def set_params(self, params: dict):
        self.params = params

    def set_tooltips(self, tooltips: list):
        self.tooltips = tooltips

    def set_color_factors(self, color_factors: list):
        self.color_factors = color_factors

    def display_plot(self):
        show(self.figure)
