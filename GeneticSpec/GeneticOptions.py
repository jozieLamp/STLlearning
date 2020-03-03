
#Class to handle specific parameteters of genetic algorithm learning process
class GeneticOptions:
    def __init__(self):

        self.initialPopSize = 50
        self.max_num_rand = 10
        self.use_or = False
        self.number_generations = 3

        self.threshold_name = "Theta"
        self.solution_set_size = 10
        #can be one of "regularised_logodds", "logodds"
        self.fitness_type = "regularised_logodds"
        self.size_penalty_coefficient = 1
        self.undefined_reference_threshold = 0.1


        self.init__max_number_of_atoms = 3

        self.init__random_number_of_atoms = False
        self.init__average_number_of_atoms = 3
        self.init__fixed_number_of_atoms = 2
        self.init__prob_of_less_than = 0.5
        self.init__prob_of_true_atom = 0 #0.01
        self.init__and_weight = 1
        self.init__or_weight = 1
        self.init__not_weight = 1
        self.init__imply_weight = 1
        self.init__eventually_weight = 1
        self.init__globally_weight = 1
        self.init__until_weight = 1
        self.init__eventuallyglobally_weight = 1
        self.init__globallyeventually_weight = 1

        self.min_time_bound = 0
        self.max_time_bound = 100

        self.mutate__one_node = True
        self.mutate__mutation_probability_per_node = 0.01
        self.mutate__mutation_probability_one_node = 1 # 0.05
        self.mutate__insert__weight = 2
        self.mutate__delete__weight = 2
        self.mutate__replace__weight = 4
        self.mutate__change__weight = 1

        self.mutate__delete__keep_left_node = 0.5

        self.mutate__insert__eventually_weight = 2
        self.mutate__insert__globally_weight = 2
        self.mutate__insert__negation_weight = 1

        self.mutate__replace__modal_to_modal_weight = 3
        self.mutate__replace__modal_to_bool_weight = 1
        self.mutate__replace__bool_to_modal_weight = 1
        self.mutate__replace__bool_to_bool_weight = 3
        self.mutate__replace__keep_left_node = 0.5

        self.mutate__replace__eventually_weight = 1
        self.mutate__replace__globally_weight = 1
        self.mutate__replace__until_weight = 1
        self.mutate__replace__and_weight = 1
        self.mutate__replace__or_weight = 1
        self.mutate__replace__imply_weight = 1
        self.mutate__replace__not_weight = 1
        self.mutate__replace__new_left_node_for_boolean = 0.5
        self.mutate__replace__new_left_node_for_until = 0.5
        self.mutate__replace__new_left_node_for_until_from_globally = 0.05
        self.mutate__replace__new_left_node_for_until_from_eventually = 0.95

        self.mutate__change__prob_lower_bound = 0.5
        self.mutate__change__proportion_of_variation = 0.1

    #Takes two arrays of doubles
    def discriminationFunction(self, x, y):
        return (x[0] - y[0]) / abs(x[1] + y[1])


        #takes array  of doubles of x and  y as input
        #returns double


        #BiFunction <double[], double[], Double> DISCRIMINATION_FUNCTION = (x, y) -> (x[0] - y[0]) / (Math.abs(x[1] + y[1]));
