# I like to {build scheduled tasks that are given due date and amount of days required} a {calendar, denoting each day how many tasks can be handled}
# We want to avoid tasks passing due date and also have least maximum tasks per day. We assign assign ratings to tasks (preferences)
import pprint
import random
import datetime
import numpy as np
class Task:
	def __init__(self, n, d, l, r):
		self.duration = d
		self.due_date = l
		self.name = n
		self.ref = r
	def __repr__(self):
		return self.name + ",duration:"+str(self.duration)+",due_date:"+str(self.due_date)+",ref:"+str(self.ref)

# given a file with list of tasks, initialize them and build the schedules.
def initialize_tasks(file):
	result = []
	with open(file, 'r') as f:
		lines = f.readlines()
		for i in range(len(lines)):
			line = lines[i]
			t_components = line.split(',')
			t = Task(t_components[0], int(t_components[1]), int(t_components[2]), len(lines) - i)
			result.append(t)
	return result

def task_priority(tasks, mode="performance"):
	due_dates = []
	durations = []
	refs = []
	complexities = []
	batches = []
	
	for task in tasks:
		due_dates.append(task.due_date)
		durations.append(task.duration)
		refs.append(task.ref)
	
	for task in tasks:
		complexities.append(task.duration/np.mean([duration for duration, due_date in zip(durations, due_dates)]) + task.ref/np.mean(refs))
	
	for i in range(len(tasks)):
		task = tasks[i]
		name = task.name
		if mode == "performance":
			ratio = abs(((task.duration/task.due_date)/np.mean([duration/due_date for duration, due_date in zip(durations,due_dates)])) - \
			(complexities[i]) / np.mean(complexities))
		elif mode == "preference":
			ratio = -task.ref
		elif mode == "not very nice":
			ratio = -abs(((task.duration/task.due_date)/np.mean([duration/due_date for duration, due_date in zip(durations,due_dates)])) - \
			(complexities[i]) / np.mean(complexities))
		batches.append((task, ratio))
	batches.sort(key=lambda tup: tup[1])
	return [tup[0] for tup in batches]

def scheduled_calendars(tasks):
	due_dates = [task.due_date for task in tasks]; due_dates.sort(); task_compaction = []
	task_log = []
	for due_date in due_dates:
		cur_tasks = []
		for task in tasks:
			if task.due_date <= due_date:
				cur_tasks.append(task)
		durations = [task.duration for task in cur_tasks]
		for task in task_priority(cur_tasks):
			added = False
			duration = task.duration
			tups = list(zip(task_compaction, list(range(len(task_compaction)))))
			for date, i in sorted(tups, key=lambda tup: tup[0]):
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
		name = record[0].name; duration = record[0].duration; due_date = record[0].due_date; ref = record[0].ref
		index1 = int(record[1][0]); index2 = index1 + int(record[1][1]) - 1
		for i in range(index1,index2+1):
			cur_date = date + datetime.timedelta(days=i)
			cur_date_str = str(cur_date.month) + "/" + str(cur_date.day)
			max_i = i if i > max_i else max_i
			k = days_arr[(i + days_arr.index(day))%7] + "_" + cur_date_str
			day2tasks[k] = day2tasks.get(k,[])
			day2tasks[k].append(Task(name, duration, due_date, ref)); duration -= 1; due_date -= 1
	for i in range(min_i, max_i+1):
		cur_date = date + datetime.timedelta(days=i)
		cur_date_str = str(cur_date.month) + "/" + str(cur_date.day)
		k = days_arr[(i + days_arr.index(day))%7] + "_" + cur_date_str
		tasks = task_priority(day2tasks[k])
		print(k, [task.name + "," + str(task.duration)+","+str(task.due_date)+","+str(task.ref) for task in tasks])
		if "sunday" in k:
			print()

# test script
tasks = initialize_tasks("./sample.txt")
accums, log = scheduled_calendars(tasks)
render_log2(log)

# Write test cases for task scheduler.