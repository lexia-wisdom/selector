#!/usr/bin/env python
#   This file is part of nexdatas - Tango Server for NeXus data writer
#
#    Copyright (C) 2014-2015 DESY, Jan Kotanski <jkotan@mail.desy.de>
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
## \file Views.py
# module with different table views

""" main window application dialog """


try:
    from taurus.external.qt import Qt
except:
    from taurus.qt import Qt

import sip
import logging
logger = logging.getLogger(__name__)


class CheckerLabelWidget(Qt.QWidget):
    def __init__(self, parent=None):
        super(Qt.QWidget, self).__init__(parent)
        self.checkBox = Qt.QCheckBox(self)
        self.label = Qt.QLabel(self)
        layout = Qt.QHBoxLayout()
        layout.addWidget(self.checkBox)
        layout.addWidget(self.label)
        layout.setContentsMargins(2, 2, 2, 2)
        self.setLayout(layout)

    def isChecked(self):
        return self.checkBox.isChecked()

    def setChecked(self, status):
        self.label.setEnabled(status)
        return self.checkBox.setChecked(status)

    def setCheckable(self, status):
        return self.checkBox.setCheckable(status)

    def setEnabled(self, status):
        return self.checkBox.setEnabled(status)

    def setPolicy(self, policy):
        return self.label.setPolicy(policy)

    def setText(self, text):
        return self.label.setText(text)


class TableView(Qt.QTableView):

    def __init__(self, parent=None):
        super(TableView, self).__init__(parent)
        self.verticalHeader().setVisible(False)
#        self.horizontalHeader().setVisible(False)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setResizeMode(Qt.QHeaderView.Stretch)


class OneTableView(Qt.QTableView):

    def __init__(self, parent=None):
        super(OneTableView, self).__init__(parent)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setResizeMode(Qt.QHeaderView.Stretch)

    def reset(self):
        super(OneTableView, self).reset()
        for i in range(1, 5):
            self.hideColumn(i)


class CheckerView(Qt.QWidget):

    def __init__(self, parent=None):
        super(CheckerView, self).__init__(parent)
        self.model = None
        self.glayout = Qt.QGridLayout(self)
        self.widgets = []
#        self.mapper = Qt.QSignalMapper(self)
        self.dmapper = None
        self.displays = []
#        self.connect(self.mapper, Qt.SIGNAL("mapped(QWidget*)"),
#                     self.checked)
        self.spacer = None
        self.widget = Qt.QCheckBox
        self.center = True
        self.rowMax = 0
        self.selectedWidgetRow = None
        self.showLabels = True
        self.showNames = True

    def checked(self, widget):
        row = self.widgets.index(widget)
        self.selectedWidgetRow = row
        ind = self.model.index(row, 0)
        value = Qt.QVariant(self.widgets[row].isChecked())

        if self.dmapper:
            if not value:
                self.displays[row].setChecked(bool(False))

#        self.model.setData(ind, value, Qt.Qt.CheckStateRole)

    def setModel(self, model):
        self.model = model
#        self.connect(self.model,
#                     Qt.SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
#                     self.reset)
#        self.connect(self.model,
#                     Qt.SIGNAL("modelReset()"),
#                     self.reset)
        self.reset()

    def clearLayout(self):
#        print "CLEAR"
        if self.glayout:
#            print "LAY"
            for w in self.widgets:
                w.hide()
                w.close()
                w.setParent(None)
                if hasattr(w, "deleteLater"):
                    w.deleteLater()
                Qt.QObjectCleanupHandler().add(w)
                del w    
                w = None
                
            self.widgets = []
            if self.dmapper:
                self.displays = []
            self.spacer = None
