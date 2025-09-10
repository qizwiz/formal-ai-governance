from src.peterson_ai_model import PetersonianAISystem, Agent, Decision

def run_simple_validation():
    """Run a simple validation example"""
    print("Running Simple Validation Example for Petersonian AI Model")
    print("=" * 50)
    
    # Create system
    system = PetersonianAISystem()
    
    # Create agents with capabilities
    agent_a = Agent(id="A", name="CEO", capability=10.0)
    agent_b = Agent(id="B", name="Manager", capability=7.0, supervisor_id="A")
    agent_c = Agent(id="C", name="Junior", capability=4.0, supervisor_id="B")
    
    # Add agents to system
    system.add_agent(agent_a)
    system.add_agent(agent_b)
    system.add_agent(agent_c)
    
    print("Initial Agent Capabilities:")
    print(f"  Agent A (CEO): {agent_a.capability}")
    print(f"  Agent B (Manager): {agent_b.capability}")
    print(f"  Agent C (Junior): {agent_c.capability}")
    print()
    
    # Check hierarchy validity
    print(f"Hierarchy Valid: {system.hierarchy.is_valid()}")
    print()
    
    # Create decisions
    simple_decision = Decision(id="simple", description="Simple task", complexity=3.0)
    complex_decision = Decision(id="complex", description="Complex task", complexity=8.0)
    
    # Test decision routing
    print("Decision Routing Examples:")
    print("-" * 30)
    
    # Simple decision should be handled by Junior
    print("1. Agent C receives simple task (complexity=3.0):")
    handler_id, log_entry = system.route_decision(simple_decision, "C")
    handler = system.hierarchy.agents[handler_id]
    print(f"   Decision handled by: {handler.name}")
    print(f"   Handled directly: {log_entry.directly_made}")
    print()
    
    # Complex decision should be referred to CEO
    print("2. Agent C receives complex task (complexity=8.0):")
    handler_id, log_entry = system.route_decision(complex_decision, "C")
    handler = system.hierarchy.agents[handler_id]
    print(f"   Decision handled by: {handler.name}")
    print(f"   Handled directly: {log_entry.directly_made}")
    if not log_entry.directly_made:
        print(f"   Referred from: Agent C to Agent B to Agent A")
    print()
    
    # Test performance evaluation
    print("Performance Evaluation:")
    print("-" * 20)
    
    # Add some decisions with outcomes
    decision1 = Decision(id="d1", description="Task 1", complexity=2.0, outcome=True)
    decision2 = Decision(id="d2", description="Task 2", complexity=2.0, outcome=False)
    decision3 = Decision(id="d3", description="Task 3", complexity=2.0, outcome=True)
    
    system.add_decision(decision1)
    system.add_decision(decision2)
    system.add_decision(decision3)
    system.route_decision(decision1, "C")
    system.route_decision(decision2, "C")
    system.route_decision(decision3, "C")
    
    performance = agent_c.calculate_performance()
    print(f"Agent C performance: {performance:.2f}")
    
    # Test accountability
    accountability = agent_c.calculate_accountability()
    print(f"Agent C accountability: {accountability:.2f}")
    
    # Test citizenship score
    max_knowledge = system.get_max_knowledge_contribution() if hasattr(system, 'get_max_knowledge_contribution') else 1.0
    citizenship = agent_c.calculate_citizenship_score(max_knowledge)
    print(f"Agent C citizenship score: {citizenship:.2f}")
    
    print("\nSimple validation example complete!")

if __name__ == "__main__":
    run_simple_validation()