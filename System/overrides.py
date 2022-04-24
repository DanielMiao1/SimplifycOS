# -*- coding: utf-8 -*-
"""
System/overrides.py
PyQt widget overrides
Made by Daniel M using Python 3
"""

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *


class ToolButton(QToolButton):
	def __init__(self, parent):
		super(ToolButton, self).__init__(parent)


class PushButton(QPushButton):
	"""Add QPushButton Animation"""
	def __init__(self, text="", color="black") -> None:
		super().__init__()
		self.color = color
		self.setText(text)
		self._animation = QVariantAnimation(startValue=QColor("black"), endValue=QColor("white"), valueChanged=self.valueChanged, duration=200)
		self.updateStylesheet(QColor("white"))
		self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

	def valueChanged(self, color: QColor) -> None:
		"""If value changed"""
		self.updateStylesheet(color)

	def updateStylesheet(self, background: QColor) -> None:
		"""Update style sheet"""
		self.setStyleSheet(f"QPushButton {{background-color: {background.name()}; color: #888888; padding: 16px 32px; text-align: center; text-decoration: none; font-size: 16px; margin: 4px 2px; border: 2px solid white;}}")

	def enterEvent(self, event: QEvent) -> None:
		"""Display backward color animation on mouse hover"""
		self._animation.setDirection(QAbstractAnimation.Backward)
		self._animation.start()
		super().enterEvent(event)

	def leaveEvent(self, event: QEvent) -> None:
		"""Display forward color animation on mouse leave"""
		self._animation.setDirection(QAbstractAnimation.Forward)
		self._animation.start()
		super().leaveEvent(event)
	
	def updateColor(self, color="black") -> None:
		"""Update the color"""
		self.color = color
	

class Slider(QWidget):
	def __init__(self, minimum, maximum, value, update_function, interval=1, labels=None) -> None:
		super(Slider, self).__init__()
		levels = range(minimum, maximum + interval, interval)
		self.update_function = update_function
		self.levels = list(zip(levels, labels)) if labels is not None else list(zip(levels, map(str, levels)))
		self.layout = QVBoxLayout(self)
		self.left_margin = 10
		self.top_margin = 10
		self.right_margin = 10
		self.bottom_margin = 10
		self.layout.setContentsMargins(self.left_margin, self.top_margin, self.right_margin, self.bottom_margin)
		self.slider = QSlider(Qt.Orientation.Horizontal, self)
		self.slider.setMinimum(minimum)
		self.slider.setMaximum(maximum)
		self.slider.setValue(value)
		self.slider.setTickPosition(QSlider.TicksBelow)
		self.slider.setMinimumWidth(300)
		self.slider.setTickInterval(interval)
		self.slider.setSingleStep(1)
		self.slider.valueChanged.connect(self.update_function)
		self.layout.addWidget(self.slider)
		
	def value(self) -> int or float:
		return self.slider.value()
	
	def setValue(self, value) -> None:
		self.slider.setValue(value)
	
	def paintEvent(self, event) -> None:
		super(Slider, self).paintEvent(event)
		painter = QPainter(self)
		style = self.slider.style()
		style_slider = QStyleOptionSlider()
		style_slider.initFrom(self.slider)
		style_slider.orientation = self.slider.orientation()
		length = style.pixelMetric(QStyle.PM_SliderLength, style_slider, self.slider)
		available = style.pixelMetric(QStyle.PM_SliderSpaceAvailable, style_slider, self.slider)
		for x, y in self.levels:
			rect = painter.drawText(QRect(), Qt.TextFlag.TextDontPrint, y)
			position = QStyle.sliderPositionFromValue(self.slider.minimum(), self.slider.maximum(), x, available) + length // 2
			bottom = self.rect().bottom()
			if x == self.slider.minimum():
				if position-rect.width() // 2 + self.left_margin <= 0:
					self.left_margin = rect.width() // 2 - position
				if self.bottom_margin <= rect.height():
					self.bottom_margin = rect.height()
				self.layout.setContentsMargins(self.left_margin, self.top_margin, self.right_margin, self.bottom_margin)
			if x == self.slider.maximum() and rect.width() // 2 >= self.right_margin:
				self.right_margin = rect.width() // 2
				self.layout.setContentsMargins(self.left_margin, self.top_margin, self.right_margin, self.bottom_margin)
			painter.drawText(QPoint(position - rect.width() // 2 + self.left_margin, bottom), y)


class WebEngineView(QWebEngineView):
	def __init__(self, hide_context_menu=False) -> None:
		super(WebEngineView, self).__init__()
		self.hide_context_menu = hide_context_menu
	
	def contextMenuEvent(self, _) -> None:
		if self.hide_context_menu:
			return
		super(WebEngineView, self).contextMenuEvent()


class FileEditLineEdit(QLineEdit):
	def __init__(self, parent, cancel_function=None) -> None:
		super(FileEditLineEdit, self).__init__(parent)
		self.cancel_function = cancel_function
	
	def keyPressEvent(self, event):
		if event.key() == Qt.Key.Key_Escape and self.cancel_function is not None:
			self.cancel_function()
		super(FileEditLineEdit, self).keyPressEvent(event)