#            for i in reversed(range(self.glayout.count())): 
#                print i
#                child = self.glayout.itemAt(i)
            print "VIEW COUNTS", self.glayout.count()
            child = self.glayout.takeAt(0)
            while child:
                print "child View", child
                self.glayout.removeItem(child)
                if isinstance(child, Qt.QWidgetItem):
                    w = child.widget()
                    w.hide()
                    w.close()
                    w.setParent(None)
                    self.glayout.removeWidget(w)
                    if hasattr(w, "deleteLater"):
                        w.deleteLater()
#                        print "WL", type(w)
#                    else:
#                        print "WW", type(w)
#                    print "DEL W", w    
                    Qt.QObjectCleanupHandler().add(w)
#                    sip.delete(w)
                    del w    
                    w = None
#                else:
#                    print "TYPE",type(child)
#                    if hasattr(child, "widget"):
#                        print "WTYPE",type(child.widget())
#                child.setParent(None)
#                Qt.QObjectCleanupHandler().add(child)
                if child:
                    sip.delete(child)
                del child    
                child = self.glayout.takeAt(0)
#            print "COUNTS", self.glayout.count()
            Qt.QWidget().setLayout(self.layout())
            Qt.QObjectCleanupHandler().add(self.layout())
            self.glayout = Qt.QGridLayout(self)

    def connectMapper(self):
#        self.mapper = Qt.QSignalMapper(self)
#            self.connect(self.mapper, Qt.SIGNAL("mapped(QWidget*)"),
#                         self.checked)
        if self.dmapper:
            self.dmapper = Qt.QSignalMapper(self)
#                self.connect(self.dmapper, Qt.SIGNAL("mapped(QWidget*)"),
#                             self.dchecked)

    def reset(self):
        self.hide()
        self.clearLayout()
#        self.connectMapper()
        self.updateState()
#        if self.selectedWidgetRow is not None:
#            if len(self.widgets) > self.selectedWidgetRow:
#                self.widgets[self.selectedWidgetRow].setFocus()
#            self.selectedWidgetRow = None
        self.show()

    def __findRowNumber(self, rowMax, rowCount):
        rowNo = rowMax
        if rowNo < 1:
            rowNo = 1
        fullColumnNo = rowCount / rowNo
        lastRowNo = rowCount % rowNo
        while lastRowNo and fullColumnNo < rowNo - lastRowNo:
            rowNo -= 1
            lastRowNo += fullColumnNo
        return rowNo

    def updateState(self):
        if not self.model is None:
            rowCount = self.model.rowCount()
            rowNo = self.__findRowNumber(self.rowMax, rowCount)

            for row in range(rowCount):

                cb, ds = self.__setWidgets(row)
#                self.__setNameTips(row, cb)
                self.__createGrid(row, cb, ds, rowNo)

            if not self.spacer:
#            if not self.spacer or True:
                self.spacer = Qt.QSpacerItem(10, 10,
                                          Qt.QSizePolicy.Minimum,
#                                         QSizePolicy.Expanding,
                                          Qt.QSizePolicy.Expanding)
#                print "SPACER", self.spacer
                self.glayout.addItem(self.spacer)

        self.update()
        self.updateGeometry()

    def __createGrid(self, row, cb, ds, rowNo=None):
        rowNo = self.rowMax if not rowNo else rowNo
        ind = self.model.index(row, 0)
        ind2 = self.model.index(row, 2)
        status = self.model.data(ind, role=Qt.Qt.CheckStateRole)
        dstatus = self.model.data(ind2, role=Qt.Qt.CheckStateRole)
        if status is not None:
            cb.setChecked(bool(status))
        if self.dmapper:
            if dstatus is not None:
                ds.setChecked(bool(dstatus))
        if row >= len(self.widgets):
            if rowNo:
                lrow = row % rowNo
                lcol = row / rowNo
            else:
                lrow = row
                lcol = 0
            if self.dmapper:
                lrow = lrow + 1
                lcol = 2 * lcol
