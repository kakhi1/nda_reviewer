from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from nda_reviewer.tools.custom_tool import PdfDocxReaderTool


# Initialize the tool to search within any DOCX file's content


# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class NdaReviewer():
	"""NdaReviewer crew"""


	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	# @agent
	# def uploader(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['uploader'], 
			
	# 		verbose=True,
			
	@agent
	def uploader(self) -> Agent:
		# 1) Create the agent from config
		agent = Agent(
			config=self.agents_config['uploader'],
			verbose=True,
			tools=[PdfDocxReaderTool()]
		)
		# 2) Attach the PdfDocxReaderTool so the agent can read PDF/DOCX


		return agent


	@agent
	def legal_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['legal_analyst'],
			verbose=True,

		)
	
	@agent
	def recommendation_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['recommendation_agent'],
			verbose=True,

		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task


	# @task
	# def upload_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['upload_task'],
	# 		output_file='report.md',
	# 	)
	@task
	def upload_task(self) -> Task:
		# Override the default 'run' so we can instruct the agent to call our tool
		def on_run(inputs, memory, context):
			file_path = inputs.get("uploaded_file", "")
			if not file_path:
				raise ValueError("No file path provided in 'uploaded_file'")

			# Instruct the uploader agent: "Use the pdf_docx_reader tool to parse the file"
			prompt = f"Read the file located at {file_path} and return its text content."
			# 3) The agent sees the prompt, decides to call the 'pdf_docx_reader' tool
			response = self.uploader().run(prompt, inputs=inputs)

			# Final text from the file
			extracted_text = response.get("output", "")
			# Return it under 'uploaded_content' so subsequent tasks can consume it
			return {"uploaded_content": extracted_text}

		return Task(
			config=self.tasks_config['upload_task'],
			output_file='report.md',
				run=on_run
			)



	@task
	def analysis_task(self) -> Task:
		return Task(
			config=self.tasks_config['analysis_task'],
			output_file='report.md',

		)
	
	@task
	def recommendation_task(self) -> Task:
		return Task(
			config=self.tasks_config['recommendation_task'],
			output_file='report.md',

		)



	@crew
	def crew(self) -> Crew:
		"""Creates the NdaReviewer crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)


