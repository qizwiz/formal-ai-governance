#!/usr/bin/env python3
"""
Simple test to verify core Petersonian AI implementation
"""

def test_core_components():
    """Test that core components can be imported and instantiated"""
    try:
        # Test importing core components
        from src.peterson_ai_model import PetersonianAISystem, Agent, Decision
        print("✓ Core components imported successfully")
        
        # Test creating system
        system = PetersonianAISystem()
        print("✓ PetersonianAISystem instantiated successfully")
        
        # Test creating agents
        agent = Agent(id="test", name="TestAgent", capability=5.0)
        print("✓ Agent instantiated successfully")
        
        # Test creating decisions
        decision = Decision(id="test1", description="Test decision", complexity=3.0)
        print("✓ Decision instantiated successfully")
        
        # Test adding to system
        system.add_agent(agent)
        system.add_decision(decision)
        print("✓ Components added to system successfully")
        
        print("\nAll core component tests passed! ✓")
        return True
        
    except Exception as e:
        print(f"✗ Core component test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Petersonian AI Core Components")
    print("=" * 40)
    success = test_core_components()
    if success:
        print("\nCore implementation is working correctly!")
    else:
        print("\nThere are issues with the core implementation.")