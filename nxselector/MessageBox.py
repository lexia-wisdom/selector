#!/usr/bin/env python
#   This file is part of nexdatas - Tango Server for NeXus data writer
#
#    Copyright (C) 2014 DESY, Jan Kotanski <jkotan@mail.desy.de>
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
## \file MessageBox.py
# error message box

""" error message box """

import sys
import logging
import PyTango
logger = logging.getLogger(__name__)

try:
    from taurus.external.qt import Qt
except:
    from taurus.qt import Qt


class MessageBox(Qt.QObject):
    def __init__(self, parent):
        Qt.QObject.__init__(self, parent)

    @classmethod
    def getText(cls, default, error=None):
        if error is None:
            error = sys.exc_info()[1]
        text = default
        try:
            if isinstance(error, PyTango.DevFailed):
                text = str("\n".join(["%s " % (err.desc) for err in error]))

        except Exception as e:
#            print e
            pass
        return text

    @classmethod
    def warning(cls, parent, title, text, detailedText=None, icon=None):
        msgBox = Qt.QMessageBox(parent)
        msgBox.setText(title)
        msgBox.setInformativeText(text)
        if detailedText is not None:
            msgBox.setDetailedText(detailedText)
        if icon is None:
            icon = Qt.QMessageBox.Warning
        msgBox.setIcon(icon)
#        msgBox.setSizeGripEnabled(True)
#        msgBox.setMinimumWidth(12000)
        spacer = Qt.QSpacerItem(500, 0, Qt.QSizePolicy.Minimum,
                                Qt.QSizePolicy.Expanding)
        layout = msgBox.layout()
        layout.addItem(spacer, layout.rowCount(), 0, 1, layout.columnCount())
        ret = msgBox.exec_()