#                if lrow == 1:
#                    self.glayout.addWidget(
#                        Qt.QLabel(self.slabel), 0, lcol, 1, 1)
#                    self.glayout.addWidget(
#                        Qt.QLabel(self.dlabel), 0, lcol + 1, 1, 1,
#                        Qt.Qt.AlignRight)
#                self.glayout.addWidget(ds, lrow, lcol + 1, 1, 1,
#                                      Qt.Qt.AlignRight)
            print "ADD CB", cb    
            self.glayout.addWidget(cb, lrow, lcol, 1, 1)
#            self.glayout.addWidget(Qt.QCheckBox(), lrow, lcol, 1, 1)
#            self.widgets.append(cb)
#            self.connect(cb, Qt.SIGNAL("clicked()"),
#                         self.mapper, Qt.SLOT("map()"))
#            self.mapper.setMapping(cb, cb)
#            if self.dmapper:
#                self.displays.append(ds)
#                self.connect(ds, Qt.SIGNAL("clicked()"),
#                             self.dmapper, Qt.SLOT("map()"))
#                self.dmapper.setMapping(ds, ds)

    def __setWidgets(self, row):
        ind = self.model.index(row, 0)
        flags = self.model.flags(ind)
        ind2 = self.model.index(row, 2)
        flags2 = self.model.flags(ind2)
        ds = None
        cb = None
        if row < len(self.widgets):
            cb = self.widgets[row]
            if self.dmapper:
                ds = self.displays[row]
        else:
            cb = self.widget()
            if hasattr(cb, "setCheckable"):
                cb.setCheckable(True)
            if self.dmapper:
                ds = self.widget()
                if hasattr(ds, "setCheckable"):
                    ds.setCheckable(True)
            if hasattr(cb, "setSizePolicy") and self.center:
                sizePolicy = Qt.QSizePolicy(
                    Qt.QSizePolicy.Fixed, Qt.QSizePolicy.Fixed)
                sizePolicy.setHorizontalStretch(10)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(
                    cb.sizePolicy().hasHeightForWidth())
                cb.setSizePolicy(sizePolicy)

        cb.setEnabled(bool(Qt.Qt.ItemIsEnabled & flags))
        if self.dmapper:
            ds.setEnabled(bool(Qt.Qt.ItemIsEnabled & flags2))
        return (cb, ds)

    def __setNameTips(self, row, cb):
        ind = self.model.index(row, 0)
        ind1 = self.model.index(row, 1)
        name = self.model.data(ind, role=Qt.Qt.DisplayRole)
        label = self.model.data(ind1, role=Qt.Qt.DisplayRole)

        if name:
            if self.showLabels and label and \
                    str(label).strip():
                if self.showNames:
                    cb.setText("%s [%s]" % (
                            str(label),
                            str(name)))
                else:
                    cb.setText("%s" % (str(label)))
            else:
                cb.setText(str(name))

#        text = self.model.data(ind, role=Qt.Qt.ToolTipRole)
        text = None
        text = str(text) if text else ""

        if self.showLabels:
            if self.showNames:
                if text.strip():
                    cb.setToolTip(text)
            else:
                if text.strip():
                    cb.setToolTip(
                        "%s: %s" % (str(name), text))
                else:
                    cb.setToolTip(str(name))
        else:
            ln = str(label) if label else str(name)
            if text.strip():
                cb.setToolTip("%s: %s" % (ln, text))
            else:
                cb.setToolTip(ln)


class CheckDisView(CheckerView):

    def __init__(self, parent=None):
        super(CheckDisView, self).__init__(parent)
#        self.dmapper = Qt.QSignalMapper(self)
#        self.connect(self.dmapper, Qt.SIGNAL("mapped(QWidget*)"),
#                     self.dchecked)
        self.center = False
        self.dlabel = 'Dis.'
        self.slabel = 'Sel.'

    def dchecked(self, widget):
        row = self.displays.index(widget)
        self.selectedWidgetRow = row
        ind = self.model.index(row, 2)
        value = Qt.QVariant(self.displays[row].isChecked())
