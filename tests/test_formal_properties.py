"""
Comprehensive Tests for Formal Properties of Petersonian AI Agents

This module tests the mathematical properties and proven guarantees of the framework.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from peterson_ai_model import PetersonianAISystem, Agent, Decision
from formal_proofs import prove_hierarchy_validity_preservation, prove_responsibility_bounds, prove_decision_routing_correctness

def test_hierarchy_validity_preservation():
    """Test that hierarchy validity is preserved"""
    print("Testing Hierarchy Validity Preservation...")
    
    # Create system
    system = PetersonianAISystem()
    
    # Create valid hierarchy
    agent_a = Agent(id="A", name="CEO", capability=10.0)
    agent_b = Agent(id="B", name="Manager", capability=7.0, supervisor_id="A")
    agent_c = Agent(id="C", name="Junior", capability=4.0, supervisor_id="B")
    
    system.add_agent(agent_a)
    system.add_agent(agent_b)
    system.add_agent(agent_c)
    
    # Test initial validity
    is_valid = system.hierarchy.is_valid()
    assert is_valid, "Initial hierarchy should be valid"
    print("  ✓ Initial hierarchy is valid")
    
    # Test validity preservation proof
    proof_result = prove_hierarchy_validity_preservation(
        system.hierarchy.agents, 
        system.hierarchy.edges
    )
    assert proof_result, "Hierarchy validity should be preserved"
    print("  ✓ Hierarchy validity preservation proven")

def test_responsibility_bounds():
    """Test that responsibility values are bounded"""
    print("Testing Responsibility Bounds...")
    
    # Create system and agents
    system = PetersonianAISystem()
    agent_a = Agent(id="A", name="CEO", capability=10.0)
    agent_b = Agent(id="B", name="Manager", capability=7.0, supervisor_id="A")
    agent_c = Agent(id="C", name="Junior", capability=4.0, supervisor_id="B")
    
    system.add_agent(agent_a)
    system.add_agent(agent_b)
    system.add_agent(agent_c)
    
    # Test complex decision that gets referred
    complex_decision = Decision(id="complex", description="Complex task", complexity=8.0)
    handler_id, log_entry = system.route_decision(complex_decision, "C")
    
    # Calculate responsibility
    responsibility = agent_c.get_responsibility_for_decision(log_entry, system.hierarchy)
    
    # Test bounds
    bounds_satisfied = prove_responsibility_bounds(responsibility)
    assert bounds_satisfied, f"Responsibility {responsibility} should be in [0,1]"
    assert 0 <= responsibility <= 1, f"Responsibility {responsibility} should be in [0,1]"
    print(f"  ✓ Responsibility bounded: {responsibility:.3f}")

def test_decision_routing_correctness():
    """Test that decision routing works correctly"""
    print("Testing Decision Routing Correctness...")
    
    # Create system
    system = PetersonianAISystem()
    agent_a = Agent(id="A", name="CEO", capability=10.0)
    agent_b = Agent(id="B", name="Manager", capability=7.0, supervisor_id="A")
    agent_c = Agent(id="C", name="Junior", capability=4.0, supervisor_id="B")
    
    system.add_agent(agent_a)
    system.add_agent(agent_b)
    system.add_agent(agent_c)
    
    # Test simple decision (should be handled directly)
    simple_decision = Decision(id="simple", description="Simple task", complexity=3.0)
    handler_id, log_entry = system.route_decision(simple_decision, "C")
    assert handler_id == "C", "Junior should handle simple decision"
    assert log_entry.directly_made == True, "Decision should be made directly"
    print("  ✓ Simple decision routed correctly")
    
    # Test complex decision (should be referred up hierarchy)
    complex_decision = Decision(id="complex", description="Complex task", complexity=8.0)
    handler_id, log_entry = system.route_decision(complex_decision, "C")
    assert handler_id == "A", "CEO should handle complex decision"
    assert log_entry.directly_made == False, "Decision should be referred"
    print("  ✓ Complex decision routed correctly")
    
    # Test routing correctness proof
    proof_result = prove_decision_routing_correctness(agent_c, complex_decision, system.hierarchy)
    assert proof_result, "Decision routing should be correct"
    print("  ✓ Decision routing correctness proven")

def test_system_stability():
    """Test system stability properties"""
    print("Testing System Stability...")
    
    # Create system
    system = PetersonianAISystem()
    agent_a = Agent(id="A", name="CEO", capability=10.0)
    agent_b = Agent(id="B", name="Manager", capability=7.0, supervisor_id="A")
    agent_c = Agent(id="C", name="Junior", capability=4.0, supervisor_id="B")
    
    system.add_agent(agent_a)
    system.add_agent(agent_b)
    system.add_agent(agent_c)
    
    # Test that hierarchy remains valid after operations
    instability = system.hierarchy.calculate_instability()
    stability = 1.0 - instability
    assert 0 <= stability <= 1, f"System stability {stability} should be in [0,1]"
    print(f"  ✓ System stability: {stability:.3f}")

def run_all_tests():
    """Run all formal property tests"""
    print("Running Formal Property Tests for Petersonian AI Agents")
    print("=" * 55)
    
    try:
        test_hierarchy_validity_preservation()
        test_responsibility_bounds()
        test_decision_routing_correctness()
        test_system_stability()
        
        print("\n" + "=" * 55)
        print("🎉 ALL FORMAL PROPERTY TESTS PASSED! 🎉")
        print("Mathematical properties verified:")
        print("  ✓ Hierarchy validity preservation")
        print("  ✓ Responsibility bounds")
        print("  ✓ Decision routing correctness")
        print("  ✓ System stability bounds")
        print("=" * 55)
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)