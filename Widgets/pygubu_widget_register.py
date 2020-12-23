"""
Module permettant de rendre disponible les Widgets de ce répertoire dans Pygudu
"""
from pygubu import BuilderObject, register_widget
from GraphWidget import MyGraphWidget
from VectorViewWidget import VectorView
from ConsoleViewWidget import ConsoleWidget


class GraphWidgetBuilder(BuilderObject):
    class_ = MyGraphWidget


register_widget('customwidgets.GraphWidget', GraphWidgetBuilder,
                'GraphWidget', ('tk', 'ttk', 'customwidgets'))


class VectorViewWidgetBuilder(BuilderObject):
    class_ = VectorView


register_widget('customwidgets.VectorWidget', VectorViewWidgetBuilder,
                'VectorView', ('tk', 'ttk', 'customwidgets'))


class ConsoleWidgetBuilder(BuilderObject):
    class_ = ConsoleWidget


register_widget('customwidgets.ConsoleWidget', ConsoleWidgetBuilder,
                'ConsoleWidget', ('tk', 'ttk', 'customwidgets'))