#        self.model.setData(ind, value, Qt.Qt.CheckStateRole)


class RadioView(CheckerView):

    def __init__(self, parent=None):
        super(RadioView, self).__init__(parent)
        self.widget = Qt.QRadioButton


class LeftRadioView(CheckerView):

    def __init__(self, parent=None):
        super(LeftRadioView, self).__init__(parent)
        self.widget = Qt.QRadioButton
        self.center = False


class LeftCheckerView(CheckerView):

    def __init__(self, parent=None):
        super(LeftCheckerView, self).__init__(parent)
        self.center = False


class ButtonView(CheckerView):

    def __init__(self, parent=None):
        super(ButtonView, self).__init__(parent)
        self.widget = Qt.QPushButton
        self.center = False


class CheckerViewNL(CheckerView):

    def __init__(self, parent=None):
        super(CheckerViewNL, self).__init__(parent)
        self.showLabels = False


class LeftCheckerViewNL(LeftCheckerView):

    def __init__(self, parent=None):
        super(LeftCheckerViewNL, self).__init__(parent)
        self.showLabels = False


class ButtonViewNL(ButtonView):

    def __init__(self, parent=None):
        super(ButtonViewNL, self).__init__(parent)
        self.showLabels = False


class RadioViewNL(RadioView):

    def __init__(self, parent=None):
        super(RadioViewNL, self).__init__(parent)
        self.showLabels = False


class LeftRadioViewNL(LeftRadioView):

    def __init__(self, parent=None):
        super(LeftRadioViewNL, self).__init__(parent)
        self.showLabels = False


class CheckerViewNN(CheckerView):

    def __init__(self, parent=None):
        super(CheckerViewNN, self).__init__(parent)
        self.showNames = False


class LeftCheckerViewNN(LeftCheckerView):

    def __init__(self, parent=None):
        super(LeftCheckerViewNN, self).__init__(parent)
        self.showNames = False


class ButtonViewNN(ButtonView):

    def __init__(self, parent=None):
        super(ButtonViewNN, self).__init__(parent)
        self.showNames = False


class RadioViewNN(RadioView):

    def __init__(self, parent=None):
        super(RadioViewNN, self).__init__(parent)
        self.showNames = False


class LeftRadioViewNN(LeftRadioView):

    def __init__(self, parent=None):
        super(LeftRadioViewNN, self).__init__(parent)
        self.showNames = False


class RadioDisView(CheckDisView):

    def __init__(self, parent=None):
        super(RadioDisView, self).__init__(parent)
        self.widget = Qt.QRadioButton


class ButtonDisView(CheckDisView):

    def __init__(self, parent=None):
        super(ButtonDisView, self).__init__(parent)
        self.widget = Qt.QPushButton
        self.center = False


class CheckDisViewNL(CheckDisView):

    def __init__(self, parent=None):
        super(CheckDisViewNL, self).__init__(parent)
        self.showLabels = False


class ButtonDisViewNL(ButtonDisView):

    def __init__(self, parent=None):
        super(ButtonDisViewNL, self).__init__(parent)
        self.showLabels = False


class RadioDisViewNL(RadioDisView):

    def __init__(self, parent=None):
        super(RadioDisViewNL, self).__init__(parent)
        self.showLabels = False


class CheckDisViewNN(CheckDisView):

    def __init__(self, parent=None):
        super(CheckDisViewNN, self).__init__(parent)
        self.showNames = False


class CheckerLabelViewNN(CheckerViewNN):
    def __init__(self, parent=None):
        super(CheckerViewNN, self).__init__(parent)
        self.widget = CheckerLabelWidget


class ButtonDisViewNN(ButtonDisView):

    def __init__(self, parent=None):
        super(ButtonDisViewNN, self).__init__(parent)
        self.showNames = False


class RadioDisViewNN(RadioDisView):

    def __init__(self, parent=None):
        super(RadioDisViewNN, self).__init__(parent)
        self.showNames = False
