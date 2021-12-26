# I like to {build scheduled tasks that are given due date and amount of days required} a {calendar, denoting each day how many tasks can be handled}
# We want to avoid tasks passing due date and also have least maximum tasks per day.
import pprint
import random
import datetime

class Task:
	def __init__(self, n, d, l):
		self.duration = d
		self.due_date = l
		self.name = n
	def __repr__(self):
		return self.name + ",duration:"+str(self.duration)+",due_date:"+str(self.due_date)

# given a file with list of tasks, initialize them and build the schedules.
def initialize_tasks(file):
	result = []
	with open(file, 'r') as f:
		for line in f.readlines():
			t_components = line.split(',')
			t = Task(t_components[0], int(t_components[1]), int(t_components[2]))
			result.append(t)
	return result

def scheduled_calendars(tasks):
	due_dates = [task.due_date for task in tasks]
	due_dates.sort()
	task_compaction = []; task_log = []
	for due_date in due_dates:
		cur_tasks = []
		for task in tasks:
			if task.due_date <= due_date:
				cur_tasks.append(task)
		durations = [task.duration for task in cur_tasks]
		for task in sorted(cur_tasks, key = lambda task: task.duration)[::-1]:
			added = False
			duration = task.duration
			tups = list(zip(task_compaction, list(range(len(task_compaction)))))
			for date, i in sorted(tups, key=lambda tup: tup[0])[::-1]:
				if date + duration - 1 < due_date:
					schedule = (date, duration, i)
					task_compaction[i] += duration
					added = True
					break	
			if not added:
				if duration - 1 < due_date:
					task_compaction.append(duration)
					schedule = (0, duration, len(task_compaction)-1)
				else:
					print("task:", task, "isn't added.")
					return
			task_log.append((task, schedule))
		for task in cur_tasks:
			tasks.remove(task)
	return task_compaction, task_log

def render_log(log):
	dictionary = {}; result = []
	for record in log:
		k = record[1][-1]
		dictionary[k] = [record[1]] if k not in dictionary else dictionary[k] + [record[1]]
	for k in dictionary:
		dictionary[k].sort(key= lambda r: r[0])
		result.append(dictionary[k])
	pprint.pprint(dictionary)

def render_log2(log):
	day2tasks = {}
	days_arr = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
	min_i = 0; max_i = 0
	date = datetime.datetime.now(); day = days_arr[date.weekday()]

	for record in log:
		name = record[0].name
		index1 = int(record[1][0]); index2 = index1 + int(record[1][1]) - 1
		for i in range(index1,index2+1):
			cur_date = date + datetime.timedelta(days=i)
			cur_date_str = str(cur_date.month) + "/" + str(cur_date.day)
			max_i = i if i > max_i else max_i
			k = days_arr[(i + days_arr.index(day))%7] + "_" + cur_date_str
			day2tasks[k] = day2tasks.get(k,[])
			day2tasks[k].append(name)
	for i in range(min_i, max_i+1):
		cur_date = date + datetime.timedelta(days=i)
		cur_date_str = str(cur_date.month) + "/" + str(cur_date.day)
		k = days_arr[(i + days_arr.index(day))%7] + "_" + cur_date_str
		print(k, day2tasks[k])
		if "sunday" in k:
			print()

# test script
tasks = initialize_tasks("./sample.txt")
accums, log = scheduled_calendars(tasks)
render_log(log)
render_log2(log)
