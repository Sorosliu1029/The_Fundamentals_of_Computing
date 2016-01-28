"""
Provided code for application portion of module 1

Helper class for implementing efficient version
of DPA algorithm
"""

# general imports
import random
import matplotlib.pyplot as plt
import project_degree_distributions_for_graphs as provided


class DPATrial:
    """
    Simple class to encapsulate optimized trials for DPA algorithm
    
    Maintains a list of node numbers with multiple instances of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a DPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_node trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that the number of instances of
        each node number is in the same ratio as the desired probabilities
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for dummy_idx in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors
    

def DPA(num_nodes, new_neigh_num):
    trial = DPATrial(new_neigh_num)
    result = provided.make_complete_graph(new_neigh_num)
    for new_add_node in range(new_neigh_num, num_nodes):
        new_neigh_set = trial.run_trial(new_neigh_num)
        result[new_add_node] = new_neigh_set
    return result

graph = DPA(27770, 1)
unnor_in_degree_dstr = provided.in_degree_distribution(graph)
in_degree_sum = sum(unnor_in_degree_dstr.values())
nor_in_degree_dsrt = [value / float(in_degree_sum) for value in unnor_in_degree_dstr.values()]
plt.plot(unnor_in_degree_dstr.keys(), nor_in_degree_dsrt, 'ro')
plt.yscale('log')
plt.xscale('log')
plt.xlabel('log of in-degree')
plt.ylabel('log of the normalized distribution')
plt.title('DPA Graph')
plt.show()
