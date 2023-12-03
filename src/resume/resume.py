from resume.abstract_classes.abstract_resume import CV
from resume.iterators.iterators import Iterator


from typing import (
	Dict,
	List,
	Union,
	Callable
)

from reportlab.lib.pagesizes import A4, landscape, letter, inch
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch, cm

from reportlab.lib import colors

from reportlab.platypus import (
    SimpleDocTemplate, 
    BaseDocTemplate, 
    PageTemplate, 
    PageBreak, 
    Frame, 
    FrameBreak, 
    Spacer, 
    Paragraph,
    Image,
    Table,
    TableStyle
)

from resume.utils.Utils import (
	TextFormatter
)

import pyphen
from collections import deque

class Resume(CV):
	def __init__(self, data, name, iterator = None) -> None:
		super().__init__(data, name)
		self.iterator = Iterator(data) if iterator is None else iterator(data) 

	def generate_cv(self) -> str:
		self.Document(self).generate_template()

	def generate_simple_cv(self) -> str:
		self.Document(self).generate_simple_cv()

	class Document:
		def __init__(self, resume) -> None:
			self.resume = resume
			#Other private properties goes here
			self.__data = resume._data
			self._doc = SimpleDocTemplate(
				self.resume._name,
				pagesizes = A4,
				rightMargin = 2*cm,
				leftMargin = 2*cm,
				topMargin = 2*cm,
				bottomMargin = 2*cm)
			self._styles = getSampleStyleSheet()


		@property
		def get_data(self) -> Dict:
			"""
			This method retrieves the data passed to Resume instance. 
			"""
			return self.__data

		@property
		def get_iterator(self) -> Iterator:
			"""
			For optimization purposes, we have to introduce custom iterator.
			This method, called 'GETTER', retrieves the iterator.
			"""
			return self.resume.iterator

		@property
		def get_styles(self):
			"""
			This method retrieves the styles to use when creating a section.
			The logic is similar to that of React or Next.
			"""
			return self._styles

		@property
		def get_document(self):
			"""
			Retrieve the instance of SimpleDocTemplate class.
			to use its methods.
			"""
			return self._doc

		@property
		def get_about(self) -> str:
			"""
			Retrieve the 'about' text.
			"""
			data = self.get_data
			about = data.get("Individual traits", "No traits!")

			#Let us hyphen it, using our methods
			#Apply formatting!
			return TextFormatter.get_formatted_text(about) 

		def retrieve_speaking_languages(self) -> Dict[str, str]:
			"""
				This method returns a dictionary of languages:
					KEY: the name of the language
					VALUE: The formatted description of the languages based on Utils class
						   called TextFormatter which uses Pyphen library to hyphen words
						   in a text. 

				Args:
					self: The reference to the Object

				Returns: 
					Dictionary
			"""
			#retrieve data
			data = self.get_data

			#Slice the data
			data = data.get("Speaking Languages", {})

			#Organize data
			english, estonian, russian = TextFormatter.process_descriptions([
				language.get("Description", "No Description") 
				for language in [
					data.get(language,"No such language") for language in data.keys()
				]
			])



			#return dictionary
			return {
				"English": english,
				"Estonian": estonian,
				"Russian": russian
			}

	

		def get_fisrt_introduction(self) -> List[Union[Paragraph, Table]]:
			"""
			This method returns the first paragraph for the first page.

			Args:
				self: A reference to the class, object.
			"""
			#Get styles
			styles = self.get_styles

			#Get about information
			about = self.get_about

			# Organize Data
			data = {
				"Name": "Curriculum Vitae",
				"Author": "An independent python developer Sergei Ivanov",
				"About": {
					"Title": "About Me",
					"Content": about if about else ""
				},

				"Education": "Education",
			}

			#Implement Switch using Dictionary
			switch = {
				"Name": "Heading1",
				"Author": "Heading2",
				"About": {
					"Title": "Heading3",
					"Content": "Normal"
				},
				"Education": "Heading2",
			}

			table_data = self.get_data.get("Education", {})

			#Use a method to generate a custom section based on data
			#Pass our organized data
			result = self.generate_section(data, switch, True, "Education", table_data)
		

			#Return the list of paragraphs to use in the main part
			return result

		def skills_description(self) -> List[Union[Paragraph, Table]]:
			"""
			This function returns the second section of CV which describes communicative skills.

			Args: 
				Self: Reference to the class.

			Return:
				List of Paragraph and Table objects.

			"""

			#Retrieve styles
			styles = self.get_styles

			#Define result to return
			result = []

			#Define containters to store data for each language
			english = []
			estonian = []
			russian = []

			#Retrieve Data
			data = self.get_data.get("Speaking Languages", {})

			#Describe the section
			description = TextFormatter.get_formatted_text("""
				In this section, I would like to show my knowledge of speaking languages
			""")

			#Define section
			section = self.generate_section({
				"Name": "My Skills",
				"Description": description if description else ""
			}, {
				"Name": "Heading2",
				"Description": "Normal"
			}, False)


			#Traverse the data and populate language sections!
			for language in data:
				#Define queue
				queue = deque([])
				#Define the value for the corresponding language
				#This is going to be a nested dictionary for each language
				nested_dictionary = data[language]
				filtered = self.filter(nested_dictionary, lambda x: x != "Description")
				#Append the language to the queue
				queue.append([
					language, 
					filtered
				])

				while queue:
					#Deque 
					current = queue.popleft()

					#Destruct
					lang, table_data = current

					language_section = self.generate_section({
						"Section Name": lang,
						"Description": TextFormatter.get_formatted_text(nested_dictionary["Description"])
					}, {
						"Section Name": "Heading2",
						"Description": "Normal"
					}, True, lang, table_data)

					[english, estonian, russian][
						0 if lang == "English" else 1 if lang == "Estonian" else 2
					] += language_section

			
			return section, english,estonian, russian

		def create_table(self, data: Dict, first_column = "") -> Table:
			"""
			This method creates a table for specific inputs (follow DRY principle).

			Args:
				self: Reference to the class,
				data: input data which is of Dictionary type,
				first_column: in case you need to add the column name for keys of data.
			"""

			#Define Colums
			COLUMNS = [first_column]

			#Define rows
			ROWS = []

			#Define HashMap
			unique_columns = {}

			
			for key in data:
				#Enter the Outer loop
				#Retrieve the nested dictionary which is a value for the current key
				#Use print(isinstance(data[key], dict)) to check for nested dictionaries

				#Define value
				value = data[key] 

				#Handle some errors within the outer loop 
				try:
					#Define row
					row = [key]
					#Traverse the current nested dictionary
					if isinstance(value, dict):
						for _key, _value in value.items():
							#For each nested dictionary keys are uniques -> table property
							#So, we do not need to add those everytime! Suggestion: Use HashMap
							if _key not in unique_columns:
								COLUMNS.append(_key)
								unique_columns[_key] = True

							#Add key-value paired data to ROWS
							if isinstance(_value, list):
								for item in _value:
									if isinstance(item, tuple) and len(item) == 2:
										row += [item[0]]
										row += item[1]
									else:
										row += [_value]

							else:
								row += [_value]

						ROWS.append(row)
					else:
						ROWS.append(row)
				except KeyError:
					raise Error("Invalid Key")
			
			#Define Table
			table_data = [COLUMNS] + ROWS
			
			#Define styles for the Table 
			#Create the table
			table = Table(table_data)
			table.setStyle(TableStyle([
				('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header row background color
				('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header row text color
				('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center alignment for all cells
				('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Bold font for header row
				('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Padding for header row
				('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Background color for data rows
			]))

			return table

		def create_table_recursive(self, data: Dict, column_name="") -> Table:
			"""
			This method create a table using recursive approach

			Args:
				data: a dictionary to represent a data structure,
				column_name: a name for the first column.

			Returns:
				Table: An instance of Table class.
			"""
    
			COLUMNS = []
			ROWS = []
			unique_columns = {}

			for key in data:
				value = data[key]
				row = [key]
				if isinstance(value, dict):
					for _key, _value in value.items():
						COLUMNS.append(_key)
						unique_columns[_key] = True

						if isinstance(_value, dict):
							sub_table = self.create_table_recursive(_value, _key)
							sub_table_str = ""
							sub_table.wrapOn(self.get_canvas, 0, 0)
							sub_table.drawOn(self.get_canvas, 0, 0)
							for line in self.get_canvas._code:
								if isinstance(line, str):
									sub_table_str += line
							row += [sub_table_str]
						elif isinstance(_value, list):
							row += ["\n".join(str(item)) for item in _value]
						else:
							row += [_value]
					ROWS.append(row)
				else:
					ROWS.append(ROW)


		    #Define Table
			table_data = [COLUMNS] + ROWS
			
			#Define styles for the Table 
			#Create the table
			table = Table(table_data)
			table.setStyle(TableStyle([
				('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header row background color
				('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header row text color
				('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center alignment for all cells
				('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Bold font for header row
				('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Padding for header row
				('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Background color for data rows
			]))

			return table


		def filter(self, data: Dict, callback: Callable[[any], any] = True) -> Dict:
			"""
			Filter out the data based on condition provided in lambda function.

			Args:
				self: Reference to the class,
				data: dictionary,
				callback: lambda function to apply.

			Return:
				Modified Dictionary After Filter is Done.
			"""

			#Define the result
			result = {}

			#Traverse the dictionary
			for key in data:
				#Apply the lambda function
				if callback(key):
					result[key] = data[key]

			return result

		
		def filter_recursive(self, data: Dict, remove: str) -> Dict:
			"""
			This method uses the recursive approach to filter our a dictionary.

			Args:
				self: a reference to the object,
				data: dictionary to represent data structure,
				remove: a key to be removed in a filtered dictionary.

			Returns:
				A filtered dictionary.
			"""

			#Define base case
			if not isinstance(data, dict):
				return data

			#Define the result
			result = {}
			for key, value in data.items():
				if key != remove:
					if isinstance(value, dict):
						filtered_value = self.filter_recursive(value, remove)
						result[key] = filtered_value
					else:
						result[key] = value
			return result


		def generate_section(
			self, 
			data: Dict, 
			Switch: Dict = {}, 
			need_table: bool = False, 
			name: str = "Custom Name",
			table_data = {}) -> List[Union[Paragraph, Table]]:
			"""
			This method returns a section based on data and rules to apply styles.

			Args: 
				self: Reference to the class,
				data: dictionary containing the data to be rendere,
				Switch: dictionary to stylize the data to be rendered,
				need_table: boolean to check if user needs table,
				name: name to include in the first table.
			"""

			#Get styles
			styles = self.get_styles

			#Implement Switch to apply styles
			switch = Switch if Switch else {
				"Section Name": "Heading1",
				"Subsection1": {
					"Title": "Heading2",
					"Subtitle": "Heading3",
					"Content": "Normal"
				},

				"Subsection2": {
					"Title": "Heading2",
					"Subtitle": "Heading3",
					"Content": "Normal"
				},
			}

			table_data = table_data if table_data else data

			#Define result to return
			#Because I wanna get it and append to content (addToEnd)
			result = []

			#Iterate over the data dictionary to filld the list
			#We use Paragraph's constructor to create instance of Paragraph
			#Those have two params: 1) content; 2) style
			#Example: content.append(Paragraph("Some content of string type", styles["Normal"]))

			for key in data:
				#Traverse the outer dictionary
				#Define the value
				value = data[key]

				#Define the style
				style = switch[key]


				#Traverse the nested dictionary
				if not isinstance(value, dict):
					#Create the paragraph
					paragraph = Paragraph(value, styles[style])
					#Add to the result section
					result.append(paragraph)
				else:
					#define the nested switch
					nested_switch = switch[key]
					#Loop over the nested dictionary
					for _key, _value in value.items():
						#Define paragraph
						paragraph = Paragraph(_value, styles[nested_switch[_key]])
						#Append to result list
						result.append(paragraph)

			#Prepare the space for the table
			result.append(Spacer(1, 12))

			#Check if the user needs table
			#If so, create one and append to the end of the result list
			if need_table == True:
				table = self.create_table(table_data, first_column = name)
				result.append(table)


			return result

		#@cached
		def generate_section_recursive(self, data: Dict, rules: Dict) -> List[Paragraph]:
			"""
			This method retrieves the section using the recursive approach. 
			
			Description: 
				This is also a difficult method to understand, because
				traversed which is a recursive call happens to be a list
				instead of a nested dictionary to traverse until there are
				no nested dictionaries. More importantly, traversed is a list of
				Paragraph instances with the correct styles given in the map called
				'rules'. 

			Purpose:
				This method is powerful as it could create the whole section based on
				the data stored in the dictionaries.

			Args:
				self: the reference to the object,
				data: a dictionary to store the data of each section,
				rules: a dictionary which is the same shape as 'data' 
					and its purpose to store styles recognizeable by reportlab library.

			Returns:
				A list of Paragraph instances to be used later in the main list called 'content'.
			"""
			result = []
			styles = self.get_styles
			for key, value in data.items():
				value = data[key]
				style = rules[key]
				if isinstance(value, dict):
					traversed = self.generate_section_recursive(value, style)
					result.extend(traversed)
				else:
					paragraph = Paragraph(value, styles[style])
					result.append(paragraph)
			return result

		#Todo Revise the create_table to do this stuff
		def create_table_from_nested_data(self, data) -> Table:
			"""
			This method creates Table instance from a nested dictionary.

			Description:
				This method uses an iterative approach to fill the table_data list.
				A nested dictionary contained the value for a key as a tuple of items.

			Purpose:
				To generate a table based on difficult data: to represent a tuple as str in the displayed table.

			Args:
				self: the reference to the class,
				data: a dictionary of data which is used for the table.

			Returns:
				A Table object.
			"""
			table_data = []
			unique_columns = set()

			column_names = ["Programming Languages"]

			for lang, lang_data in data.items():
				for key in lang_data:
					if key not in unique_columns:
						column_names.append(key)
						unique_columns.add(key)

			table_data.append(column_names)

			for lang, lang_data in data.items():
				row_data = [lang]
				for col in column_names[1:]:
					if col in lang_data:
						value = lang_data[col]
						if col == "Technologies":
							if isinstance(value, tuple):
								row_data.append(", ".join(value))
							elif isinstance(value, list):
								tech_list = [f"{tech_type}: {', '.join(tech_list)}" for tech_type, tech_list in value]
								row_data.append("\n".join(tech_list))
							else:
								row_data.append(value)
						else:
							row_data.append(value)
					else:
						row_data.append("")
				table_data.append(row_data)

            # Define the table style
			table_style = TableStyle([
		        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header row background color
		        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header row text color
		        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center alignment for all cells
		        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Bold font for header row
		        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Padding for header row
		        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Background color for data rows
		    ])

		    # Create the table and apply the style
			table = Table(table_data)
			table.setStyle(table_style)

			return table

		def programming_skills(self):
			"""
			Retrieve the programming skills section.
			
			Desciption:
				This method generates a whole section using the recursive method called 'generate_section_recursive'.	
			"""

			#Get data
			data = self.get_data

			#Filter the data
			table_data = self.filter_recursive(data.get("Programming languages", {}), "Description")
			#Define result
			result = []

			#Provide description for Data Bases Section defined below
			description = """
				Throughout my programming journey, I touched upon various data bases such as Prisma, MongoDB, SQL
				This CV part describes my experience and knowledge gained so far. 
			"""


			#Create sections
			section_programming = self.generate_section({
				"Name": "Programming Languages",
				"Description": TextFormatter.get_formatted_text(data.get("Programming languages", {}).get("Description", ""))
			}, {
				"Name": "Heading2",
				"Description": "Normal"
			}, False)

			
			section_database = self.generate_section({
				"Name": "Data Bases",
				"Description": TextFormatter.get_formatted_text(description)
			}, {
				"Name": "Heading2",
				"Description": "Normal"
			}, True, "Data Bases", self.filter_recursive(data.get("Data bases"), "Description"))

			#Data for Additional Information Section:
			extra = data.get("Additional information", {})
			leetcode = extra.get("Leetcode", {})
			commitment = extra.get("Commitment", "")
			oop = extra.get("OOP", {})

			section_additional_information = self.generate_section_recursive({
				"Name": "Additional Information",
				"Section": {
					"Title": "Leetcode",
					"URL": "My link is available at" + leetcode.get("URL", ""),
					"Description": TextFormatter.get_formatted_text(leetcode.get("Description", ""))
				},

				"Interest Fields": {
					"Title": "Interest Fields",
					"Description": TextFormatter.get_formatted_text(data.get("Interest fields", ""))
				},

				"Commitment": {
					"Title": "Commitment",
					"GitHub": "My GitHub is available at " + data.get("Personal information", {}).get("GitHub", "") + ".",
					"Description": TextFormatter.get_formatted_text(commitment),
				},
				"OOP": {
					"Title": oop.get("Title", ""),
					"Description": TextFormatter.get_formatted_text(oop.get("Description", ""))
				},

				"Projects": {
					"Title": "Projects",
					"Description": "The projects that I have developed include:",
					"Games": TextFormatter.get_formatted_text("""
						I have implemented the following games: Snake, GuessNumber, Suduko, TicTacToe.
						To build each of them, I used OOP - which is object oriental programming, 
						one of the most fundamental principles in Computer Science.

					"""),
					"Resume": {
						"Title": "Resume - My CV",
						"Description": TextFormatter.get_formatted_text("""
							This current project is also my project; while developing it, I was using reportlab library
							and faced various difficulties. To build it, I used OOP principles: Encapsulation, Abstraction, Inheritance, Polymorphism.
							Meanwhile I had to use various Python's decorators to achieve some critical functionality such as memoization, and format 
							text; also, I cannot neglect the value of others: staticmethod, classmethod, propert - all these decorators are vital when
							working with OOP in Python. 
						"""),
					},
				}
			}, {
				"Name": "Heading2",
				"Section": {
					"Title": "Heading3",
					"URL": "Normal",
					"Description": "Normal",
				}, 

				"Interest Fields": {
					"Title": "Heading3",
					"Description": "Normal"
				},

				"Commitment": {
					"Title": "Heading3",
					"GitHub": "Normal",
					"Description": "Normal"
				},

				"OOP": {
					"Title": "Heading3",
					"Description": "Normal"
				},

				"Projects": {
					"Title": "Heading3",
					"Description": "Heading4",
					"Games": "Normal",
					"Resume": {
						"Title": "Heading2",
						"Description": "Normal"
					},
				}
			})
		
		

			result += section_programming
			table = self.create_table_from_nested_data(table_data)
			result.append(table)
			result.append(Spacer(1, 12))
			result += section_database
			result.append(Spacer(1, 12))
			result += section_additional_information
		
			return result


		def generate_template(self):
			"""
			A method of Document class to create a desired document.

			Description: 
				This is the main method which builds the document. 
				It uses various methods of Document class to ensure following DRY programming principle
				while maintaining OOP ones: 1) Encapsulation, 2) Abstraction, 3) Inheritance, and 4) Polymorphism.
			"""

			# Initialize the document:

			doc = self.get_document
			styles = self.get_styles

			content = []
			first_page_content = []

			#Descriptions of Speaking Languages Done By Utils 
			descriptions = self.retrieve_speaking_languages()

			#Get about me
			about = self.get_about

			#Define data
			data = self.get_data


			#Retrieve Speaking Languages Data
			#This is used for filling Paragraphs with data
			languages = data["Speaking Languages"]

			#THE FIRST PART

			"""
				Add The following to the content:
					Type: Curriculum Vitae,
					Author: Name of The developer,
					About: 
						Title: This is Heading 3
						Content: Description of the developer
					Education: Introducing to Table; Add the table
			"""
			introduction = self.get_fisrt_introduction()
			first_page_content.extend(introduction)

			#Here we describe the communicative skills
			section, english, estonian, russian = self.skills_description()

			first_page_content.extend(section)
			first_page_content.extend(english)
			first_page_content.extend(estonian)
			first_page_content.extend(russian)
			first_page_content.append(Spacer(1, 12))
			#Programming skills

			skills = self.programming_skills()
			first_page_content.extend(skills)

		
			content.extend(first_page_content)
		
			doc.build(content)


		def generate_simple_cv(self):
			"""
			A method of Document class to create a desired document (simplified)
			"""

			# Initialize the document:
			doc = self.get_document
			styles = self.get_styles

			data = self.get_data

			content = []

			section = self.generate_section_recursive({
				"Title": "Curriculum Vitae",
				"first-name": data.get('first-name'),
				"last-name": data.get('last-name'),
				"email": data.get('email'),
			    "phone": data.get('phone'),
			    "education": data.get('education'),
			    "work-experience": data.get('work-experience'),
			    "english-proficiency": data.get('english-proficiency'),
			    "estonian-proficiency": data.get('estonian-proficiency'),
			    "russian-proficiency": data.get('russian-proficiency'),
			    "mongo-proficiency": data.get('mongo-proficiency'),
			    "leetcode": data.get('leetcode'),
			    "github": data.get('github'),
			    "hobby": data.get('hobby')
			}, {
				"Title": "Heading1",
				"first-name":'Normal',
				"last-name":'Normal',
				"email": 'Normal',
			    "phone": 'Normal',
			    "education": 'Normal',
			    "work-experience": 'Normal',
			    "english-proficiency": 'Normal',
			    "estonian-proficiency": 'Normal',
			    "russian-proficiency": 'Normal',
			    "mongo-proficiency": 'Normal',
			    "leetcode": 'Normal',
			    "github": 'Normal',
			    "hobby": 'Normal'
			})

			content.extend(section)
			doc.build(content)