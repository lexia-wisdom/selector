#!/usr/bin/env python
#   This file is part of nexdatas - Tango Server for NeXus data writer
#
#    Copyright (C) 2014-2016 DESY, Jan Kotanski <jkotan@mail.desy.de>
#
#    nexdatas is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    nexdatas is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with nexdatas.  If not, see <http://www.gnu.org/licenses/>.
## \package nxselector nexdatas
## \file InfoDlg.py
# info about tango servers

"""  info about tango servers """

try:
    from taurus.external.qt import Qt
except:
    from taurus.qt import Qt

from taurus.qt.qtgui.util.ui import UILoadable

import logging
logger = logging.getLogger(__name__)


@UILoadable(with_ui='ui')
class InfoDlg(Qt.QDialog):
    ## constructor
    # \param parent parent widget
    def __init__(self, parent=None):
        super(InfoDlg, self).__init__(parent)
        self.loadUi()
        self.state = None

    def createGUI(self):
        if self.state:
            self.ui.writerLabel.setText(self.state.writerDevice)
            self.ui.configLabel.setText(self.state.configDevice)
            self.ui.doorLabel.setText(self.state.door)
            self.ui.selectorLabel.setText(Qt.QString(
                self.state.server if self.state.server else 'module'))
