from form import Form

class Login:
	def __init__(self, qtw, qtg):
		self.username = ""
		self.password = ""
		self._qtw = qtw
		self._qtg = qtg


	@property
	def get_qtw(self):
		return self._qtw

	@property
	def get_qtg(self):
		return self._qtg

	def generate_login(self):
		"""Build login page
		"""

		# get properties
		qtw = self.get_qtw
		qtg = self.get_qtg

		# create a form
		form = Form(
			name="Login In",
			data=["username", "password"],  
			qtw=qtw, 
			qtg=qtg)

		return form.create_form()

		