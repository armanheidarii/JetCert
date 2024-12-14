from multiprocessing import Process
import matplotlib.pyplot as plt


def process_show(x, overall_execution_times):
    plt.figure(figsize=(10, 6))

    plt.plot(
        x,
        overall_execution_times,
        label="overall execution times",
        color="red",
    )

    plt.title("Time Results of the MAPE Cycles")
    plt.xlabel("MAPE iteration")
    plt.ylabel("Time")
    plt.ylim(-0.2, 4)
    plt.axhline(0, color="black", linewidth=0.5, ls="--")
    plt.axvline(0, color="black", linewidth=0.5, ls="--")
    plt.grid()
    plt.legend()
    plt.show()


def show(x, overall_execution_times):
    process = Process(target=process_show, args=(x, overall_execution_times))
    process.start()
