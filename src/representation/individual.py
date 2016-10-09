from algorithm.mapper import mapper
from fitness.default_fitness import default_fitness
from parameters.parameters import params


class Individual(object):
    """
    A GE individual.
    """

    def __init__(self, genome, ind_tree, map_ind=True):
        """
        Initialise an instance of the individual class (i.e. create a new
        individual).
        
        :param genome: An individual's genome.
        :param ind_tree: An individual's derivation tree, i.e. an instance
        of the representation.tree.Tree class.
        :param map_ind: A boolean flag that indicates whether or not an
        individual needs to be mapped.
        """
        
        if map_ind:
            # The individual needs to be mapped from the given input
            # parameters.
            self.phenotype, self.genome, self.tree, self.nodes, self.invalid, \
                self.depth, self.used_codons = mapper(genome, ind_tree)
        
        else:
            # The individual does not need to be mapped.
            self.genome, self.tree = genome, ind_tree
        
        self.fitness = default_fitness(params['FITNESS_FUNCTION'].maximise)
        self.name = None

    def __lt__(self, other):
        """
        Set the definition for comparison of two instances of the individual
        class by their fitness values. Allows for sorting/ordering of a
        population of individuals.
        
        :param other: Another instance of the individual class (i.e. another
        individual) with which to compare.
        :return: Whether or not the fitness of the current individaul is
        greater than the comparison individual.
        """
        
        if params['FITNESS_FUNCTION'].maximise:
            return self.fitness < other.fitness
        else:
            return other.fitness < self.fitness

    def __str__(self):
        """
        Generates a string by which individuals can be identified. Useful
        for printing information about individuals.
        
        :return: A string describing the individual.
        """
        return ("Individual: " +
                str(self.phenotype) + "; " + str(self.fitness))
    
    def deep_copy(self):
        """
        Copy an individual and return a unique version of that individual.
        
        :return: A unique copy of the individual.
        """

        if not params['GENOME_OPERATIONS']:
            # Create a new unique copy of the tree.
            new_tree = self.tree.__copy__()

        else:
            new_tree = None
        
        # Create a copy of self by initialising a new individual.
        new_ind = Individual(list(self.genome), new_tree, map_ind=False)
        
        # Set new individaul parameters (no need to map genome to new
        # individual).
        new_ind.phenotype, new_ind.invalid = self.phenotype, self.invalid
        new_ind.depth, new_ind.nodes = self.depth, self.nodes
        new_ind.used_codons = self.used_codons
        
        return new_ind

    def evaluate(self, dist="training"):
        """
        Evaluates phenotype in using the fitness function set in the params
        dictionary. For regression/classification problems, allows for
        evaluation on either training or test distributions. Sets fitness
        value.
        
        :param dist: An optional parameter for problems with training/test
        data. Specifies the distribution (i.e. training or test) upon which
        evaluation is to be performed.
        :return: Nothing unless multicore evaluation is being used. In that
        case, returns self.
        """

        if hasattr(params['FITNESS_FUNCTION'], "training_test"):
            # The problem has training and test data. These fitness functions
            # need an extra input parameter specifying the distribution upon
            # which to be evaluated.
            self.fitness = params['FITNESS_FUNCTION'](self.phenotype, dist)

        else:
            # Evaluate fitness using specified fitness function.
            self.fitness = params['FITNESS_FUNCTION'](self.phenotype)

        if params['MULTICORE']:
            return self
