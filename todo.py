import streamlit as st
import pandas as pd
import re
import datetime  # To handle dates

from db_funs import add_data, get_task, view_all_data, create_table, edit_task_data, delete_data, view_all_task_names

# library for data viz
import matplotlib.pyplot as plt


# Adds header and applies colour to the app
def Header():
	st.header('TaskFlow Web App')


# Main function
def main():
	menu = ["Create", "Read", "Update", "Delete", "See Task Status", "Reminders", "About"]
	choice = st.sidebar.selectbox("Menu", menu)
	create_table()  # Ensure table exists before any operation

	# Menu options and corresponding functions
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
	elif choice == "See Task Status":
		Header()
		show_all_tasks()
	elif choice == "Reminders":  # NEW - Handle Reminders
		Header()
		show_reminders()  # Display reminder logic here
	else:
		Header()
		st.subheader("About Us")
		st.info("Built with Streamlit, Pandas, SQLite3, and Regex")
		st.info("Team Members: Soham Kawadkar, Yatin Mhatre, Pranay Devtale")



# Create task
def Create_task():
	st.subheader("Add Item")
	col1, col2 = st.columns(2)

	with col1:
		st.info("Special characters are not allowed: < > : ; ~ ` ^ _ {} + =")
		corrected_task = st.text_area('Task To Do', key="task_input")
		task = re.sub('[;:><`+=~^_{}]', "", corrected_task)  # Removes special characters

	with col2:
		task_status = st.selectbox('Status', ["ToDo", "Done"], key="status_select")
		task_due_date = st.date_input("Due Date")  # Task due date

	if st.button("Add Task"):
		add_data(task, task_status, task_due_date)  # Insert the data into the table
		st.success(f"Added :: {task} :: To Task")
		



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
	with st.expander("View Data" ): # Shows the present data
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
	with st.expander("Updated Data" ):
		result = view_all_data()
		clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
		st.dataframe(clean_df)




def show_all_tasks():
    # Fetch all task data from the database
    with st.expander("View All"):
        result = view_all_data()
        clean_df = pd.DataFrame(result, columns=["Task", "Status", "Date"])
        st.dataframe(clean_df)

    with st.expander("Task Status"):
        task_df = clean_df['Status'].value_counts().to_frame(name='count').reset_index() # Count repetations of each status
        task_df.columns = ['Status Type', 'count']  # rename the columns
        st.dataframe(task_df)

        # Create a pie chart using matplotlib
        fig, ax = plt.subplots()
        ax.pie(task_df['count'], labels=task_df['Status Type'], autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal ratio ensures the pie chart is circular.

        # Display the chart in Streamlit
        st.pyplot(fig)




# Function to handle reminders
def show_reminders():
	st.subheader("Reminders")

	# Fetch all task data from the database
	result = view_all_data()  # Make sure your db_funs has this function returning tasks with due dates
	clean_df = pd.DataFrame(result, columns=["Task", "Status", "Date"])

	# Ensure 'Date' is in a proper datetime format for filtering
	clean_df['Date'] = pd.to_datetime(clean_df['Date'], errors='coerce')

	# Get today's date
	today = datetime.date.today()

	# Filter for tasks due today
	due_today = clean_df[clean_df['Date'] == pd.Timestamp(today)]
	if not due_today.empty:
		st.warning("Tasks Due Today:")
		st.table(due_today)

	# Filter for overdue tasks
	overdue = clean_df[clean_df['Date'] < pd.Timestamp(today)]
	if not overdue.empty:
		st.error("Overdue Tasks:")
		st.table(overdue)

	# Filter for tasks due in the next 3 days
	next_three_days = clean_df[(clean_df['Date'] > pd.Timestamp(today)) &
							   (clean_df['Date'] <= pd.Timestamp(today + datetime.timedelta(days=3)))]
	if not next_three_days.empty:
		st.info("Tasks Due in the Next 3 Days:")
		st.table(next_three_days)

	# Show a success message if no tasks are due soon or overdue
	if due_today.empty and overdue.empty and next_three_days.empty:
		st.success("No upcoming deadlines or overdue tasks!")




if __name__ == '__main__':
	main()