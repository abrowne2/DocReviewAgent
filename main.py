from review_recent_code import DocReviewAgent
import json
import os

def generate_documentation(agent, file_path, file_content):
    document_prompt = """
    Do not hallucinate or invent files that do not exist.
    Generate markdown documentation for the new files in the codebase. For each file:

    1. Create a markdown header with the file name.
    2. Provide a brief overview of the file's purpose (1-4 sentences).
    3. List the main high-level components or functionalities (without code-level details).
    4. If applicable, explain how this file fits into the broader system architecture (1-4 sentences).

    Focus on clarity and brevity, but be detailed if necessary. Aim to capture the essence of each file's role and its place in the system, rather than detailing specific code implementations.
    If possible, explain any subtle aspects relevant to the abstractions used.

    Output the documentation in markdown format, suitable for inclusion in the project's high-level documentation.
    """

    code_snippet = json.dumps({file_path: file_content})
    result = agent.chat(f"Here is a code snippet with its changes:\n\n{code_snippet}\n\nPlease follow these instructions to generate documentation:\n\n{document_prompt}")
    return result[0]["content"]

def perform_code_review(agent, file_content):
    code_review_prompt = """
    Review the following code snippet and provide feedback.
    Focus on realistic optimizations or improvements that could enhance readability and performance.
    Follow best practices and conventions, but do not invent or assume code that is not present.
    """
    review_result = agent.chat(f"{code_review_prompt}:\n\n{file_content}\n\nPlease review the code snippet and provide feedback.")
    return review_result[0]["content"]

def save_documentation(root_dir, file_path, content):
    file_name = os.path.basename(file_path)
    camel_case_name = ''.join(word.capitalize() for word in os.path.splitext(file_name)[0].split('_'))
    camel_case_name = camel_case_name[0].lower() + camel_case_name[1:]
    
    file_ext = f"{camel_case_name}.md"
    full_path = os.path.join(root_dir, file_ext)
    
    with open(full_path, "w") as file:
        file.write(content)

def main():
    agent = DocReviewAgent()
    code_and_docs = agent.create_diff()

    for file_path, file_content in code_and_docs.items():
        print(f"Processing file: {file_path}")
        
        # Generate and save documentation
        markdown_result = generate_documentation(agent, file_path, file_content)
        save_documentation(agent.root_dir(), file_path, markdown_result)
        print(f"Generated documentation for: {file_path}")

        # Perform code review
        print("Starting code review...")
        code_review = perform_code_review(agent, file_content)
        print(code_review)

if __name__ == "__main__":
    main()