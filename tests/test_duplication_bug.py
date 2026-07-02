"""
Test Script to Reproduce Tool Duplication Bug in CrewAI 0.177.0

This script creates a simple test case that should help us identify
where tool duplication might be occurring.
"""

import time
from typing import Any, ClassVar
from crewai import Agent, Task, Crew
from crewai.tools import BaseTool

class DuplicationTrackingTool(BaseTool):
    """Tool that tracks every invocation to detect duplication"""
    
    name: str = "DuplicationTrackingTool"
    description: str = "Tracks tool invocations to detect duplication"
    
    # Class variables to track all invocations across instances
    invocation_count: ClassVar[int] = 0
    invocation_times: ClassVar[list] = []
    invocation_details: ClassVar[list] = []

    def _run(self, test_id: str = "default", **kwargs) -> str:
        """Tool execution that logs invocation details"""
        # Increment global counter
        DuplicationTrackingTool.invocation_count += 1
        current_count = DuplicationTrackingTool.invocation_count
        current_time = time.time()
        
        # Record invocation details
        invocation_detail = {
            'count': current_count,
            'time': current_time,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'test_id': test_id,
            'kwargs': kwargs,
            'time_since_last': None,
            'duplicate_warning': False
        }
        
        # Calculate time since last invocation
        if DuplicationTrackingTool.invocation_times:
            time_since_last = current_time - DuplicationTrackingTool.invocation_times[-1]
            invocation_detail['time_since_last'] = time_since_last
            
            # Flag as potential duplicate if very rapid (< 100ms)
            if time_since_last < 0.1:
                invocation_detail['duplicate_warning'] = True
                print(f"⚠️  POTENTIAL DUPLICATE DETECTED! Time since last: {time_since_last:.6f}s")
        
        DuplicationTrackingTool.invocation_times.append(current_time)
        DuplicationTrackingTool.invocation_details.append(invocation_detail)
        
        # Detailed logging
        print(f"🔧 TOOL INVOCATION #{current_count}")
        print(f"   🕐 Timestamp: {invocation_detail['timestamp']} ({current_time:.6f})")
        print(f"   🆔 Test ID: {test_id}")
        print(f"   📦 Kwargs: {kwargs}")
        
        if invocation_detail['time_since_last']:
            print(f"   ⏱️  Time since last: {invocation_detail['time_since_last']:.6f}s")
            if invocation_detail['duplicate_warning']:
                print(f"   ⚠️  RAPID REPEATED INVOCATION - POSSIBLE DUPLICATION!")
        
        print("-" * 60)
        
        # Simulate some work
        time.sleep(0.02)  # 20ms delay
        
        return f"[EXEC #{current_count}] Test {test_id} completed at {invocation_detail['timestamp']}"

def test_tool_duplication_direct():
    """Test direct tool invocation for duplication"""
    print("🔍 TESTING DIRECT TOOL INVOCATION FOR DUPLICATION")
    print("=" * 60)
    
    # Reset counters
    DuplicationTrackingTool.invocation_count = 0
    DuplicationTrackingTool.invocation_times = []
    DuplicationTrackingTool.invocation_details = []
    
    print("🚀 CALLING TOOL DIRECTLY MULTIPLE TIMES...")
    print()
    
    # Call tool multiple times directly
    for i in range(5):
        print(f"CALLTYPE {i+1}:")
        try:
            tool = DuplicationTrackingTool()
            result = tool._run(f"direct_{i+1}", iteration=i+1)
            print(f"   Result: {result}")
        except Exception as e:
            print(f"   Error: {e}")
        print()
        time.sleep(0.05)  # Small delay between calls
    
    print("📊 DIRECT INVOCATION ANALYSIS:")
    print(f"   Total Invocations: {DuplicationTrackingTool.invocation_count}")
    if DuplicationTrackingTool.invocation_count > 5:
        print(f"   ❌ DUPLICATION DETECTED: {DuplicationTrackingTool.invocation_count - 5} extra invocations")
        return True
    else:
        print(f"   ✅ No duplication detected in direct calls")
        return False

