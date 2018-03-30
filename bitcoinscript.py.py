import xlrd
import os
from epsilon.models import Question, Option, Course, Content

bchainexcel= xlrd.open_workbook(os.path.join(os.getcwd(), 'block_chain_quiz.xlsx'))
z = bchainexcel.sheet_by_index(0)

for i in range(1, 20):
	try:
		course = Course.objects.get(name='Blockchain')
		content = Content.objects.get(course_id=course, name='Bitcoin')
		question = z.cell(i, 1).value
		level = z.cell(i, 8).value
	
		option_a = z.cell(i, 2).value
		option_b = z.cell(i, 3).value
		option_c = z.cell(i, 4).value
		option_d = z.cell(i, 5).value
		option_e = z.cell(i, 6).value

		answer = z.cell(i,7).value
			
		quiz = Question.objects.create(
				content_id = content,
				level = level,
				question = question,
				answer = answer
			
			)
				
		print (str(i) + "done")
	
	except Exception as e:
		print(e)
		print(i)