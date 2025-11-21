from colorama import Fore, Style, init
from typing import Dict, Any
import json
from datetime import datetime

init(autoreset=True)


class MASLogger:
    
    def __init__(self, verbosity: int = 1):
        self.verbosity = verbosity
        
    def header(self, text: str):
        if self.verbosity >= 0:
            print(f"\n{Fore.CYAN}{'-' * 60}")
            print(f"{Fore.CYAN}{text}")
            print(f"{Fore.CYAN}{'-' * 60}{Style.RESET_ALL}\n")
    
    def section(self, text: str):
        if self.verbosity >= 1:
            print(f"\n{Fore.YELLOW}{'-' * 60}")
            print(f"{Fore.YELLOW}{text}")
            print(f"{Fore.YELLOW}{'-' * 60}{Style.RESET_ALL}\n")
    
    def agent_start(self, agent_name: str, role: str):
        if self.verbosity >= 1:
            print(f"{Fore.GREEN}{agent_name} - {role}{Style.RESET_ALL}")
            if self.verbosity >= 2:
                print(f"{Fore.CYAN}Timestamp: {datetime.now().strftime('%H:%M:%S')}{Style.RESET_ALL}")
    
    def reasoning(self, thought: str):
        if self.verbosity >= 1:
            print(f"{Fore.MAGENTA}Reasoning:{Style.RESET_ALL}")
            lines = thought.split('\n')
            for line in lines:
                if line.strip():
                    print(f"   {line}")
            print()
    
    def decision(self, decision: str, reason: str = ""):
        if self.verbosity >= 1:
            print(f"{Fore.GREEN}Decision: {decision}{Style.RESET_ALL}")
            if reason and self.verbosity >= 2:
                print(f"   Reason: {reason}")
            print()
    
    def state_update(self, field: str, preview: str = ""):
        if self.verbosity >= 1:
            print(f"{Fore.BLUE}State update: {field}{Style.RESET_ALL}")
            print("\n----------------------------------------------")
            if preview and self.verbosity >= 2:
                preview_text = preview[:100] + "..." if len(preview) > 100 else preview
                print(f"   Preview: {preview_text}")
            print()
    
    def communication(self, from_agent: str, message: str):
        if self.verbosity >= 2:
            print(f"{Fore.CYAN}{from_agent} -> Blackboard:{Style.RESET_ALL}")
            print(f"   {message[:150]}...")
            print()
    
    def state_snapshot(self, state: Dict[str, Any]):
        if self.verbosity >= 2:
            print(f"{Fore.YELLOW}State snapshot:{Style.RESET_ALL}")
            for key, value in state.items():
                if key == "messages":
                    print(f"   {key}: {len(value)} messages")
                elif key == "paper_abstract" and value:
                    print(f"   {key}: {len(value)} chars")
                elif isinstance(value, str) and len(value) > 100:
                    print(f"   {key}: {value[:100]}...")
                else:
                    print(f"   {key}: {value}")
            print()
    
    def error(self, message: str):
        print(f"{Fore.RED}ERROR: {message}{Style.RESET_ALL}\n")
    
    def warning(self, message: str):
        if self.verbosity >= 1:
            print(f"{Fore.YELLOW}WARNING: {message}{Style.RESET_ALL}\n")
    
    def success(self, message: str):
        print(f"{Fore.GREEN}{message}{Style.RESET_ALL}\n")
    
    def info(self, message: str):
        if self.verbosity >= 1:
            print(f"{Fore.WHITE}{message}{Style.RESET_ALL}")
    
    def final_output(self, report: str):
        self.header("FINAL ANALYSIS REPORT")
        print(f"{Fore.WHITE}{report}{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}{'-' * 60}{Style.RESET_ALL}\n")
    
    def workflow_summary(self, total_agents: int, iterations: int, time_taken: float):
        if self.verbosity >= 1:
            self.section("WORKFLOW SUMMARY")
            print(f"   Total Agents Executed: {total_agents}")
            print(f"   Total Iterations: {iterations}")
            print(f"   Time Taken: {time_taken:.2f} seconds")
            print(f"   Average per Agent: {time_taken/total_agents:.2f}s")
            print()


def format_agent_message(agent_name: str, content: str, action: str = "") -> Dict[str, str]:
    return {
        "agent": agent_name,
        "content": content,
        "action": action,
        "timestamp": datetime.now().isoformat()
    }


logger = MASLogger(verbosity=1)


def set_verbosity(level: int):
    global logger
    logger = MASLogger(verbosity=level)