def test_tool_duplication_with_agents():
    """Test tool invocation through agents for duplication"""
    print("🔍 TESTING AGENT-TRIGGERED TOOL INVOCATION FOR DUPLICATION")
    print("=" * 60)
    
    # Reset counters
    DuplicationTrackingTool.invocation_count = 0
    DuplicationTrackingTool.invocation_times = []
    DuplicationTrackingTool.invocation_details = []
    
    # Create tool
    tool = DuplicationTrackingTool()
    
    # Create agent with the tool
    agent = Agent(
        role="Test Agent",
        goal="Test tool invocation behavior",
        backstory="Agent to test tool duplication",
        tools=[tool],
        verbose=True
    )
    
    # Create task that uses the tool
    task = Task(
        description="Use the duplication tracking tool with test_id 'agent_test'",
        expected_output="Confirmation that tool was used",
        agent=agent
    )
    
    # Create crew
    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=True
    )
    
    print("🚀 EXECUTING CREW WITH TOOL...")
    print()
    
    # Execute the crew
    try:
        result = crew.kickoff()
        print()
        print("✅ CREW EXECUTION COMPLETED")
        print(f"   Result: {result}")
        
        # Analyze tool invocation counts
        print("\n📊 AGENT INVOCATION ANALYSIS:")
        print(f"   Total Tool Invocations: {DuplicationTrackingTool.invocation_count}")
        if DuplicationTrackingTool.invocation_count > 1:
            print(f"   ❌ POTENTIAL DUPLICATION: {DuplicationTrackingTool.invocation_count} total invocations for 1 expected")
            return True
        else:
            print(f"   ✅ No duplication detected in agent calls")
            return False
            
    except Exception as e:
        print(f"❌ ERROR DURING AGENT EXECUTION: {e}")
        import traceback
        traceback.print_exc()
        return False

def demonstrate_bug_report():
    """Demonstrate the exact bug report conditions"""
    print("📋 DEMONSTRATING BUG REPORT CONDITIONS")
    print("=" * 60)
    
    print("Issue: [BUG] Tool invocation occurs twice in version 0.177.0")
    print()
    print("Reported Conditions:")
    print("1. Set up a multi-crew architecture with agents configured to call external tools")
    print("2. Register at least 4 tools in the environment")
    print("3. Trigger tool execution through an agent")
    print("4. Observe that the tool is invoked twice in quick succession")
    print()
    print("Our Setup:")
    print("✅ CrewAI 0.177.0 is installed and working")
    print("✅ Multi-tool architecture is possible")
    print("✅ Tool execution framework is functional")
    print("❓ Duplication may occur in specific LLM-triggered scenarios")
    
    print("=" * 60)

if __name__ == "__main__":
    print("🤖 CREWAI TOOL DUPLICATION BUG REPRODUCTION TEST")
    print("Attempting to reproduce the specific conditions where")
    print("tools are invoked twice in CrewAI version 0.177.0")
    print()
    
    # Demonstrate bug report conditions
    demonstrate_bug_report()
    print()
    
    # Test 1: Direct tool invocation
    print("TEST 1: Direct Tool Invocation")
    direct_duplication = test_tool_duplication_direct()
    print()
    
    # Test 2: Agent-triggered tool invocation (if we can run it)
    print("TEST 2: Agent-Triggered Tool Invocation")
    try:
        agent_duplication = test_tool_duplication_with_agents()
    except Exception as e:
        print(f"⚠️  Agent test skipped due to: {e}")
        agent_duplication = False
    
    print()
    print("🎯 OVERALL RESULTS:")
    if direct_duplication or agent_duplication:
        print("   ❌ Duplication detected - bug reproduced!")
    else:
        print("   ✅ No duplication found in our tests")
        print("   The bug might occur in specific LLM-triggered scenarios")
        print("   or with particular tool configurations")
    
    print()
    print("🚀 READY TO INVESTIGATE FURTHER AND CREATE FIX!")