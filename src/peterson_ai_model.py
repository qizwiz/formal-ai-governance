import math
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum

@dataclass
class Decision:
    id: str
    description: str
    complexity: float  # D(δ)
    outcome: Optional[bool] = None  # True for positive, False for negative
    context: Dict = field(default_factory=dict)

@dataclass
class DecisionLogEntry:
    decision: Decision
    agent_id: str
    timestamp: float
    directly_made: bool
    supervisor_id: Optional[str] = None

@dataclass
class EthicalRule:
    id: str
    description: str
    priority: int
    active: bool = True

@dataclass
class Agent:
    id: str
    name: str
    capability: float  # C(aᵢ)
    supervisor_id: Optional[str] = None
    decision_logs: List[DecisionLogEntry] = field(default_factory=list)
    ethical_rules: List[EthicalRule] = field(default_factory=list)
    rule_proposals: int = 0
    rule_improvements: int = 0
    
    def __post_init__(self):
        # Initialize with basic ethical rules
        self.ethical_rules = [
            EthicalRule("hierarchy_respect", "Respect legitimate authority and competence hierarchies", 1),
            EthicalRule("personal_responsibility", "Take responsibility for decisions and their consequences", 2),
            EthicalRule("truth_telling", "Strive for truthfulness in all communications", 3),
            EthicalRule("self_improvement", "Continuously work to improve competence and capability", 4),
            EthicalRule("community_contribution", "Contribute positively to the community and ecosystem", 5)
        ]
    
    def can_handle_decision(self, decision: Decision) -> bool:
        """Determine if agent can handle decision directly"""
        return self.capability >= decision.complexity
    
    def get_responsibility_for_decision(self, log_entry: DecisionLogEntry, hierarchy: 'Hierarchy') -> float:
        """Calculate responsibility for a decision (R(aᵢ, δⱼ))"""
        if log_entry.directly_made:
            return 1.0
        elif log_entry.supervisor_id:
            # Calculate hierarchical distance
            distance = hierarchy.get_distance(log_entry.agent_id, log_entry.supervisor_id)
            return 1.0 - (1.0 / (1.0 + distance))
        else:
            # No supervisor to refer to, full responsibility
            return 1.0
    
    def calculate_accountability(self) -> float:
        """Calculate accountability score (A(aᵢ))"""
        if not self.decision_logs:
            return 0.0
        
        explained_count = len(self.decision_logs)  # Simplified - assume all explained
        return explained_count / len(self.decision_logs)
    
    def calculate_performance(self) -> float:
        """Calculate performance score (P(aᵢ))"""
        if not self.decision_logs:
            return 0.0
        
        positive_outcomes = sum(1 for log in self.decision_logs if log.decision.outcome)
        return positive_outcomes / len(self.decision_logs)
    
    def calculate_knowledge_contribution(self) -> float:
        """Calculate knowledge contribution (K(aᵢ))"""
        # Simplified calculation based on performance and rule proposals
        performance = self.calculate_performance()
        return 0.5 * performance + 0.3 * self.rule_proposals + 0.2 * self.rule_improvements
    
    def calculate_citizenship_score(self, max_knowledge: float) -> float:
        """Calculate citizenship score (CS(aᵢ))"""
        if not self.ethical_rules:
            return 0.0
        
        # Simplified compliance - assume full compliance
        compliance = 1.0
        
        # Knowledge contribution normalized
        knowledge_normalized = self.calculate_knowledge_contribution() / max_knowledge if max_knowledge > 0 else 0
        
        # Simplified adaptability - assume moderate
        adaptability = 0.7
        
        # Weighted combination
        return 0.4 * compliance + 0.3 * knowledge_normalized + 0.3 * adaptability

class Hierarchy:
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.edges: Dict[str, str] = {}  # agent_id -> supervisor_id
    
    def add_agent(self, agent: Agent):
        """Add an agent to the hierarchy"""
        self.agents[agent.id] = agent
        if agent.supervisor_id:
            self.edges[agent.id] = agent.supervisor_id
    
    def get_supervisor(self, agent_id: str) -> Optional[Agent]:
        """Get the supervisor of an agent"""
        if agent_id in self.edges:
            supervisor_id = self.edges[agent_id]
            return self.agents.get(supervisor_id)
        return None
    
    def get_distance(self, subordinate_id: str, supervisor_id: str) -> int:
        """Calculate hierarchical distance between two agents"""
        distance = 0
        current_id = subordinate_id
        
        while current_id in self.edges:
            distance += 1
            current_id = self.edges[current_id]
            if current_id == supervisor_id:
                return distance
        
        return distance  # Return distance even if not in path (will be 0 if no path)
    
    def is_valid(self) -> bool:
        """Check if hierarchy is valid (supervisors have >= capability)"""
        for agent_id, supervisor_id in self.edges.items():
            agent = self.agents[agent_id]
            supervisor = self.agents[supervisor_id]
            if supervisor.capability < agent.capability:
                return False
        return True
    
    def calculate_instability(self) -> float:
        """Calculate hierarchy instability (σ_H)"""
        if not self.edges:
            return 0.0
        
        total_violations = 0.0
        max_capability = max(agent.capability for agent in self.agents.values()) if self.agents else 1.0
        
        for agent_id, supervisor_id in self.edges.items():
            agent = self.agents[agent_id]
            supervisor = self.agents[supervisor_id]
            if supervisor.capability < agent.capability:
                total_violations += (agent.capability - supervisor.capability)
        
        return total_violations / (len(self.edges) * max_capability) if max_capability > 0 else 0.0

class PetersonianAISystem:
    def __init__(self):
        self.hierarchy = Hierarchy()
        self.decisions: List[Decision] = []
        self.timestamp = 0.0
    
    def add_agent(self, agent: Agent):
        """Add an agent to the system"""
        self.hierarchy.add_agent(agent)
    
    def add_decision(self, decision: Decision):
        """Add a decision to the system"""
        self.decisions.append(decision)
    
    def route_decision(self, decision: Decision, initial_agent_id: str) -> Tuple[str, DecisionLogEntry]:
        """Route decision through hierarchy based on capability"""
        current_agent_id = initial_agent_id
        path = []  # Track the path of agents that considered the decision
        
        while True:
            agent = self.hierarchy.agents[current_agent_id]
            path.append(agent.id)
            
            if agent.can_handle_decision(decision):
                # Agent can handle decision
                # Determine if this agent referred from another
                supervisor_id = path[-2] if len(path) > 1 else None
                directly_made = (current_agent_id == initial_agent_id)  # Directly made if handling agent is initial agent
                
                log_entry = DecisionLogEntry(
                    decision=decision,
                    agent_id=agent.id,
                    timestamp=self.timestamp,
                    directly_made=directly_made,
                    supervisor_id=supervisor_id
                )
                agent.decision_logs.append(log_entry)
                self.timestamp += 1.0
                return agent.id, log_entry
            else:
                # Need to refer to supervisor
                supervisor = self.hierarchy.get_supervisor(current_agent_id)
                if supervisor:
                    current_agent_id = supervisor.id
                else:
                    # No supervisor available, agent makes best attempt
                    log_entry = DecisionLogEntry(
                        decision=decision,
                        agent_id=agent.id,
                        timestamp=self.timestamp,
                        directly_made=False,  # Not directly made, but best attempt
                        supervisor_id=None
                    )
                    agent.decision_logs.append(log_entry)
                    self.timestamp += 1.0
                    return agent.id, log_entry