from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load data from CSV
students = pd.read_csv('/Users/suryaprakash/Desktop/Project/students.csv')  # Contains roll number, branch, name
rooms = pd.read_csv('/Users/suryaprakash/Desktop/Project/ rooms.csv')  # Contains room number, capacity
faculty = pd.read_csv('/Users/suryaprakash/Desktop/Project/faculty.csv')  # Contains faculty name, branch

# Function to allocate students to rooms branch-wise
def allocate_seats_branch_wise(students, rooms, faculty):
    allocation = {}
    faculty_allocation = {}
    
    # Group students by branch
    grouped_students = students.groupby('branch')
    room_index = 0
    remaining_capacity = rooms.iloc[room_index]['capacity']  # Start with the first room capacity

    for branch, students_in_branch in grouped_students:
        students_in_branch = students_in_branch.reset_index(drop=True)  # Reset index for easy looping
        student_index = 0
        
        while student_index < len(students_in_branch):
            # If current room is full, move to the next room
            if remaining_capacity == 0:
                room_index += 1
                if room_index < len(rooms):
                    remaining_capacity = rooms.iloc[room_index]['capacity']
                else:
                    break  # No more rooms available
            
            # Allocate as many students as the current room can hold
            num_to_allocate = min(remaining_capacity, len(students_in_branch) - student_index)
            allocated_students = students_in_branch.iloc[student_index:student_index + num_to_allocate].to_dict('records')
            
            room_number = rooms.iloc[room_index]['room_number']
            
            # Add the students to the room
            if room_number not in allocation:
                allocation[room_number] = []
            allocation[room_number].extend(allocated_students)
            
            # Update indices and remaining capacity
            student_index += num_to_allocate
            remaining_capacity -= num_to_allocate

            # Assign a faculty member to the room (not from the same branch as students)
            available_faculty = faculty[faculty['branch'] != branch]  # Faculty from different branches
            if room_number not in faculty_allocation and not available_faculty.empty:
                assigned_faculty = available_faculty.sample(1).to_dict('records')[0]  # Randomly assign a faculty member
                faculty_allocation[room_number] = assigned_faculty

    return allocation, faculty_allocation

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/allocate', methods=['POST'])
def allocate():
    allocation, faculty_allocation = allocate_seats_branch_wise(students, rooms, faculty)
    return render_template('result.html', allocation=allocation, faculty_allocation=faculty_allocation)

if __name__ == '__main__':
    app.run(debug=True)
