def task():
    tasks = [] # empty list
    print("------WELCOME TO THE TASK MANAGEMENT APP------")

    total_task = int(input("Enter how many task you want to add = "))
    for i in range(1, total_task+1):
        task_name = input(f"Enter task {i} = ") # enter task 1 = 
        tasks.append(task_name)

    print(f"Today's task are\n{tasks}") 

    while True:
        operation = int(input("Enter 1-Add\n2-Update\n3-Delete\n4-View\n5-Exit/Stop/"))
        if operation ==1 :
            add = input("Enter task you want to add =")
            tasks.append(add) # adding the new task in end 
            print(f"Task {add} has been added successfully.... ")

        elif operation ==2:
            updated_val = input("Enter the task name you want to update= ")
            if updated_val in tasks:
                up = input("Enter your new tasks= ")
                ind = tasks.index(updated_val) # index ->  to find the position 
                tasks[ind] = up
                print(f"Updated task {up}")
        
        elif operation ==3:
            del_task = input("Enter your task name to delete = ")
            if del_task in tasks:
                ind = tasks.index(del_task)
                del tasks[ind]
                print(f"Task {del_task} has been deleted successfully....")

        elif operation == 4:
            print(f"Total tasks = {tasks}")

        elif operation == 5:
            print("Closing the program....")
            break

        else:
            print("Invalid Input")
        

task()
 