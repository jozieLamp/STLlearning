#Class to handle specific parameteters of genetic algorithm learning process
class GeneticOptions:
    def __init__(self):
        initialPopSize = 50

        threshold_name = "Theta"
        solution_set_size = 10
        #can be one of "regularised_logodds", "logodds"
        fitness_type = "regularised_logodds"
        size_penalty_coefficient = 1
        undefined_reference_threshold = 0.1

        init__random_number_of_atoms = False
        init__average_number_of_atoms = 3
        init__fixed_number_of_atoms = 2
        init__prob_of_less_than = 0.5
        init__prob_of_true_atom = 0 #0.01
        init__and_weight = 1
        init__or_weight = 1
        init__not_weight = 1
        init__imply_weight = 1
        init__eventually_weight = 1
        init__globally_weight = 1
        init__until_weight = 1
        init__eventuallyglobally_weight = 1
        init__globallyeventually_weight = 1

        min_time_bound = 0
        max_time_bound = 100

        mutate__one_node = True
        mutate__mutation_probability_per_node = 0.01
        mutate__mutation_probability_one_node = 1 # 0.05
        mutate__insert__weight = 2
        mutate__delete__weight = 2
        mutate__replace__weight = 4
        mutate__change__weight = 0

        mutate__delete__keep_left_node = 0.5

        mutate__insert__eventually_weight = 2
        mutate__insert__globally_weight = 2
        mutate__insert__negation_weight = 1

        mutate__replace__modal_to_modal_weight = 3
        mutate__replace__modal_to_bool_weight = 1
        mutate__replace__bool_to_modal_weight = 1
        mutate__replace__bool_to_bool_weight = 3
        mutate__replace__keep_left_node = 0.5

        mutate__replace__eventually_weight = 1
        mutate__replace__globally_weight = 1
        mutate__replace__until_weight = 1
        mutate__replace__and_weight = 1
        mutate__replace__or_weight = 1
        mutate__replace__imply_weight = 1
        mutate__replace__not_weight = 1
        mutate__replace__new_left_node_for_boolean = 0.5
        mutate__replace__new_left_node_for_until = 0.5
        mutate__replace__new_left_node_for_until_from_globally = 0.05
        mutate__replace__new_left_node_for_until_from_eventually = 0.95

        mutate__change__prob_lower_bound = 0.5
        mutate__change__proportion_of_variation = 0.1