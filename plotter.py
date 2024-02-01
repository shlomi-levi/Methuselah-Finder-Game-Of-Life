import matplotlib.pyplot as plt
from constants import SAVE_FILE_NAME
import pickle
from ResultsFormat import Result

def plot_best_fitness_by_generation(r:Result):
    dots = [(i + 1, chromosome.evaluation_value) for i, chromosome in enumerate(r.best_by_generation)]

    plot('Best Fitness Over Generations Of The Genetic Algorithm', 'Generation', 'Fitness', dots)

def plot_all_chromosomes_fitness(r:Result):
    dots = []
    i = 0

    for evaluation_list in r.evaluation_list_by_generation:
        i += 1
        for evaluation_value in evaluation_list:
            dots.append( (i, evaluation_value) )

    plot('Fitness Over Generations Of The Genetic Algorithm', 'Generation', 'Fitness', dots)

def plot_avg_fitness_by_generation(r:Result):
    dots = []
    i = 0

    for evaluation_list in r.evaluation_list_by_generation:
        i += 1
        dots.append( (i, sum(evaluation_list) / len(evaluation_list) ))

    plot('Average Fitness Over Generations Of The Genetic Algorithm', 'Generation', 'Fitness', dots)

def plot(title, xlabel, ylabel, dots):
    for dot in dots:
        plt.scatter(dot[0], dot[1], marker='o', color='blue')

    # Customize the plot
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(False)
    # plt.legend()

    plt.show()

def main():
    try:
        with open(SAVE_FILE_NAME, 'rb') as file:
            data = pickle.load(file)

    except Exception as error:
        print(error)
        exit()

    # plot_best_fitness_by_generation(data)
    # plot_all_chromosomes_fitness(data)
    plot_avg_fitness_by_generation(data)


if __name__ == '__main__':
    main()
