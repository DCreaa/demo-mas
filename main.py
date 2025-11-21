import sys
import time

from graph.state import create_initial_state, get_state_summary
from graph.workflow import create_research_workflow, run_workflow, display_workflow_summary
from utils.logger import logger, set_verbosity

MODEL_NAME = "llama3.1:8b"
VERBOSITY = 1
INTERACTIVE_MODE = False

SAMPLE_PAPER = """
Recent advances in deep learning have demonstrated remarkable performance in image classification tasks. 
However, standard convolutional neural networks often struggle with limited training data and exhibit 
poor generalization to out-of-distribution samples. This paper proposes a novel meta-learning framework 
that combines few-shot learning with adversarial training to improve model robustness. Our approach, 
termed "Adaptive Meta-Adversarial Networks (AMAN)", leverages episodic training to learn transferable 
representations while incorporating adversarial perturbations during meta-training. We introduce a 
dynamic task sampling strategy that progressively increases task difficulty, enabling the model to 
develop more resilient features. Experimental results on miniImageNet and tieredImageNet benchmarks 
show that AMAN achieves state-of-the-art performance, improving 5-shot classification accuracy by 3.2% 
over existing methods while maintaining computational efficiency. Furthermore, our ablation studies 
reveal that the synergy between meta-learning and adversarial training is crucial for achieving robust 
generalization. The proposed framework opens new directions for building AI systems that can rapidly 
adapt to new tasks with minimal data while remaining resilient to distributional shifts.
"""


def check_ollama_connection(model_name: str) -> bool:
    try:
        from langchain_ollama import ChatOllama
        
        llm = ChatOllama(model=model_name, num_predict=10)
        llm.invoke("test")
        
        logger.success("Ollama is running correctly")
        return True
        
    except Exception as e:
        return False


def display_welcome_banner():
    banner = """
---------------------------------------------------------------
    RESEARCH PAPER ANALYSIS MAS
---------------------------------------------------------------
    """
    print(banner)


def main():
    set_verbosity(VERBOSITY)
    
    display_welcome_banner()
    
    if not check_ollama_connection(MODEL_NAME):
        sys.exit(1)
    
    logger.info("Using embedded sample paper abstract")
    paper_abstract = SAMPLE_PAPER.strip()
    
    if len(paper_abstract) < 100:
        logger.warning("Paper abstract is very short. Results may be limited.")
    
    logger.info(f"Paper abstract: {len(paper_abstract)} characters")
    logger.info(f"Target: Generate comprehensive research review\n")
    
    initial_state = create_initial_state(paper_abstract)
    
    if VERBOSITY >= 2:
        logger.section("INITIAL STATE")
        logger.info(get_state_summary(initial_state))
    
    try:
        workflow = create_research_workflow(model_name=MODEL_NAME)
    except Exception as e:
        logger.error(f"Failed to create workflow: {str(e)}")
        sys.exit(1)
    
    if INTERACTIVE_MODE:
        logger.info("Interactive mode enabled - press Enter after each agent")
        input("\nPress Enter to start workflow...")
    
    start_time = time.time()
    
    try:
        final_state = run_workflow(workflow, initial_state)
        
    except KeyboardInterrupt:
        logger.warning("\nWorkflow interrupted by user")
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"Workflow execution failed: {str(e)}")
        if VERBOSITY >= 2:
            import traceback
            logger.error(traceback.format_exc())
        sys.exit(1)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    if VERBOSITY >= 1:
        display_workflow_summary(final_state)
    
    logger.section("EXECUTION STATISTICS")
    logger.info(f"Total execution time: {elapsed_time:.2f} seconds")
    logger.info(f"Total agent messages: {len(final_state.get('messages', []))}")
    logger.info(f"Workflow iterations: {final_state.get('iteration_count', 0)}")
    logger.info(f"Analysis complete: {final_state.get('analysis_complete', False)}")
    
    if INTERACTIVE_MODE:
        save = input("\nSave final report to file? (y/n): ")
        if save.lower() == 'y':
            filename = input("Enter filename (default: review_report.txt): ").strip()
            if not filename:
                filename = "review_report.txt"
            
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("=" * 70 + "\n")
                    f.write("MAS RESEARCH PAPER REVIEW\n")
                    f.write("=" * 70 + "\n\n")
                    f.write(final_state.get("final_report", "No report generated"))
                
                logger.success(f"Report saved to: {filename}")
            except Exception as e:
                logger.error(f"Failed to save report: {str(e)}")
    
    logger.header("DEMONSTRATION END")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupt!")
        sys.exit(0)