from multiprocessing import Process
import matplotlib.pyplot as plt


def process_show(
    x,
    monitor_execution_times,
    analyse_execution_times,
    planning_execution_times,
    execute_execution_times,
):
    plt.figure(figsize=(10, 6))

    plt.plot(x, monitor_execution_times, label="monitor execution times", color="blue")
    plt.plot(
        x,
        analyse_execution_times,
        label="analyse execution times",
        color="orange",
    )
    plt.plot(
        x,
        planning_execution_times,
        label="planning execution times",
        color="green",
    )
    plt.plot(x, execute_execution_times, label="execute execution times", color="red")

    plt.title("Time Results of the MAPE Cycle")
    plt.xlabel("MAPE iteration")
    plt.ylabel("Time")
    plt.ylim(-0.02, 0.2)
    plt.axhline(0, color="black", linewidth=0.5, ls="--")
    plt.axvline(0, color="black", linewidth=0.5, ls="--")
    plt.grid()
    plt.legend()
    plt.show()


def show(
    x,
    monitor_execution_times,
    analyse_execution_times,
    planning_execution_times,
    execute_execution_times,
):
    process = Process(
        target=process_show,
        args=(
            x,
            monitor_execution_times,
            analyse_execution_times,
            planning_execution_times,
            execute_execution_times,
        ),
    )
    process.start()
