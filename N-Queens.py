import tkinter as tk
from tkinter import ttk, messagebox
import random
# Genetic Algorithm Helper Functions
def generateRandomChromosome(numberOfQueens):
    return [random.randint(1, numberOfQueens) for _ in range(numberOfQueens)]

def calculateFitness(chromosome):
    horizontalCollisions = sum([chromosome.count(queen) - 1 for queen in chromosome]) / 2
    numQueens = len(chromosome)
    leftDiagonal = [0] * 2 * numQueens
    rightDiagonal = [0] * 2 * numQueens
    for index in range(numQueens):
        leftDiagonal[index + chromosome[index] - 1] += 1
        rightDiagonal[len(chromosome) - index + chromosome[index] - 2] += 1
    diagonalCollisions = 0
    for index in range(2 * numQueens - 1):
        collisions = 0
        if leftDiagonal[index] > 1:
            collisions += leftDiagonal[index] - 1
        if rightDiagonal[index] > 1:
            collisions += rightDiagonal[index] - 1
        diagonalCollisions += collisions / (numQueens - abs(index - numQueens + 1))
    return int(maxFitness - (horizontalCollisions + diagonalCollisions))


def calculateProbability(chromosome, fitnessFunction):
    return fitnessFunction(chromosome) / maxFitness


def selectChromosome(population, probabilities):
    populationWithProbabilities = zip(population, probabilities)
    totalWeight = sum(probability for _, probability in populationWithProbabilities)
    randomValue = random.uniform(0, totalWeight)
    currentWeight = 0
    for individual, weight in zip(population, probabilities):
        if currentWeight + weight >= randomValue:
            return individual
        currentWeight += weight
    assert False, "Selection failed!"


def performCrossover(parent1, parent2):
    chromosomeLength = len(parent1)
    crossoverPoint = random.randint(0, chromosomeLength - 1)
    return parent1[0:crossoverPoint] + parent2[crossoverPoint:]


def applyMutation(chromosome):
    chromosomeLength = len(chromosome)
    mutationPoint = random.randint(0, chromosomeLength - 1)
    newGeneValue = random.randint(1, chromosomeLength)
    chromosome[mutationPoint] = newGeneValue
    return chromosome


def geneticAlgorithmSolver(population, fitnessFunction):
    mutationProbability = 0.03
    nextGeneration = []
    probabilities = [calculateProbability(individual, fitnessFunction) for individual in population]
    for _ in range(len(population)):
        parent1 = selectChromosome(population, probabilities)
        parent2 = selectChromosome(population, probabilities)
        offspring = performCrossover(parent1, parent2)
        if random.random() < mutationProbability:
            offspring = applyMutation(offspring)
        nextGeneration.append(offspring)
        if fitnessFunction(offspring) == maxFitness:
            break
    return nextGeneration


# GUI Logic
def startSolver():
    global maxFitness, stopSolverFlag
    stopSolverFlag = False

    try:
        numberOfQueens = int(entryInput.get())
        if numberOfQueens < 4:
            messagebox.showerror("Error", "No solution exists for N < 4!")
            return

        maxFitness = (numberOfQueens * (numberOfQueens - 1)) / 2
        initialPopulation = [generateRandomChromosome(numberOfQueens) for _ in range(100)]
        generationCounter = 1

        def solve():
            nonlocal generationCounter, initialPopulation
            if stopSolverFlag:
                return  # Stop execution if stopSolverFlag is set

            # Calculate fitness of each individual
            fitnessValues = [calculateFitness(chromosome) for chromosome in initialPopulation]
            
            # Check if any chromosome has the max fitness (solution found)
            if maxFitness in fitnessValues:
                solution = initialPopulation[fitnessValues.index(maxFitness)]
                generationLabel.config(text=f"Solution Found in Generation {generationCounter}!")
                displayChessboard(solution, numberOfQueens)
                return  # Exit after finding the solution

            # Continue if solution is not found
            generationLabel.config(text=f"Running Generation: {generationCounter}")
            generationCounter += 1
            initialPopulation = geneticAlgorithmSolver(initialPopulation, calculateFitness)

            # Get the best chromosome of the current generation
            bestChromosome = max(initialPopulation, key=calculateFitness)
            displayChessboard(bestChromosome, numberOfQueens)

            # Schedule the next iteration if no solution is found yet
            root.after(200, solve)

        solve()

    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number!")


def stopSolver():
    global stopSolverFlag
    stopSolverFlag = True
    generationLabel.config(text="Solver Stopped")

def displayChessboard(chromosome, numberOfQueens):
    for widget in chessboardFrame.winfo_children():
        widget.destroy()

    for row in range(numberOfQueens):
        for column in range(numberOfQueens):
            backgroundColor = "#fff" if (row + column) % 2 == 0 else "#bbb"
            textContent = "Q" if chromosome[column] - 1 == row else ""
            cellLabel = tk.Label(
                chessboardFrame,
                text=textContent,
                bg=backgroundColor,
                fg="red" if textContent == "Q" else "black",
                width=4,
                height=2,
                font=("Arial", 14),
                relief="solid",
                borderwidth=1,
            )
            cellLabel.grid(row=row, column=column)


# GUI Components
root = tk.Tk()
root.title("N-Queens Genetic Algorithm")
root.geometry("1000x700")

headerLabel = tk.Label(root, text="N-Queens Solver using Genetic Algorithm", font=("Arial", 18, "bold"), bg="#4CAF50", fg="white")
headerLabel.pack(fill=tk.X, pady=10)

inputFrame = tk.Frame(root, pady=20)
inputFrame.pack()

entryLabel = tk.Label(inputFrame, text="Enter Number of Queens (N):", font=("Arial", 14))
entryLabel.grid(row=0, column=0, padx=10)

entryInput = ttk.Entry(inputFrame, font=("Arial", 14), width=10)
entryInput.grid(row=0, column=1, padx=10)

startButton = tk.Button(inputFrame, text="Start", command=startSolver, font=("Arial", 14), bg="#4CAF50", fg="white")
startButton.grid(row=0, column=2, padx=10)

stopButton = tk.Button(inputFrame, text="Stop", command=stopSolver, font=("Arial", 14), bg="#f44336", fg="white")
stopButton.grid(row=0, column=3, padx=10)

generationLabel = tk.Label(root, text="Waiting for input...", font=("Arial", 14))
generationLabel.pack(pady=10)

chessboardFrame = tk.Frame(root, bg="#eee", relief="solid", borderwidth=2)
chessboardFrame.pack(pady=20)

footerLabel = tk.Label(root, text="Visualization powered by Genetic Algorithm | Designed by Team MTA", font=("Arial", 10), bg="#4CAF50", fg="white")
footerLabel.pack(fill=tk.X, side=tk.BOTTOM, pady=10)

root.mainloop()
