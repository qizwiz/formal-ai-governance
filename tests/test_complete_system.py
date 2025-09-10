#!/usr/bin/env python3
"""
Comprehensive test to verify all core Petersonian AI components work together
"""

def test_complete_system():
    \"\"\"Test that all core components integrate correctly\"\"\"
    try:
        print(\"Testing Complete Petersonian AI System\")
        print(\"=\" * 40)
        
        # Test 1: Import all core components
        print(\"1. Testing core component imports...\")
        from src.peterson_ai_model import PetersonianAISystem, Agent, Decision, Hierarchy
        print(\"   ✓ All core components imported successfully\")
        
        # Test 2: Create system and agents
        print(\"2. Testing system creation...\")
        system = PetersonianAISystem()
        
        # Create hierarchy with different capability levels
        agent_a = Agent(id=\"A\", name=\"CEO\", capability=10.0)
        agent_b = Agent(id=\"B\", name=\"Manager\", capability=7.0, supervisor_id=\"A\")
        agent_c = Agent(id=\"C\", name=\"Junior\", capability=4.0, supervisor_id=\"B\")
        
        system.add_agent(agent_a)
        system.add_agent(agent_b)
        system.add_agent(agent_c)
        print(\"   ✓ System and agents created successfully\")
        
        # Test 3: Validate hierarchy
        print(\"3. Testing hierarchy validation...\")
        is_valid = system.hierarchy.is_valid()
        assert is_valid, \"Hierarchy should be valid\"
        print(f\"   ✓ Hierarchy valid: {is_valid}\")
        
        # Test 4: Decision routing
        print(\"4. Testing decision routing...\")
        simple_decision = Decision(id=\"simple\", description=\"Simple task\", complexity=3.0)
        complex_decision = Decision(id=\"complex\", description=\"Complex task\", complexity=8.0)
        
        # Simple decision should be handled by Junior
        handler_id, log_entry = system.route_decision(simple_decision, \"C\")
        assert handler_id == \"C\", \"Junior should handle simple decision\"
        assert log_entry.directly_made == True, \"Decision should be made directly\"
        print(\"   ✓ Simple decision routed correctly\")
        
        # Complex decision should be referred to CEO
        handler_id, log_entry = system.route_decision(complex_decision, \"C\")
        assert handler_id == \"A\", \"CEO should handle complex decision\"
        assert log_entry.directly_made == False, \"Decision should be referred\"
        print(\"   ✓ Complex decision routed correctly\")
        
        # Test 5: Responsibility calculation
        print(\"5. Testing responsibility calculation...\")
        responsibility = agent_c.get_responsibility_for_decision(log_entry, system.hierarchy)
        assert 0 <= responsibility <= 1, \"Responsibility should be between 0 and 1\"
        print(f\"   ✓ Responsibility calculated: {responsibility:.2f}\")
        
        # Test 6: Performance evaluation
        print(\"6. Testing performance evaluation...\")
        # Add some decisions with outcomes
        decision1 = Decision(id=\"d1\", description=\"Task 1\", complexity=2.0, outcome=True)
        decision2 = Decision(id=\"d2\", description=\"Task 2\", complexity=2.0, outcome=False)
        
        system.add_decision(decision1)
        system.add_decision(decision2)
        system.route_decision(decision1, \"C\")
        system.route_decision(decision2, \"C\")
        
        performance = agent_c.calculate_performance()
        assert 0 <= performance <= 1, \"Performance should be between 0 and 1\"
        print(f\"   ✓ Performance calculated: {performance:.2f}\")
        
        # Test 7: Accountability
        print(\"7. Testing accountability...\")
        accountability = agent_c.calculate_accountability()
        assert 0 <= accountability <= 1, \"Accountability should be between 0 and 1\"
        print(f\"   ✓ Accountability calculated: {accountability:.2f}\")
        
        # Test 8: System stability
        print(\"8. Testing system stability...\")
        stability = system.calculate_system_stability()
        assert 0 <= stability <= 1, \"Stability should be between 0 and 1\"
        print(f\"   ✓ System stability: {stability:.3f}\")
        
        # Test 9: Capability updates
        print(\"9. Testing capability updates...\")
        old_capability = agent_c.capability
        system.update_capabilities()
        new_capability = agent_c.capability
        print(f\"   ✓ Capability updated: {old_capability:.2f} -> {new_capability:.2f}\")
        
        # Test 10: Citizenship score
        print(\"10. Testing citizenship score...\")
        max_knowledge = system.get_max_knowledge_contribution()
        citizenship = agent_c.calculate_citizenship_score(max_knowledge)
        assert 0 <= citizenship <= 1, \"Citizenship should be between 0 and 1\"
        print(f\"   ✓ Citizenship score: {citizenship:.2f}\")
        
        print(\"\n\" + \"=\" * 40)
        print(\"🎉 ALL TESTS PASSED! 🎉\")
        print(\"=\" * 40)
        
        return True
        
    except Exception as e:
        print(f\"\n❌ TEST FAILED: {e}\")
        import traceback
        traceback.print_exc()
        return False

if __name__ == \"__main__\":
    success = test_complete_system()
    exit(0 if success else 1)
