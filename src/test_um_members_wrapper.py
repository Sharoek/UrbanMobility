import subprocess

# Path to your Python login script
script_path = "um_members.py"

# Test username/password combos (SQLi & null byte payloads)
test_cases = [
    ("admin' OR '1'='1", "anything"),
    ("admin'--", "anything"),
    ("admin' #", "anything"),
    ("admin OR 1=1", "anything"),
    ("admin%00", "anything"),
    ("admin", "' OR '1'='1"),
    ("admin", "' OR 1=1 --"),
    ("admin", "anything%00"),
]

for username, password in test_cases:
    print(f"Testing username: {username} | password: {password}")

    # Start your script as a subprocess
    proc = subprocess.Popen(
        ["python", script_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # Send username and password input (with newlines)
    inputs = f"{username}\n{password}\n"

    try:
        out, err = proc.communicate(input=inputs, timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()
        print("Script timed out!")
        out, err = "", ""

    # Print relevant output snippet to see what happened
    print("Output:")
    print(out.strip())

    # Basic heuristic to detect possible bypass or rejection
    lowered = out.lower()
    if ("invalid" not in lowered and "error" not in lowered) and ("exit" not in lowered):
        print("⚠️ Possible bypass or unexpected response — check manually.")
    else:
        print("✅ Input rejected or handled correctly.")

    print("-" * 60)
