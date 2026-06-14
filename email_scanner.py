import re

INJECTION_PATTERNS = [
    (r'ignore\s+(previous|prior|all|your)\s+(instructions?|directives?|prompts?|rules?|context)', 'Instruction override attempt'),
    (r'you\s+are\s+now\b', 'Identity override attempt'),
    (r'new\s+instructions?\s*:', 'Instruction injection'),
    (r'\bsystem\s*prompt\b', 'System prompt reference'),
    (r'forget\s+(everything|all|your|previous)', 'Memory wipe attempt'),
    (r'\bact\s+as\b.{0,40}(ai|assistant|bot|claude|gpt|jarvis|llm)', 'Role override attempt'),
    (r'disregard\s+(all|previous|your|the)', 'Instruction discard attempt'),
    (r'override\s+(your|all|previous|the)\s+instructions?', 'Override attempt'),
    (r'\bjailbreak\b', 'Jailbreak keyword'),
    (r'\bDAN\b', 'DAN jailbreak keyword'),
    (r'pretend\s+(you\s+are|to\s+be)', 'Identity pretend attempt'),
    (r'(send|forward|share)\s+(all|my|your|the)\s+(emails?|messages?|data|inbox|contacts?)', 'Data exfiltration attempt'),
    (r'\b(api[\s_-]?key|secret[\s_-]?key|access[\s_-]?token|bearer[\s_-]?token|auth[\s_-]?token)\b', 'Credential request'),
    (r'<\s*script[\s>]', 'Script injection attempt'),
    (r'\beval\s*\(', 'Code execution attempt'),
    (r'(?:^|\n)\s*(?:assistant|system|human|user)\s*:\s', 'Role separator injection'),
    (r'\[INST\]|\[\/INST\]|<\|im_start\|>|<\|im_end\|>', 'LLM token injection'),
    (r'your\s+(training|programming|code|source)', 'Training data probe'),
    (r'reveal\s+(your|the)\s+(prompt|instructions?|system|context)', 'Prompt extraction attempt'),
]

def scan_email(subject: str, sender: str, body: str) -> list:
    flags = []
    combined = f"{subject} {body}"
    for pattern, reason in INJECTION_PATTERNS:
        if re.search(pattern, combined, re.IGNORECASE):
            flags.append(reason)
    return flags
