class InputField: 
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


	def render_input(self, is_password=False):
		"""Create a label 
		"""

		# get properties
		qtw = self.get_qtw
		qtg = self.get_qtg
		data = self.get_data
		styles = self.get_styles

		input_field = qtw.QLineEdit()
		input_field.setFont(qtg.QFont(
			styles.get("font-family", "helvetica"),
			styles.get("font-size", 12)
		))

		if is_password == True:
			input_field.setEchoMode(qtw.QLineEdit.Password)

		return input_field