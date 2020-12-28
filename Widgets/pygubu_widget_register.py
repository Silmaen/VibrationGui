# encoding: utf8
"""
Module permettant de rendre disponible les Widgets de ce répertoire dans Pygudu
"""
from pygubu import BuilderObject, register_widget
from GraphWidget import MyGraphWidget
from VectorViewWidget import VectorView
from ConsoleViewWidget import ConsoleWidget
from TemporalView import AffichageTemporel
from ControlFrame import ControlFrameWidget


# ------------ graph widget ---------------------
class GraphWidgetBuilder(BuilderObject):
    class_ = MyGraphWidget


register_widget('customwidgets.GraphWidget', GraphWidgetBuilder,
                'GraphWidget', ('tk', 'ttk', 'customwidgets'))


# ------------ vector widget ---------------------
class VectorViewWidgetBuilder(BuilderObject):
    class_ = VectorView


register_widget('customwidgets.VectorWidget', VectorViewWidgetBuilder,
                'VectorView', ('tk', 'ttk', 'customwidgets'))


# ------------ console widget ---------------------
class ConsoleWidgetBuilder(BuilderObject):
    class_ = ConsoleWidget


register_widget('customwidgets.ConsoleWidget', ConsoleWidgetBuilder,
                'ConsoleWidget', ('tk', 'ttk', 'customwidgets'))


# ------------ temporal widget ---------------------
class AffichageTemporelBuilder(BuilderObject):
    class_ = AffichageTemporel


register_widget('customwidgets.AffichageTemporel', AffichageTemporelBuilder,
                'AffichageTemporel', ('tk', 'ttk', 'customwidgets'))


# ------------ Controlframe widget ---------------------
class ControlframeBuilder(BuilderObject):
    class_ = ControlFrameWidget


register_widget('customwidgets.Controlframe', ControlframeBuilder,
                'Controlframe', ('tk', 'ttk', 'customwidgets'))
