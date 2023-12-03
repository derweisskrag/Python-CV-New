from label import Label
from button import Button
from input import InputField

class Form:
	def __init__(self, name, data, qtw, qtg): 
		self._name = name
		self._data = data
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


	def create_form(self):
		"""Build the form
		"""
		# get data
		data = self.get_data

		# get properties
		qtw = self.get_qtw
		qtg = self.get_qtg

		# Define basic styles
		styles = {
			"font-family": "helvetica",
			"font-size": 16
		}

		# passing `qtw` and `qtg` as props
		# get labels
		input_fields = [InputField(info, styles, qtw, qtg) for info in data]

		# create button
		btn = Button(data, styles, qtw, qtg)

		# create a form
		form_layout = qtw.QFormLayout()

		# add name
		name = Label(
			self._name, {
				"font-family": "Times New Roman",
				"font-size": 24
			},
			qtw,
			qtg)

		# Add the name to the layout
		form_layout.addRow(name.render_label())

		# add first labels
		for name, input_field in zip(data, input_fields):
			if name == "password":
				form_layout.addRow(name, input_field.render_input(is_password=True))
			else:
				form_layout.addRow(name, input_field.render_input())

		# add button 
		form_layout.addRow(btn.render_button())

		return form_layout




