import streamlit as st
import pandas as pd  
import re 
from animate import css
from db_funs import add_data, get_task, view_all_data, create_table, edit_task_data, delete_data, view_all_task_names


# Adds header and applies colour to the app
def Header():
	st.markdown('<h1 class="fade-in glow"> ToDo List Web App </h1>', unsafe_allow_html=True)


# main code 
def main():
	css()
	menu = ["Create","Read","Update","Delete","See Tasks","About"]
	choice = st.sidebar.selectbox("Menu",menu)
	create_table()   # creates a database, if it already does not exists
	if choice == "Create":
		Header()
		Create_task()
			
	elif choice == "Read":
		Header()
		Read_data()

	elif choice == "Update":
		Header()
		Update_task()

	elif choice == "Delete":
		Header()
		Delete_task()

	elif choice == "See Tasks":
		Header()
		show_all_tasks()	

	else:
		Header()
		st.subheader(" Category 2 : ")
		st.info("Built with Streamlit, Pandas, SQLite3 and Regex")
		st.info("Team Members: Arin Thamke , Janvi Panchal, Yashas Mayekar")



# creates table and adds the task 
def Create_task(): 
	st.subheader("Add Item")
	col1,col2 = st.columns(2)

	with col1:
			st.info("These special characters are not allowed: < > : ; ~ ` ^ _ {} + =")
			corrected_task = st.text_area('<div class="bounce-in">Task To Do</div>', key="task_input")
			task = re.sub('[;:><`+=~^_{}]', "", corrected_task)     # Removes the special characters

	with col2:
			task_status = st.selectbox('<div class="zoom-in">Status</div>', ["ToDo", "Done"], key="status_select")
			task_due_date = st.date_input("Due Date")

	if st.button("Add Task"):
		add_data(task,task_status,task_due_date)     # insetrs the data into table
		st.success(f'<div class="fade-in">Added ::{task} ::To Task</div>', unsafe_allow_html=True)
		


# allows the accesebility to read data
def Read_data():  
	with st.expander("View All", expanded=True):
		result = view_all_data()
		clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])     #data is structured in Pandas 
		st.markdown('<div class="slide-in">', unsafe_allow_html=True)
		st.dataframe(clean_df)     # merges the database with streamlit 
		st.markdown('</div>', unsafe_allow_html=True)

	with st.expander("Task Status"):
		task_df = clean_df['Status'].value_counts().to_frame()
		task_df = task_df.reset_index()
		st.dataframe(task_df)		



# allows to update/edit data 
def Update_task():
	st.subheader("Edit Items", expanded=True)
	with st.expander("Current Data", expanded=True): # Shows the previously stored data without any changes
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
			st.info("These special characters are not allowed: < > : ; ~ ` ^ _ {} + =")
			new_corrected_task = st.text_area("Task To Do",task)
			new_task = re.sub('[;:><`+=~^_{}]', "",new_corrected_task)    # Does not allow the special characters in the updated task

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
	with st.expander("View Data", expanded=True): # Shows the present data 
		result = view_all_data()
		clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
		st.dataframe(clean_df)
    
	# Selects the task which is to be deleted 
	unique_list = [i[0] for i in view_all_task_names()]
	delete_by_task_name =  st.selectbox("Select Task",unique_list)
	if st.button("Delete"):
		delete_data(delete_by_task_name)
		st.warning("Deleted: '{}'".format(delete_by_task_name))
    
	# Shows the table after deletion of task
	with st.expander("Updated Data", expanded=True):
		result = view_all_data()
		clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
		st.dataframe(clean_df)



def show_all_tasks():
	# Fetch all task data from the database
	result = view_all_data()
	if result:
		# Display task data as a structured DataFrame
		clean_df = pd.DataFrame(result, columns=["Task", "Status", "Date"])
		st.markdown('<div class="fade-in">', unsafe_allow_html=True)
		st.dataframe(clean_df)
		st.markdown('</div>', unsafe_allow_html=True)
	else:
		st.write("No tasks available.")



if __name__ == '__main__':
	main()