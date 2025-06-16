#######################################
# Configure this according to your spec
#######################################
# number of runs
num_runs = 3
# number of hours per run
runtime = 12
# number of cores
cores = 26


#######################################
# Dont change this part
#######################################
# number of targets per sample
targets_1_1 = 33
targets_1_2 = 6
targets_2 = 15
targets_3 = 10
targets_4 = 6
targets_5 = 44


def compute_runtime(num_targets):
    total_executions = num_targets*num_runs
    executions_per_cpu = total_executions//cores
    remainder = total_executions % cores
    if remainder != 0:
        executions_per_cpu += 1
    final = executions_per_cpu * runtime
    return final

print("Estimated runtime for experiment 1-1")
r11 = compute_runtime(targets_1_1)
print(f"Estimated runtime: {r11}h")
print("Estimated runtime for experiment 1-2")
r12 = 2*compute_runtime(targets_1_2)
print(f"Estimated runtime: {r12}h")
print("Estimated runtime for experiment 2")
r2 = 2*compute_runtime(targets_2)
print(f"Estimated runtime: {r2}h")
print("Estimated runtime for experiment 3")
r3 = 2*compute_runtime(targets_3)
print(f"Estimated runtime: {r3}h")
print("Estimated runtime for experiment 4")
r4 = 2*compute_runtime(targets_4)
print(f"Estimated runtime: {r4}h")
print("Estimated runtime for experiment 5")
r5 = compute_runtime(targets_5)
print(f"Estimated runtime: {r5}h")

s = r11 + r12 + r2 + r3 + r4 + r5
d = s/24
print(f"Final estimated runtime: {s}h, which is {d} days")

