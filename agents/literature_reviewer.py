from typing import Dict, Any
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

from graph.state import AgentState
from utils.logger import logger, format_agent_message
from utils.prompts import build_literature_prompt


class LiteratureReviewerAgent:
    
    def __init__(self, model_name: str = "llama3.1:8b"):
        self.name = "Literature Reviewer"
        self.model_name = model_name
        
        self.llm = ChatOllama(
            model=model_name,
            temperature=0.5,  # Moderate creativity for analysis
            num_predict=800   # Longer outputs for detailed analysis
        )
        
        logger.info(f"{self.name} agent ready")
    
    def execute(self, state: AgentState) -> Dict[str, Any]:
        logger.agent_start(self.name, "Analyzing Research Context")
        
        try:
            paper_abstract = state.get("paper_abstract", "")
            if not paper_abstract:
                logger.warning("No paper abstract available")
                return state
            
            logger.info(f"Analyzing paper ({len(paper_abstract)} chars)")
            
            findings = self._analyze_literature(paper_abstract)
            
            logger.reasoning(f"Identified key research context and related work areas. "
                           f"Analysis covers: key concepts, research domain, novelty assessment.")
            
            updated_state = state.copy()
            updated_state["literature_findings"] = findings
            
            message = format_agent_message(
                agent_name=self.name,
                content=f"Completed literature review. Identified key concepts and research context.",
                action="literature_analysis"
            )
            current_messages = state.get("messages", [])
            updated_state["messages"] = current_messages + [message]
            
            logger.state_update("literature_findings", findings[:150])
            logger.success("Literature review complete")
            
            updated_state["next_agent"] = "supervisor"
            
            return updated_state
            
        except Exception as e:
            logger.error(f"Literature review failed: {str(e)}")
            return state
    
    def _analyze_literature(self, paper_abstract: str) -> str:
        system_prompt = build_literature_prompt({"paper_abstract": paper_abstract})
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content="Provide your literature review analysis following the specified format.")
        ]
        
        logger.info("Running the literature analysis")
        response = self.llm.invoke(messages)
        
        return response.content