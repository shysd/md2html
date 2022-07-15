import sys
import re
import time


class Interpreter:
    RULES = [
        # headings
        ["\s#{6}\s+([^\n]+)", "\n<h6>$1</h6>"],
        ["\s#{5}\s+([^\n]+)", "\n<h5>$1</h5>"],
        ["\s#{4}\s+([^\n]+)", "\n<h4>$1</h4>"],
        ["\s#{3}\s+([^\n]+)", "\n<h3>$1</h3>"],
        ["\s#{2}\s+([^\n]+)", "\n<h2>$1</h2>"],
        ["\s#{1}\s+([^\n]+)", "\n<h1>$1</h1>"],

        # bold and italics
        ["\*\*\s?([^\n]+)\*\*", "<strong>$1</strong>"],
        ["_\s?([^\n]+)_", "<em>$1</em>"],


        # links
        ["[^!]\[([^\]]+)\]\(([^\)]+)\)", " <a href=\"$2\">$1</a>"],

        # images
        ["!\[([^\]]+)\]\(([^\)]+)\)", "<img src=\"$2\" alt=\"$1\" />"],

        # code blocks
        ["\n([^\n]+)\n```([^`]+)```", "<pre><code id=\"$1\">$2</code></pre>"],

        # unordered list
        ["\*\s([^\n]+)\n", "<ul><li>$1</li></ul>"],

        # paragraphs
        ["([^\n]+)\n?", "<p>$1</p>"],

    ]

    def __init__(self):
        pass

    # Convert markdown to html
    @staticmethod
    def interpret(rules, filename):
        t = time.time()
        data = ""
        with open(filename, 'r') as f:
            # lines = f.readlines()
            data = f.read()

            for rule in rules:
                matches = re.finditer(rule[0], data)

                for match in matches:
                    try:
                        rep2 = rule[1].replace("$2", match.group(2))
                        rep1 = rep2.replace("$1", match.group(1))
                    except IndexError:
                        rep1 = rule[1].replace("$1", match.group(1))

                    data = data.replace(match.group(0), rep1)

        fw = open("output.html", 'w')
        fw.write(data)
        fw.close()
        diff = time.time() - t
        print("-----Took %.3f seconds-----" % diff)


if __name__ == "__main__":
    name = sys.argv[1]

    # For windows, check if it starts with ".\"
    if name[0:2] == ".\\":
        name = name[2:]

    Interpreter.interpret(Interpreter.RULES, name)
