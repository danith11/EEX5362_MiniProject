import tkinter as tk
from tkinter import ttk, messagebox
import random
import math
import heapq
import matplotlib.pyplot as plt

# poisson distribution and exponential distribution


def poissonService(rate):
    return -math.log(1.0 - random.random()) / rate


def exponentialService(rate):
    return -math.log(1.0 - random.random()) / rate

# Cloud Simulator logic


def simulateCloudSystem(arrivalRate, serviceRate, servers, queueLimit, simulateTime=1000):

    currentTime = 0
    eventQueue = []
    taskQueue = []
    serverStatus = [0] * servers
    serverBusyTime = [0] * servers

    totalWait = 0
    totalExecution = 0
    completed = 0
    failed = 0
    taskId = 0

    heapq.heappush(eventQueue, (poissonService(
        arrivalRate), "arrival", taskId))

    while eventQueue:
        currentTime, event, sid = heapq.heappop(eventQueue)

        if currentTime > simulateTime:
            break

        if event == "arrival":
            heapq.heappush(
                eventQueue,
                (currentTime + poissonService(arrivalRate), "arrival", taskId)
            )
            taskId += 1

            if 0 in serverStatus:
                s = serverStatus.index(0)
                serverStatus[s] = 1
                serviceTime = exponentialService(serviceRate)
                serverBusyTime[s] += serviceTime

                heapq.heappush(
                    eventQueue,
                    (currentTime + serviceTime, "departure", s)
                )
                totalExecution += serviceTime
                completed += 1
            else:
                if len(taskQueue) < queueLimit:
                    taskQueue.append(currentTime)
                else:
                    failed += 1

        else:
            serverStatus[sid] = 0

            if taskQueue:
                arrival = taskQueue.pop(0)
                totalWait += currentTime - arrival

                serverStatus[sid] = 1
                serviceTime = exponentialService(serviceRate)
                serverBusyTime[sid] += serviceTime

                heapq.heappush(
                    eventQueue,
                    (currentTime + serviceTime, "departure", sid)
                )
                totalExecution += serviceTime
                completed += 1
# calculations
    averageWaitTime = totalWait / completed if completed else 0
    averageExecutionTime = totalExecution / completed if completed else 0
    throughput = completed / simulateTime
    utilization = sum(serverBusyTime) / (servers * simulateTime)
    errorRate = failed / (completed + failed) if (completed + failed) else 0

    return averageWaitTime, averageExecutionTime, throughput, utilization, errorRate

# Simulator run function
def runSimulation():
    try:
        arrival = float(arrivalEntry.get())
        service = float(serviceEntry.get())
        servers = int(serverEntry.get())
        queue = int(queueEntry.get())

        w, e, t, u, err = simulateCloudSystem(arrival, service, servers, queue)

        wait.set(f"{w:.3f}")
        execution.set(f"{e:.3f}")
        throughput.set(f"{t:.3f}")
        CPUUtil.set(f"{u*100:.2f} %")
        errorR.set(f"{err*100:.2f} %")

    except Exception as ex:
        messagebox.showerror("Input Error", str(ex))

# Graph
def showGraph():
    labels = ["Waiting Time", "Execution Time",
              "Throughput", "Utilization", "Error Rate"]
    values = [
        float(wait.get()),
        float(execution.get()),
        float(throughput.get()),
        float(CPUUtil.get().replace('%', '')),
        float(errorR.get().replace('%', ''))
    ]
    plt.figure()
    plt.bar(labels, values)
    plt.title("Cloud Performance Metrics")
    plt.show()


# GUI
root = tk.Tk()
root.title("Cloud Workload Performance Simulator")
root.geometry("520x540")

style = ttk.Style()
style.theme_use("default")
style.configure("TFrame", background="#f5f6f7")
style.configure("TLabel", background="#f5f6f7", font=("Segoe UI", 10))
style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"))
style.configure("TButton", font=("Segoe UI", 10), padding=6)
style.configure("Value.TLabel", font=("Segoe UI", 10, "bold"))

mainFrame = ttk.Frame(root, padding=20)
mainFrame.pack(expand=True)

# Header
ttk.Label(
    mainFrame,
    text="Cloud Workload Performance Simulator",
    style="Header.TLabel"
).grid(row=0, column=0, columnspan=2, pady=(0, 15))

# Input Frame
inputFrame = ttk.LabelFrame(
    mainFrame, text="Simulation Parameters", padding=15)
inputFrame.grid(row=1, column=0, columnspan=2, pady=10)

ttk.Label(inputFrame, text="Arrival Rate (λ)").grid(
    row=0, column=0, sticky="w")
arrivalEntry = ttk.Entry(inputFrame, width=20)
arrivalEntry.insert(0, "6")
arrivalEntry.grid(row=0, column=1)

ttk.Label(inputFrame, text="Service Rate (μ)").grid(
    row=1, column=0, sticky="w")
serviceEntry = ttk.Entry(inputFrame, width=20)
serviceEntry.insert(0, "2")
serviceEntry.grid(row=1, column=1)

ttk.Label(inputFrame, text="Number of Servers").grid(
    row=2, column=0, sticky="w")
serverEntry = ttk.Entry(inputFrame, width=20)
serverEntry.insert(0, "3")
serverEntry.grid(row=2, column=1)

ttk.Label(inputFrame, text="Queue Limit").grid(row=3, column=0, sticky="w")
queueEntry = ttk.Entry(inputFrame, width=20)
queueEntry.insert(0, "20")
queueEntry.grid(row=3, column=1)

# Buttons
btnFrame = ttk.Frame(mainFrame)
btnFrame.grid(row=2, column=0, columnspan=2, pady=15)

ttk.Button(btnFrame, text="Run Simulation",
           command=runSimulation).grid(row=0, column=0, padx=10)
ttk.Button(btnFrame, text="Show Graph", command=showGraph).grid(
    row=0, column=1, padx=10)

# Output Frame
outputFrame = ttk.LabelFrame(mainFrame, text="Performance Metrics", padding=15)
outputFrame.grid(row=3, column=0, columnspan=2)

wait = tk.StringVar()
execution = tk.StringVar()
throughput = tk.StringVar()
CPUUtil = tk.StringVar()
errorR = tk.StringVar()

ttk.Label(outputFrame, text="Average Waiting Time").grid(
    row=0, column=0, sticky="w")
ttk.Label(outputFrame, textvariable=wait,
          style="Value.TLabel").grid(row=0, column=1)

ttk.Label(outputFrame, text="Average Execution Time").grid(
    row=1, column=0, sticky="w")
ttk.Label(outputFrame, textvariable=execution,
          style="Value.TLabel").grid(row=1, column=1)

ttk.Label(outputFrame, text="Throughput").grid(row=2, column=0, sticky="w")
ttk.Label(outputFrame, textvariable=throughput,
          style="Value.TLabel").grid(row=2, column=1)

ttk.Label(outputFrame, text="CPU Utilization").grid(
    row=3, column=0, sticky="w")
ttk.Label(outputFrame, textvariable=CPUUtil,
          style="Value.TLabel").grid(row=3, column=1)

ttk.Label(outputFrame, text="Error Rate").grid(row=4, column=0, sticky="w")
ttk.Label(outputFrame, textvariable=errorR,
          style="Value.TLabel").grid(row=4, column=1)

root.mainloop()
