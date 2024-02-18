#sudo apt get install sublist3r
from flask import Flask, request, render_template
import subprocess
import re

app = Flask(__name__)

COMMANDS = {
    "find_subdomains": ["sublist3r", "-d"],
    "find_directory": ["./dirble", "--max-threads", "10"],
    "find_nmap": ["nmap", "-A", "-Pn", "-sC", "-sV", "-T5"],
    "what_url": ["whatweb"]
}

ANSI_ESCAPE_REGEX = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')


@app.route("/", methods=["GET", "POST"])
def index():
    scan_output = ""
    if request.method == "POST" and request.form.get("domain"):
        domain = request.form["domain"].strip()
        scan_output = execute_scan(domain)
    return render_template("index.html", scan_output=scan_output)


def execute_scan(domain):
    for cmd_key, cmd_value in COMMANDS.items():
        if cmd_key in request.form:
            if cmd_key == "find_directory" and not domain.startswith(('http://', 'https://')):
                domain = "http://" + domain
            command = cmd_value + [domain]
            return run_command(command, cmd_key)
    return ""


def run_command(command, cmd_key):
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=600)
        return process_output(cmd_key, result.stdout)
    except Exception as e:
        return f"Error running command: {str(e)}"


def process_output(cmd_key, output):
    output = remove_ansi_escape_codes(output)
    if cmd_key == "find_directory":
        return process_directory_output(output)
    elif cmd_key == "find_subdomains":
        return process_subdomains_output(output)
    else:
        return process_general_output(output, cmd_key)


def remove_ansi_escape_codes(text):
    return ANSI_ESCAPE_REGEX.sub('', text)


def process_directory_output(output):
    return '<br>'.join([line for line in output.split('\n') if "(CODE:200" in line])


def process_subdomains_output(output):
    subdomains = []
    capture = False
    for line in output.splitlines():
        if 'Total Unique Subdomains Found' in line:
            capture = True
        elif capture:
            subdomains.append(line)
    return '<br>'.join(subdomains)


def process_general_output(output, cmd_key):
    output_lines = output.split('\n')
    if "nmap" in cmd_key:
        return process_nmap_output(output_lines)
    else:
        return '<br>'.join([line for line in output_lines if not any(exclude in line for exclude in ["Job finished in", "Searching in the"])])


def process_nmap_output(lines):
    filtered_lines = []
    capture = False
    for line in lines:
        if "PORT" in line and "SERVICE" in line:
            capture = True
        elif capture and line.strip() == "":
            break
        elif capture:
            filtered_lines.append(line)
    return '<br>'.join(filtered_lines)


if __name__ == "__main__":
    app.run(debug=True)

