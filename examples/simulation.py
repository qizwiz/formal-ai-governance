import random
from peterson_ai_agent import PetersonAgent, AgentCapability, EthicalRule
from typing import List

class AgentHierarchySimulation:
    def __init__(self):
        self.agents: List[PetersonAgent] = []
        self.initialize_hierarchy()
    
    def initialize_hierarchy(self):
        """Initialize a hierarchy of agents with different capability levels"""
        # Create top-level agent (high capability)
        ceo = PetersonAgent("CEO", AgentCapability.HIGH)
        self.agents.append(ceo)
        
        # Create middle management (medium capability) reporting to CEO
        manager1 = PetersonAgent("Manager-1", AgentCapability.MEDIUM, supervisor=ceo)
        manager2 = PetersonAgent("Manager-2", AgentCapability.MEDIUM, supervisor=ceo)
        self.agents.extend([manager1, manager2])
        
        # Create junior agents (low capability) reporting to managers
        junior1 = PetersonAgent("Junior-1", AgentCapability.LOW, supervisor=manager1)
        junior2 = PetersonAgent("Junior-2", AgentCapability.LOW, supervisor=manager1)
        junior3 = PetersonAgent("Junior-3", AgentCapability.LOW, supervisor=manager2)
        junior4 = PetersonAgent("Junior-4", AgentCapability.LOW, supervisor=manager2)
        self.agents.extend([junior1, junior2, junior3, junior4])
        
        print("Agent hierarchy initialized:")
        print(f"  {ceo}")
        print(f"    {manager1}")
        print(f"      {junior1}")
        print(f"      {junior2}")
        print(f"    {manager2}")
        print(f"      {junior3}")
        print(f"      {junior4}")
        print()
    
    def run_simulation(self, rounds: int = 5):
        """Run the simulation for a specified number of rounds"""
        print(f"Running simulation for {rounds} rounds...\n")
        
        # Sample decisions of varying complexity
        decisions = [
            "Process routine customer inquiry",
            "Handle standard refund request",
            "Update product documentation",
            "Evaluate new marketing strategy",
            "Respond to critical system failure",
            "Make strategic partnership decision",
            "Address ethical dilemma with supplier",
            "Handle high-stakes financial investment"
        ]
        
        for round_num in range(rounds):
            print(f"--- Round {round_num + 1} ---")
            
            # Select a random agent to make a decision
            agent = random.choice(self.agents)
            
            # Select a random decision
            decision = random.choice(decisions)
            
            # Create context for the decision
            context = {
                "round": round_num + 1,
                "agent": agent.name,
                "timestamp": f"Round {round_num + 1}"
            }
            
            # Agent makes decision
            print(f"{agent.name} making decision: '{decision}'")
            decision_log = agent.make_decision(decision, context)
            print(f"Result: {decision_log.outcome.value}")
            print()
            
            # Occasionally have agents reflect on performance
            if random.random() < 0.3:  # 30% chance
                agent.reflect_on_performance()
            
            # Occasionally have agents propose rule changes
            if random.random() < 0.1:  # 10% chance
                agent.propose_rule_change(
                    # In a real implementation, this would be more sophisticated
                    EthicalRule(
                        rule_id=f"rule_{random.randint(1000, 9999)}",
                        description=f"New rule about {random.choice(['transparency', 'accountability', 'fairness', 'sustainability'])}",
                        priority=random.randint(1, 5)
                    )
                )
            
            print()
        
        self.print_summary()
    
    def print_summary(self):
        """Print a summary of the simulation"""
        print("=== SIMULATION SUMMARY ===")
        print("Final agent capabilities and performance:")
        for agent in self.agents:
            print(f"  {agent}")
        
        print("\nSample decision logs:")
        # Show last few decision logs from different agents
        logs_shown = 0
        for agent in self.agents:
            if agent.decision_logs and logs_shown < 10:
                print(f"  From {agent.name}:")
                for log in agent.decision_logs[-2:]:  # Last 2 decisions
                    print(f"    {log}")
                logs_shown += len(agent.decision_logs[-2:])

def main():
    """Main function to run the simulation"""
    print("Petersonian AI Agent Hierarchy Simulation")
    print("=========================================")
    print()
    
    # Create and run simulation
    simulation = AgentHierarchySimulation()
    simulation.run_simulation(rounds=10)
    
    print("\nSimulation complete.")

if __name__ == "__main__":
    main()