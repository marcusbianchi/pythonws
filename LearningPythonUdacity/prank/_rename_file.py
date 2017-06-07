import os
import string
def rename_files():
	file_list = os.listdir(r"C:\Users\marcuss.SPI\PythonWorkspace\LearningPythonUdacity\prank");
	print(file_list)
	os.chdir(r"C:\Users\marcuss.SPI\PythonWorkspace\LearningPythonUdacity\prank")
	translator = str.maketrans({key: None for key in string.digits})	
	for file_name in file_list:
		os.rename(file_name,file_name.translate(translator))
	
rename_files();
