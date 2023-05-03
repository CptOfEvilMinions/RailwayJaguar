from typing import Any, List

powershell_empire_cmd: List[str] = [
    "-exec",
    "bypass",
    "-nologo", 
    "-nop",
    "-w",
    "hidden", 
    "-enc",
]

def rule(event: Any) -> bool:
    executable = event.get("process", None).get("name", None)
    if executable is None or executable != "powershell.exe":
        return False

    command_line = event.get("process", None).get("command_line", None)
    if command_line is None:
        return False
    
    count = 0
    for cmdlet in command_line.split(" "):
        if cmdlet in command_line:
            count = count + 1

    return count > 4