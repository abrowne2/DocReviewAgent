from review_recent_code import DocReviewAgent
import json

def main():
    agent = DocReviewAgent()

    code_and_docs = agent.create_diff_corpus()

    document_prompt = """
        Do not hallucinate and come up with files that do not exist.
        Generate markdown documentation for the new files in the codebase. For each file:

        1. Create a markdown header with the file name.
        2. Provide a brief overview of the file's purpose (1-4 sentences).
        3. List the main high-level components or functionalities (without going into code-level details).
        4. If applicable, explain how this file fits into the broader system architecture (1-4 sentences).

        Focus on clarity and brevity, but be detailed if necessary. Aim to capture the essence of each file's role and its place in the system, rather than detailing specific code implementations.
        If you also have some bandwidth, consider explaining subtleties you observe that would be relevant to any abstractions.

        Output the documentation in markdown format, suitable for inclusion in the project's high-level documentation.
    """

    for file_path, file_content in code_and_docs.items():
        code_snippet = json.dumps({file_path: file_content})
        result = agent.chat(f"Here are several snippets of code and configuration with their changes:\n\n{code_snippet}\n\nPlease follow these instructions to generate documentation:\n\n{document_prompt}")
        markdown_result = result[0]["content"]

        # Extract the file name from the file_path
        file_name = file_path.split('/')[-1]

        # Remove file extension and convert to camelCase
        camel_case_name = ''.join(word.capitalize() for word in file_name.split('.')[0].split('_'))
        camel_case_name = camel_case_name[0].lower() + camel_case_name[1:]
        
        file_ext = f"{camel_case_name}.md"
        with open(f"{agent.root_dir()}/{file_ext}", "w") as file:
            file.write(markdown_result)


if __name__ == "__main__":
    main()