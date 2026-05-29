import re

SKILL_PATTERNS: dict[str, re.Pattern] = {
    "Java": re.compile(r"\bJava\b", re.I),
    "Python": re.compile(r"\bPython\b", re.I),
    "Go": re.compile(r"\bGo(lang)?\b", re.I),
    "Rust": re.compile(r"\bRust\b", re.I),
    "C++": re.compile(r"\bC\+\+\b", re.I),
    "JavaScript": re.compile(r"\bJavaScript\b|\bJS\b", re.I),
    "TypeScript": re.compile(r"\bTypeScript\b|\bTS\b", re.I),
    "React": re.compile(r"\bReact\b", re.I),
    "Vue": re.compile(r"\bVue(\.js)?\b", re.I),
    "Node.js": re.compile(r"\bNode(\.js)?\b", re.I),
    "Spring": re.compile(r"\bSpring\b", re.I),
    "MySQL": re.compile(r"\bMySQL\b", re.I),
    "Redis": re.compile(r"\bRedis\b", re.I),
    "Kafka": re.compile(r"\bKafka\b", re.I),
    "Kubernetes": re.compile(r"\bK(ubernetes|8s)\b", re.I),
    "Docker": re.compile(r"\bDocker\b", re.I),
    "AWS": re.compile(r"\bAWS\b", re.I),
    "机器学习": re.compile(r"机器学习|ML|Machine Learning", re.I),
    "深度学习": re.compile(r"深度学习|Deep Learning", re.I),
    "PyTorch": re.compile(r"\bPyTorch\b", re.I),
    "TensorFlow": re.compile(r"\bTensorFlow\b", re.I),
}


def extract_skills(text: str) -> list[str]:
    found = [name for name, pattern in SKILL_PATTERNS.items() if pattern.search(text)]
    return found[:10]
