"""A Node object.

This module represents a node in a network.
"""

class Node:
    """Node class to store node and relevant information
    
    Attributes:
    ---------
        radius: lowest radius that this node is a part of
        measure: assigned measure for node
        path: shortest path from source
        name: label for node
    """
    
    def __init__(self):
        self.radius = 0
        self.measure = 0
        self.path = []
        self.name = None

    def __str__(self):
        return f"node {self.name}, radius {self.radius}"
    
    def __repr__(self):
        return f"node {self.name}, radius {self.radius}, measure {self.measure}"