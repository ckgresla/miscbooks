# Create a Graph of Performances w Label Annotations 

import matplotlib.pyplot as plt


# Evaluation Runs Data
x = ["06.01"]
y = [1.22]
n = ["starchat-V1-LoRA"]

fig, ax = plt.subplots()
ax.scatter(x, y, color="black")

# Add Labels
for i, txt in enumerate(n):
    txt += f" @ {y[i]}%"
    ax.annotate(txt, (x[i], y[i]),
                ha="center", va="bottom",
                xytext=(x[i], y[i]+2.3)
    )


# Graph Labels & Axis Dims
plt.title('CAP Evaluation -- MVP Cases')
plt.xlabel("Date of Evaluation (2023)")
plt.ylabel("% Correct on Benchmark")
plt.ylim(0.0, 100)

plt.show()

