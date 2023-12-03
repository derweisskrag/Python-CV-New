class Label: 
	def __init__(self, data, styles, qtw, qtg):
		self._data = data
		self._styles = styles
		self._qtw = qtw
		self._qtg = qtg


	@property
	def get_data(self):
		return self._data
	

	@property
	def get_qtw(self):
		return self._qtw


	@property
	def get_qtg(self):
		return self._qtg


	@property
	def get_styles(self):
		return self._styles


	def render_label(self):
		"""Create a label 
		"""

		# get properties
		qtw = self.get_qtw
		qtg = self.get_qtg
		data = self.get_data
		styles = self.get_styles

		label = qtw.QLabel(data)
		label.setFont(qtg.QFont(
			styles.get("font-family", "helvetica"),
			styles.get("font-size", 12)
		))

		return label