# Import necessary libraries and modules
import re
import nltk
import ast
import time
import sys
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
from pylint.lint import Run

# Download NLTK resources
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')

# Define responses for specific keywords and operations
keyword_responses = {
    "error|issue|not running|logical error|not working": "Can you please provide the code?",
    "not getting intended output": "Do you want to run through the entire code?",
    "iterate through entire loop|run through entire loop": "Please paste your code"
}

operations_name = {
    "=": "Do you wish to assign {} to {}",
    "+": "Do you wish to add {} to {}",
    "-": "Do you wish to subtract {} from {}",
    "*": "Do you wish to multiply {} with {}",
    "/": "Do you wish to divide {} by {}",
    "**": "Do you wish to take the exponential of {} with {}",
    "%": "Do you wish to find the modulo division of {} by {}",
    "//": "Do you wish to take the float division of {} by {}",
    ">": "Do you wish to check if {} is greater than {}",
    "<": "Do you wish to check if {} is less than {}",
    "==": "Do you wish to check if {} is equal to {}",
    ">=": "Do you wish to check if {} is greater than or equal to {}",
    "<=": "Do you wish to check if {} is less than or equal to {}",
    "!=": "Do you wish to check if {} is not equal to {}",
}

# Class for classifying input as code or text
class CodeTextClassifier:
    def __init__(self, code_keywords):
        self.code_keywords = code_keywords

    def classify(self, input_text):
        if self.contains_code_keywords(input_text):
            return "code"
        else:
            return "text"

    def contains_code_keywords(self, text):
        for keyword in self.code_keywords:
            if re.search(r'\b{}\b'.format(re.escape(keyword)), text):
                return True
        return False

# Function to get user input
def user_response():
    return input("You: ")

# Function to respond to text input
def respond_to_text(response):
    # Preprocess the text input
    text = re.sub(r'[^\w\s]', '', response)
    text = text.lower()
    stop_words = set(stopwords.words('english'))
    words = nltk.word_tokenize(text)
    words = [word for word in words if word == "not" or word not in stop_words]
    processed_text = ' '.join(words)
    
    # Check for specific keywords and provide corresponding responses
    for keywords, response in keyword_responses.items():
        keyword_list = keywords.split('|')
        if any(re.search(r'\b{}\b'.format(re.escape(keyword)), processed_text) for keyword in keyword_list):
            return "Ducky: " + response

# Function to analyze code for syntax errors
def analyze_code(code):
    try:
        ast.parse(code)
        exec(code)
        return "Ducky: Your code does not have any syntax errors"
    except Exception as e:
        error_message = str(e)

        # Map specific error patterns to user-friendly messages
        error_mapping = {
            "unexpected EOF while parsing": "Missing closing bracket or parenthesis",
            "EOL while scanning string literal": "Missing or mismatched quotation marks",
            "NameError": "NameError - name '{}' is not declared before using",
            "unterminated string literal": "Possible missing semi-colon at line {}",
            "expected ':'": "There is a missing ':' at line {}"
        }

        for pattern, message in error_mapping.items():
            line_number_match = re.search(r'line (\d+)', error_message)
            if line_number_match:
                line_number = line_number_match.group(1)
                message = message.format(line_number)
            if pattern == "NameError":
                # Check if it's a variable not being defined
                if "' is not defined" in error_message:
                    variable_name = re.search(r"'([^']+)'", error_message).group(1)
                    return f"Ducky: Error - NameError - name '{variable_name}' is not declared before using"
            if pattern in error_message:
                return f"Ducky: Error - {message}"

        return f"Ducky: Error - {type(e).__name__} - {e}"

# Function to analyze code for specific operations
def analyze_operators(lines):
    try:
        operations = ['**', '*', '/', '//', '%', '+', '-', '==', '!=', '>', '<', '>=', '<=', '=']
        if any(op in lines for op in operations):
            operator = []
            for op in operations:
                if op in lines:
                    operator.append(op)
            if len(operator) == 1:
                a = lines.split(op)
                statement = operations_name[op].format(a[1].strip(), a[0].strip())
                print("Ducky:", statement)
                if user_response().lower() == 'yes':
                    pass
                else:
                    print("Ducky: Consider checking your assignment operation")
                    time.sleep(3)
                    print("Ducky: Do you want to continue checking code?")
                    if user_response().lower() == 'yes':
                        pass
                    else:
                        print("Ducky: Hope I helped you debugging the code. Happy Coding")
                        sys.exit()
            # ... (omitting other cases for brevity)
    except SystemExit:
        pass

