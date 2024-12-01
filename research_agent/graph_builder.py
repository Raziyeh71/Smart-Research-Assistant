import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Dict

class GraphBuilder:
    def __init__(self):
        self.graph = nx.Graph()
        
    def update_graph(self, query: str, findings: List[tuple]):
        """
        Update the knowledge graph with new findings
        """
        # Add query node
        self.graph.add_node(query, type='query')
        
        # Add findings and connect to query
        for item, summary in findings:
            if isinstance(item, dict):
                # Get title based on whether it's a paper or GitHub project
                title = item.get('title', item.get('full_name', 'Unknown'))
                
                # Add node for the finding
                self.graph.add_node(title, 
                                  type='paper' if 'title' in item else 'project',
                                  summary=summary)
                
                # Connect to query
                self.graph.add_edge(query, title)
                
                # Add connections based on common topics/keywords
                self._add_topic_connections(title, item)
    
    def _add_topic_connections(self, title: str, item: Dict):
        """
        Add connections between nodes based on common topics
        """
        # Extract topics/keywords
        topics = []
        if 'topics' in item:  # GitHub project
            topics = item['topics']
        elif 'abstract' in item:  # Academic paper
            # Simple keyword extraction from abstract
            # In a real implementation, you might want to use a proper keyword extraction algorithm
            topics = [word.lower() for word in item['abstract'].split() 
                     if len(word) > 5][:5]
        
        # Add edges between nodes with common topics
        for node in self.graph.nodes():
            if node != title and self.graph.nodes[node].get('type') in ['paper', 'project']:
                node_topics = self.graph.nodes[node].get('topics', [])
                common_topics = set(topics) & set(node_topics)
                if common_topics:
                    self.graph.add_edge(title, node, topics=list(common_topics))
    
    def visualize(self):
        """
        Visualize the knowledge graph
        """
        plt.figure(figsize=(12, 8))
        
        # Create layout
        pos = nx.spring_layout(self.graph)
        
        # Draw nodes
        node_colors = []
        for node in self.graph.nodes():
            if self.graph.nodes[node]['type'] == 'query':
                node_colors.append('lightblue')
            elif self.graph.nodes[node]['type'] == 'paper':
                node_colors.append('lightgreen')
            else:  # project
                node_colors.append('lightcoral')
        
        nx.draw_networkx_nodes(self.graph, pos, node_color=node_colors)
        nx.draw_networkx_edges(self.graph, pos)
        nx.draw_networkx_labels(self.graph, pos)
        
        plt.title("Research Knowledge Graph")
        plt.axis('off')
        plt.show()
