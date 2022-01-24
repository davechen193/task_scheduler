Do you know anyone that has a huge congestion on their todo list?
Here comes the solution with Task Scheduler!

Basically, the scheduler treats the scheduling like building a sturdy brick wall with constraints at the right hand side (due date constraint)

Assume that we are given some tasks with due dates. To avoid overdue tasks,
the scheduler does not schedule tasks past their due dates and tend to add
onto schedules to the right to make less congestion for each single day.

Boosting task scheduler with electron:
1. add a frontend and a backend server to the stack.
2. personalized data processing using s3 (data protocol with s3 instead of using database)
  * login.json (content includes login info, encoded string maps to a userid)
  {
    "content": [string],
    "users": {
      "encoded": string
    }
  }
  * users.json (content includes users table indexed by user id)
  {
    "userid": string,
    "tasks": [string]
  }
  * tasks.json (content includes tasks table indexed by task id)
  {
    "taskid": string,
    "duration": int,
    "due_date": Date,
    "description": string
  }
3. rendering schedules
  * add / remove task by using the db_connect function
  * create schedule: tasks to schedule optimization algorithm
  * add description: task notes are modifiable within the task object