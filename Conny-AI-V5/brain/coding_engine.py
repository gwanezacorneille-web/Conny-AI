class CodingEngine:
    """
    CONNY AI Coding Engine V10

    Supports:
        - Programming-language detection
        - Coding-request detection
        - Context-aware code generation
        - Code analysis foundation
        - Debugging foundation
    """

    def __init__(self, brain=None):

        self.brain = brain

        self.languages = {
            "python": ["python", "py"],
            "javascript": ["javascript", "js", "node.js", "node"],
            "java": ["java"],
            "cpp": ["c++", "cpp"],
            "c": [" c ", "c language"],
            "html": ["html"],
            "css": ["css"],
            "bash": ["bash", "shell", "sh"]
        }

    # ==================================================
    # LANGUAGE DETECTION
    # ==================================================

    def detect_language(self, text):

        lower = str(text).lower()

        # Check C++ before C.
        if "c++" in lower or "cpp" in lower:
            return "cpp"

        # Check JavaScript before generic Java.
        if (
            "javascript" in lower
            or "js" in lower
            or "node.js" in lower
            or "node " in lower
        ):
            return "javascript"

        if "java" in lower:
            return "java"

        if "python" in lower or " py " in f" {lower} ":
            return "python"

        if "html" in lower:
            return "html"

        if "css" in lower:
            return "css"

        if "bash" in lower or "shell" in lower:
            return "bash"

        if "c language" in lower or " c " in f" {lower} ":
            return "c"

        return None

    # ==================================================
    # CODING REQUEST DETECTION
    # ==================================================

    def is_coding_request(self, text):

        lower = str(text).lower().strip()

        coding_phrases = (
            "write code",
            "generate code",
            "create code",
            "make code",
            "write a program",
            "create a program",
            "make a program",
            "build a program",
            "write program",
            "create program",
            "make program",
            "build program",
            "code for",
            "program for",
            "write a function",
            "create a function",
            "make a function",
            "write a script",
            "create a script",
            "make a script",
            "debug",
            "fix this code",
            "fix my code",
            "find the bug",
            "syntax error"
        )

        if any(
            phrase in lower
            for phrase in coding_phrases
        ):
            return True

        language = self.detect_language(lower)

        if language:

            coding_action_words = (
                "write",
                "create",
                "make",
                "build",
                "generate",
                "code",
                "program",
                "function",
                "script",
                "debug",
                "fix"
            )

            if any(
                word in lower
                for word in coding_action_words
            ):
                return True

        return False

    # ==================================================
    # CODE GENERATION
    # ==================================================

    def generate(self, text):

        request = str(text).strip()
        lower = request.lower()

        language = self.detect_language(request)

        if language is None:
            language = "python"

        # ==================================================
        # PYTHON
        # ==================================================

        if language == "python":

            if "hello" in lower:

                code = '''print("Hello, world!")'''

            elif (
                "add two numbers" in lower
                or "adds two numbers" in lower
                or "sum two numbers" in lower
            ):

                code = '''def add(a, b):
    return a + b

print(add(5, 3))'''

            elif "calculator" in lower:

                code = '''def calculator(a, b, operator):
    if operator == "+":
        return a + b
    elif operator == "-":
        return a - b
    elif operator == "*":
        return a * b
    elif operator == "/":
        return a / b
    else:
        return "Unknown operator"

print(calculator(10, 5, "+"))'''

            elif "loop" in lower:

                code = '''for i in range(5):
    print(i)'''

            elif "list" in lower:

                code = '''numbers = [1, 2, 3, 4, 5]

for number in numbers:
    print(number)'''

            elif "class" in lower:

                code = '''class Person:

    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hello, {self.name}!"

person = Person("Conny")
print(person.greet())'''

            else:

                code = '''def main():
    print("Hello, world!")

if __name__ == "__main__":
    main()'''

        # ==================================================
        # JAVASCRIPT
        # ==================================================

        elif language == "javascript":

            if (
                "add two numbers" in lower
                or "adds two numbers" in lower
                or "sum two numbers" in lower
            ):

                code = '''function add(a, b) {
    return a + b;
}

console.log(add(5, 3));'''

            elif "hello" in lower:

                code = '''console.log("Hello, world!");'''

            elif "loop" in lower:

                code = '''for (let i = 0; i < 5; i++) {
    console.log(i);
}'''

            elif "array" in lower or "list" in lower:

                code = '''const numbers = [1, 2, 3, 4, 5];

numbers.forEach(number => {
    console.log(number);
});'''

            elif "class" in lower:

                code = '''class Person {
    constructor(name) {
        this.name = name;
    }

    greet() {
        return `Hello, ${this.name}!`;
    }
}

const person = new Person("Conny");
console.log(person.greet());'''

            else:

                code = '''function main() {
    console.log("Hello, world!");
}

main();'''

        # ==================================================
        # JAVA
        # ==================================================

        elif language == "java":

            if "add two numbers" in lower:

                code = '''public class Main {

    static int add(int a, int b) {
        return a + b;
    }

    public static void main(String[] args) {
        System.out.println(add(5, 3));
    }
}'''

            elif "loop" in lower:

                code = '''public class Main {

    public static void main(String[] args) {

        for (int i = 0; i < 5; i++) {
            System.out.println(i);
        }
    }
}'''

            else:

                code = '''public class Main {

    public static void main(String[] args) {

        System.out.println("Hello, world!");

    }
}'''

        # ==================================================
        # C++
        # ==================================================

        elif language == "cpp":

            if "add two numbers" in lower:

                code = '''#include <iostream>

int add(int a, int b) {
    return a + b;
}

int main() {

    std::cout << add(5, 3) << std::endl;

    return 0;
}'''

            elif "loop" in lower:

                code = '''#include <iostream>

int main() {

    for (int i = 0; i < 5; i++) {
        std::cout << i << std::endl;
    }

    return 0;
}'''

            else:

                code = '''#include <iostream>

int main() {

    std::cout << "Hello, world!" << std::endl;

    return 0;
}'''

        # ==================================================
        # C
        # ==================================================

        elif language == "c":

            if "add two numbers" in lower:

                code = '''#include <stdio.h>

int add(int a, int b) {
    return a + b;
}

int main(void) {

    printf("%d\\n", add(5, 3));

    return 0;
}'''

            elif "loop" in lower:

                code = '''#include <stdio.h>

int main(void) {

    for (int i = 0; i < 5; i++) {
        printf("%d\\n", i);
    }

    return 0;
}'''

            else:

                code = '''#include <stdio.h>

int main(void) {

    printf("Hello, world!\\n");

    return 0;
}'''

        # ==================================================
        # HTML
        # ==================================================

        elif language == "html":

            if "button" in lower:

                code = '''<!DOCTYPE html>
<html>
<head>
    <title>CONNY AI</title>
</head>
<body>

    <h1>Hello, world!</h1>

    <button>Click me</button>

</body>
</html>'''

            elif "form" in lower:

                code = '''<!DOCTYPE html>
<html>
<head>
    <title>CONNY AI</title>
</head>
<body>

    <form>
        <label>Name:</label>
        <input type="text">

        <button type="submit">Submit</button>
    </form>

</body>
</html>'''

            else:

                code = '''<!DOCTYPE html>
<html>
<head>
    <title>CONNY AI</title>
</head>
<body>

    <h1>Hello, world!</h1>

</body>
</html>'''

        # ==================================================
        # CSS
        # ==================================================

        elif language == "css":

            if "button" in lower:

                code = '''button {
    padding: 10px 20px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
}

button:hover {
    opacity: 0.8;
}'''

            else:

                code = '''body {
    font-family: sans-serif;
    margin: 0;
    padding: 20px;
}

h1 {
    font-size: 2rem;
}'''

        # ==================================================
        # BASH
        # ==================================================

        elif language == "bash":

            if "list files" in lower or "show files" in lower:

                code = '''#!/bin/bash

ls -la'''

            elif "hello" in lower:

                code = '''#!/bin/bash

echo "Hello, world!"'''

            else:

                code = '''#!/bin/bash

echo "CONNY AI script"'''

        # ==================================================
        # RETURN RESULT
        # ==================================================

        return {
            "type": "generation",
            "language": language,
            "request": request,
            "code": code
        }

    # ==================================================
    # CODE ANALYSIS
    # ==================================================

    def analyze(self, text):

        request = str(text).strip()
        lower = request.lower()

        language = self.detect_language(request)

        issues = []
        suggestions = []

        # ==============================================
        # PYTHON
        # ==============================================

        if language == "python":

            if request.count("(") != request.count(")"):
                issues.append(
                    "Unbalanced parentheses."
                )

            if request.count("[") != request.count("]"):
                issues.append(
                    "Unbalanced square brackets."
                )

            if request.count("{") != request.count("}"):
                issues.append(
                    "Unbalanced curly braces."
                )

            if (
                request.count('"') % 2 != 0
                or request.count("'") % 2 != 0
            ):
                issues.append(
                    "Unbalanced quotation marks."
                )

            if "print(x" in lower:
                issues.append(
                    "The variable 'x' may not be defined."
                )

            if not issues:
                suggestions.append(
                    "No obvious basic Python syntax problems detected."
                )

        # ==============================================
        # JAVASCRIPT
        # ==============================================

        elif language == "javascript":

            if request.count("(") != request.count(")"):
                issues.append(
                    "Unbalanced parentheses."
                )

            if request.count("{") != request.count("}"):
                issues.append(
                    "Unbalanced curly braces."
                )

            if not issues:
                suggestions.append(
                    "No obvious basic JavaScript syntax problems detected."
                )

        # ==============================================
        # C / C++
        # ==============================================

        elif language in ("c", "cpp"):

            if request.count("(") != request.count(")"):
                issues.append(
                    "Unbalanced parentheses."
                )

            if request.count("{") != request.count("}"):
                issues.append(
                    "Unbalanced curly braces."
                )

            if not issues:
                suggestions.append(
                    "No obvious basic C/C++ syntax problems detected."
                )

        # ==============================================
        # JAVA
        # ==============================================

        elif language == "java":

            if request.count("(") != request.count(")"):
                issues.append(
                    "Unbalanced parentheses."
                )

            if request.count("{") != request.count("}"):
                issues.append(
                    "Unbalanced curly braces."
                )

            if not issues:
                suggestions.append(
                    "No obvious basic Java syntax problems detected."
                )

        # ==============================================
        # HTML
        # ==============================================

        elif language == "html":

            if "<html" in lower and "</html>" not in lower:
                issues.append(
                    "Missing </html> tag."
                )

            if "<body" in lower and "</body>" not in lower:
                issues.append(
                    "Missing </body> tag."
                )

            if not issues:
                suggestions.append(
                    "No obvious basic HTML structure problems detected."
                )

        # ==============================================
        # CSS
        # ==============================================

        elif language == "css":

            if request.count("{") != request.count("}"):
                issues.append(
                    "Unbalanced CSS braces."
                )

            if not issues:
                suggestions.append(
                    "No obvious basic CSS syntax problems detected."
                )

        # ==============================================
        # BASH
        # ==============================================

        elif language == "bash":

            suggestions.append(
                "Basic Bash code detected."
            )

        # ==============================================
        # UNKNOWN
        # ==============================================

        else:

            suggestions.append(
                "Language could not be determined."
            )

        return {
            "type": "analysis",
            "language": language,
            "request": request,
            "issues": issues,
            "suggestions": suggestions,
            "has_issues": bool(issues)
        }


    # ==================================================
    # CODE FIXING
    # ==================================================

    def fix(self, text):

        request = str(text)
        lower = request.lower()

        language = self.detect_language(request)

        issues = []
        fixed_code = None

        # ----------------------------------------------
        # PYTHON
        # ----------------------------------------------

        if language == "python":

            # ------------------------------------------
            # Missing closing parenthesis
            # ------------------------------------------

            if "print(x" in lower:

                issues.append(
                    "Unbalanced parentheses."
                )

                issues.append(
                    "The variable 'x' may not be defined."
                )

                fixed_code = '''x = 5
print(x)'''

                fixed = True

            # ------------------------------------------
            # Missing colon after if statement
            # ------------------------------------------

            elif (
                "if " in lower
                and "==" in lower
                and not lower.rstrip().endswith(":")
            ):

                issues.append(
                    "Missing colon after the if statement."
                )

                fixed_code = '''x = 5

if x == 5:
    print("x is 5")'''

                fixed = True

            # ------------------------------------------
            # Missing colon after for
            # ------------------------------------------

            elif (
                "for " in lower
                and not lower.rstrip().endswith(":")
            ):

                issues.append(
                    "The for loop is missing a colon."
                )

                loop_code = request

                if ":" in loop_code:
                    loop_code = loop_code.split(
                        ":",
                        1
                    )[1].strip()

                fixed_code = (
                    loop_code.rstrip()
                    + ":\n"
                    + "    pass"
                )
            # ------------------------------------------
            # Missing colon after while
            # ------------------------------------------

            elif (
                "while " in lower
                and not lower.rstrip().endswith(":")
            ):

                issues.append(
                    "The while loop is missing a colon."
                )

                loop_code = request

                if ":" in loop_code:
                    loop_code = loop_code.split(
                        ":",
                        1
                    )[1].strip()

                fixed_code = (
                    loop_code.rstrip()
                    + ":\n"
                    + "    pass"
                )
            # ------------------------------------------
            # Missing colon after function definition
            # ------------------------------------------

            elif (
                "def " in lower
                and "()" in lower
                and not lower.rstrip().endswith(":")
            ):
                issues.append(
                    "The function definition is missing a colon."
                )

                function_code = request

                if ":" in function_code:
                    function_code = function_code.split(
                        ":",
                        1
                    )[1].strip()

                fixed_code = (
                    function_code.rstrip()
                    + ":\n"
                    + "    pass"
                )
            # ------------------------------------------
            # Missing closing parenthesis
            # ------------------------------------------

            elif (
                lower.count("(")
                > lower.count(")")
            ):

                issues.append(
                    "Unbalanced parentheses."
                )

                fixed_code = request.rstrip() + ")"

            # ------------------------------------------
            # Simple undefined variable
            # ------------------------------------------

            elif "print(" in lower:

                inside = request.split(
                    "print(",
                    1
                )[1]

                variable = inside.split(
                    ")",
                    1
                )[0].strip()

                if (
                    variable
                    and variable.isidentifier()
                    and variable not in (
                        "True",
                        "False",
                        "None"
                    )
                ):

                    issues.append(
                        "The variable '"
                        + variable
                        + "' may not be defined."
                    )

                    fixed_code = (
                        variable
                        + " = 5\n"
                        + "print("
                        + variable
                        + ")"
                    )

            # ------------------------------------------
            # Unbalanced quotes
            # ------------------------------------------

            elif (
                lower.count('"') % 2 != 0
                or lower.count("'") % 2 != 0
            ):

                issues.append(
                    "Unbalanced quotation marks."
                )

                if lower.count('"') % 2 != 0:

                    fixed_code = request.rstrip() + '"'

                else:

                    fixed_code = request.rstrip() + "'"

            # ------------------------------------------
            # No known issue
            # ------------------------------------------

            else:

                issues.append(
                    "No automatic Python fix was found."
                )
 
        # ----------------------------------------------
        # JAVASCRIPT
        # ----------------------------------------------

        elif language == "javascript":

            if "console.log(" in lower:

                if (
                    lower.count("(")
                    > lower.count(")")
                ):

                    issues.append(
                        "Unbalanced parentheses."
                    )

                    fixed_code = request.rstrip() + ")"

            else:

                issues.append(
                    "No automatic JavaScript fix was found."
                )

        # ----------------------------------------------
        # C++
        # ----------------------------------------------

        elif language == "cpp":

            if "cout" in lower and ";" not in request:

                issues.append(
                    "The statement may be missing a semicolon."
                )

                fixed_code = request.rstrip() + ";"

            else:

                issues.append(
                    "No automatic C++ fix was found."
                )

        # ----------------------------------------------
        # C
        # ----------------------------------------------

        elif language == "c":

            if "printf" in lower:

                if ";" not in request:

                    issues.append(
                        "The printf statement is missing a semicolon."
                    )

                    fixed_code = request.rstrip() + ";"

            else:

                issues.append(
                    "No automatic C fix was found."
                )

        # ----------------------------------------------
        # JAVA
        # ----------------------------------------------

        elif language == "java":

            if "system.out.println" in lower:

                if ";" not in request:

                    issues.append(
                        "The println statement is missing a semicolon."
                    )

                    fixed_code = request.rstrip() + ";"

            else:

                issues.append(
                    "No automatic Java fix was found."
                )

        # ----------------------------------------------
        # HTML
        # ----------------------------------------------

        elif language == "html":

            if "<html>" in lower and "</html>" not in lower:

                issues.append(
                    "The HTML document is missing </html>."
                )

                fixed_code = request + "\n</html>"

            else:

                issues.append(
                    "No automatic HTML fix was found."
                )

        # ----------------------------------------------
        # CSS
        # ----------------------------------------------

        elif language == "css":

            if "{" in request and "}" not in request:

                issues.append(
                    "The CSS block is missing a closing brace."
                )

                fixed_code = request + "\n}"

            else:

                issues.append(
                    "No automatic CSS fix was found."
                )

        # ----------------------------------------------
        # UNKNOWN LANGUAGE
        # ----------------------------------------------

        else:

            issues.append(
                "I couldn't determine the programming language."
            )

        # ----------------------------------------------
        # RETURN RESULT
        # ----------------------------------------------

        return {
            "type": "fix",
            "language": language,
            "request": request,
            "issues": issues,
            "code": fixed_code,
            "fixed": fixed_code is not None
        }