# Function to analyze specific constructs in code lines
def analyze_line(response):
    try:
        code_lines = response.split("\n")
        should_continue = True
        for j in range(len(code_lines)):
            if not should_continue:
                break
            # Check for 'for' loop
            if re.match(r'^\s*for\s*(\w+)\s*in\s*(?:range\(([^)]+)\)|(\w+))', code_lines[j]):
                match = re.match(r'^\s*for\s*(\w+)\s*in\s*(?:range\(([^)]+)\)|(\w+))', code_lines[j])
                loop_variable = match.group(1)
                iterable_range = match.group(2) or match.group(3)

                # Check the structure of the 'for' loop
                if len(iterable_range) == 3:
                    print(f"Ducky: Are you iterating {loop_variable} from {iterable_range[0]} to {iterable_range[2]}")
                    # ... (omitting other cases for brevity)
                else:
                    print(f"Ducky: Are you iterating {loop_variable} till {iterable_range}")
                    # ... (omitting other cases for brevity)

            # Check for 'if' statement
            elif re.match(r'^\s*if\s(.*)(?:\s*|\().*', code_lines[j]):
                match = re.match(r'^\s*if\s(.*)(?:\s*|\().*', code_lines[j])
                condition = match.group(1)
                print("Ducky: Are you filtering values through this condition:", condition)
                # ... (omitting other cases for brevity)

            # Check for 'print' statement
            elif re.match(r'^\s*print\s*\((.*)\)', code_lines[j]):
                match = re.match(r'^\s*print\s*\((.*)\)', code_lines[j])
                print_statement = match.group(1)
                print(f"Ducky: Are you intending to print {print_statement} statement")
                # ... (omitting other cases for brevity)

            # Check for 'def' function declaration
            elif re.match(r'^\s*def\s+(\w+)\s*\(', code_lines[j]):
                match = re.match(r'^\s*def\s+(\w+)\s*\(', code_lines[j])
                function_name = match.group(1)
                print(f"Ducky: Are you intending to declare a function named {function_name}?")
                # ... (omitting other cases for brevity)

            # Check for 'while' loop
            elif re.match(r'^\s*while\s*(.*)(?:\s*|\().*', code_lines[j]):
                match = re.match(r'^\s*while\s*(.*)(?:\s*|\().*', code_lines[j])
                condition = match.group(1)
                print("Ducky: Are you running a while loop with this condition:", condition)
                # ... (omitting other cases for brevity)

            # Analyze general operators
            else:
                analyze_operators(code_lines[j])
        print("Ducky: End of the code, hope I helped in solving your error")
        sys.exit()
    except SystemExit:
        return False

# Function to handle multi-line user input
def multi_line_response():
    multi_line_input = ""
    while True:
        line = input()
        if line.strip() == 'done':
            break
        multi_line_input += line + '\n'
    return multi_line_input

# Function to process text responses
def process_text_response(response):
    return respond_to_text(response)

# Function to process code responses
def process_code_response(response):
    i = 0
    if i == 0:
        if analyze_code(response) == "Ducky: Your code does not have any syntax errors":
            print("Ducky:", analyze_code(response))
            print("Ducky: Do you want to check anything further")
            if user_response().lower() == "yes":
                analyze_line(response)
            else:
                print("Ducky: Happy Coding")
                sys.exit()
            i = i + 1
        else:
            print("Ducky:", analyze_code(response))
            print("Ducky: Do you want to check anything further")
            if user_response().lower() == "yes":
                analyze_line(response)
            else:
                print("Ducky: Happy Coding")
                sys.exit()
            i = i + 1
    else:
        analyze_line(response)

# Main function to execute the chatbot
def main():
    code_keywords = ["def", "class", "import", "for", "while", "if", "else", "print"]
    classifier = CodeTextClassifier(code_keywords)

    i = 0
    print("Ducky: Hello there, I am Ducky Duck. How may I help you today.")
    while True:
        try:
            response = user_response()
            if response == "bye":
                exit()

            if classifier.classify(response) == "text":
                response = process_text_response(response)
                print(response)
                if "Can you please provide the code?" in response:
                    code_response = multi_line_response()
                    process_code_response(code_response)
            elif classifier.classify(response) == "code":
                process_code_response(response)

        except SystemExit:
            pass

if __name__ == "__main__":
    main()
