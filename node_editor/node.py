from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt

from .pin import Pin
from .gui.node_graphics import Node_Graphics
from .common import Node_Status


class Node(Node_Graphics):
    def __init__(self):
        super().__init__()
        self.uuid = None  # An identifier that used to saving and loading scene
        self.value = None  # An input value that has been set by the user

    def init_widget(self):
        """ Initialize the node widget [Your_node.py]."""
        pass

    def compute(self):
        raise NotImplementedError("compute is not implemented")

    def execute(self):
        # Get the values from the input pins
        self.execute_inputs()

        # Compute the value
        self.compute()

        # execute nodes connected to output
        self.execute_outputs()

    def execute_inputs(self):
        pass

    def execute_outputs(self):
        pass

    def delete(self):
        """Deletes the connection.

        This function removes any connected pins by calling :any:`Port.remove_connection` for each pin
        connected to this connection. After all connections have been removed, the stored :any:`Port`
        references are set to None. Finally, :any:`QGraphicsScene.removeItem` is called on the scene to
        remove this widget.

        Returns:
            None
        """

        to_delete = [pin.connection for pin in self._pins if pin.connection]
        for connection in to_delete:
            connection.delete()

        self.scene().removeItem(self)

    def get_pin(self, name):
        for pin in self._pins:
            if pin.name == name:
                return pin

    def add_pin(self, name, is_output=False, execution=False):
        pin = Pin(self, node=self, name=name, is_output=is_output, execution=execution)
        self._pins.append(pin)

    def select_connections(self, value):
        """
        Sets the highlighting of all connected pins to the specified value.

        This method takes a boolean value `value` as input and sets the `_do_highlight` attribute of all connected pins
        to this value. If a pin is not connected, this method does nothing for that pin. After setting the
        `_do_highlight` attribute for all connected pins, the `update_path` method is called for each connection.

        Args:
            value: A boolean value indicating whether to highlight the connected pins or not.

        Returns:
            None.
        """

        for pin in self._pins:
            if pin.connection:
                pin.connection._do_highlight = value
                pin.connection.update_path()
