import tkinter as tk
from tkinter import messagebox, ttk

def calculate_schedule():
    try:
        processes = process_table.get_children()
        scheduling_algorithm = scheduling_type_var.get()

        process_data = []
        for process in processes:
            values = process_table.item(process, "values")
            process_data.append({
                "pid": values[0],
                "arrival": int(values[1]),
                "burst": int(values[2]),
                "priority": int(values[3]) if scheduling_algorithm == "Priority" else None
            })

        if scheduling_algorithm == "Shortest Time Remaining":
            result = shortest_time_remaining(process_data)
        elif scheduling_algorithm == "Priority":
            result = priority_scheduling(process_data)
        else:
            raise ValueError("Unsupported scheduling type")

        display_results(result)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def shortest_time_remaining(process_data):
    process_data.sort(key=lambda x: x["arrival"])
    time = 0
    completed = 0
    n = len(process_data)
    remaining_time = {p["pid"]: p["burst"] for p in process_data}
    gantt = []
    
    while completed < n:
        available_processes = [p for p in process_data if p["arrival"] <= time and remaining_time[p["pid"]] > 0]
        if not available_processes:
            time += 1
            continue

        current = min(available_processes, key=lambda x: remaining_time[x["pid"]])
        start_time = time
        time += 1
        remaining_time[current["pid"]] -= 1

        if remaining_time[current["pid"]] == 0:
            completed += 1

        gantt.append({"pid": current["pid"], "start": start_time, "end": time})

    return gantt

def priority_scheduling(process_data):
    process_data.sort(key=lambda x: (x["priority"], x["arrival"]))
    time = 0
    gantt = []
    
    for process in process_data:
        start_time = max(time, process["arrival"])
        time = start_time + process["burst"]
        gantt.append({"pid": process["pid"], "start": start_time, "end": time})

    return gantt

def display_results(schedule):
    gantt_canvas.delete("all")
    x_offset = 20
    y_offset = 50
    bar_height = 30
    time_step = 40

    for item in schedule:
        pid = item["pid"]
        start = item["start"]
        end = item["end"]

        x1 = x_offset + start * time_step
        x2 = x_offset + end * time_step
        y1 = y_offset
        y2 = y_offset + bar_height

        gantt_canvas.create_rectangle(x1, y1, x2, y2, fill="lightblue", outline="black")
        gantt_canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=pid)
        gantt_canvas.create_text(x1, y2 + 15, text=start, anchor="n")

    gantt_canvas.create_text(x2, y2 + 15, text=end, anchor="n")

def add_process():
    pid = process_id_entry.get()
    arrival = arrival_time_entry.get()
    burst = burst_time_entry.get()
    priority = priority_entry.get()

    if not (pid and arrival.isdigit() and burst.isdigit() and (priority.isdigit() or scheduling_type_var.get() != "Priority")):
        messagebox.showerror("Error", "Invalid input")
        return

    process_table.insert("", "end", values=(pid, arrival, burst, priority if scheduling_type_var.get() == "Priority" else "N/A"))
    process_id_entry.delete(0, "end")
    arrival_time_entry.delete(0, "end")
    burst_time_entry.delete(0, "end")
    priority_entry.delete(0, "end")

def clear_table():
    for item in process_table.get_children():
        process_table.delete(item)

# UI Setup
root = tk.Tk()
root.title("CPU Scheduling Simulator")

input_frame = tk.Frame(root)
input_frame.pack(pady=10)

tk.Label(input_frame, text="Process ID").grid(row=0, column=0)
tk.Label(input_frame, text="Arrival Time").grid(row=0, column=1)
tk.Label(input_frame, text="Burst Time").grid(row=0, column=2)
tk.Label(input_frame, text="Priority (if applicable)").grid(row=0, column=3)

process_id_entry = tk.Entry(input_frame, width=10)
process_id_entry.grid(row=1, column=0, padx=5)

arrival_time_entry = tk.Entry(input_frame, width=10)
arrival_time_entry.grid(row=1, column=1, padx=5)

burst_time_entry = tk.Entry(input_frame, width=10)
burst_time_entry.grid(row=1, column=2, padx=5)

priority_entry = tk.Entry(input_frame, width=10)
priority_entry.grid(row=1, column=3, padx=5)

tk.Button(input_frame, text="Add Process", command=add_process).grid(row=1, column=4, padx=5)
tk.Button(input_frame, text="Clear Table", command=clear_table).grid(row=1, column=5, padx=5)

process_table_frame = tk.Frame(root)
process_table_frame.pack(pady=10)

tk.Label(process_table_frame, text="Process Table").pack()

process_table = ttk.Treeview(process_table_frame, columns=("PID", "Arrival", "Burst", "Priority"), show="headings")
process_table.heading("PID", text="PID")
process_table.heading("Arrival", text="Arrival Time")
process_table.heading("Burst", text="Burst Time")
process_table.heading("Priority", text="Priority")
process_table.pack()

options_frame = tk.Frame(root)
options_frame.pack(pady=10)

scheduling_type_var = tk.StringVar(value="Shortest Time Remaining")
tk.Label(options_frame, text="Select Algorithm:").grid(row=0, column=0, padx=5)

tk.OptionMenu(options_frame, scheduling_type_var, "Shortest Time Remaining", "Priority").grid(row=0, column=1, padx=5)

tk.Button(options_frame, text="Calculate Schedule", command=calculate_schedule).grid(row=0, column=2, padx=5)

chart_frame = tk.Frame(root)
chart_frame.pack(pady=20)

tk.Label(chart_frame, text="Gantt Chart").pack()

gantt_canvas = tk.Canvas(chart_frame, width=800, height=200, bg="white")
gantt_canvas.pack()

root.mainloop()