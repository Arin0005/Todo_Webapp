import streamlit as st
import pandas as pd  
from db_funs import *
import re 

from db_funs import add_data, view_all_data, create_table, edit_task_data, delete_data, view_all_task_names


# main code 
def main():
	menu = ["Create","Read","Update","Delete","About"]
	choice = st.sidebar.selectbox("Menu",menu)
	create_table()   # creates a database and if already exists then it is skipped 
	if choice == "Create":
		Create_Task()
			
	elif choice == "Read":
		Read_data()

	elif choice == "Update":
		Update_task()

	elif choice == "Delete":
		Delete_task()

	else:
		st.subheader("About ToDo List App")
		st.info("Built with Streamlit, Pandas, SQLite3 and Regex")
		st.info("Team Members: Arin Thamke , Janvi Panchal, Yashas Mayekar")


# creates table and adds the task 
def Create_Task(): 
	st.subheader("Add Item")
	col1,col2 = st.columns(2)

	with col1:
			st.info("These special characters are not allowed: < > : ; ~ ` ^ _ {} + =")
			corrected_text = st.text_area("Task To Do")
			task = re.sub('[;:><`+=~^_{}]', "", corrected_text)     # Removes the special characters

	with col2:
			task_status = st.selectbox("Status",["ToDo","Done"])
			task_due_date = st.date_input("Due Date")

	if st.button("Add Task"):
		add_data(task,task_status,task_due_date)     # insetrs the data into table
		st.success("Added ::{} ::To Task".format(task))
		

# allows the accesebility to read data
def Read_data():  
	with st.expander("View All"):
		result = view_all_data()
			
		clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])     #data is structured in Pandas 
		st.dataframe(clean_df)     # merges the database with streamlit 

	with st.expander("Task Status"):
		task_df = clean_df['Status'].value_counts().to_frame()
		task_df = task_df.reset_index()
		st.dataframe(task_df)		


# allows to update/edit data 
def Update_task():
	st.subheader("Edit Items")
	with st.expander("Current Data"): # Shows the previously stored data without any changes
		result = view_all_data()
		clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
		st.dataframe(clean_df)

	# individually selects the rows of data and gives the allowences to edit those
	list_of_tasks = [i[0] for i in view_all_task_names()]  
	selected_task = st.selectbox("Task",list_of_tasks)
	task_result = get_task(selected_task)

	if task_result: # Shows the data which is beimg edited
		task = task_result[0][0]
		task_status = task_result[0][1]
		task_due_date = task_result[0][2]

		col1,col2 = st.columns(2)
			
		with col1:
			new_task = st.text_area("Task To Do",task)

		with col2:
			new_task_status = st.selectbox(task_status,["ToDo","Done"])
			new_task_due_date = st.date_input(task_due_date)

		# Actual Updation of task 
		if st.button("Update Task"):
			edit_task_data(new_task,new_task_status,new_task_due_date,task,task_status,task_due_date)
			st.success("Updated :: {} ::To {}".format(task,new_task))

		# Shows the Updated task	
		with st.expander("View Updated Data"):
			result = view_all_data()
			clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
			st.dataframe(clean_df)



def Delete_task():
	st.subheader("Delete")
	with st.expander("View Data"): # Shows the present data 
		result = view_all_data()
		clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
		st.dataframe(clean_df)
    
	# Selects the task which is to be deleted 
	unique_list = [i[0] for i in view_all_task_names()]
	delete_by_task_name =  st.selectbox("Select Task",unique_list)
	if st.button("Delete"):
		delete_data(delete_by_task_name)
		st.warning("Deleted: '{}'".format(delete_by_task_name))
    
	# Shows the table after deletion  
	with st.expander("Updated Data"):
		result = view_all_data()
		clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
		st.dataframe(clean_df)


if __name__ == '__main__':
	main()