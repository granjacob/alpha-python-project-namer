import argparse
import os
import json

GREEK_ALPHABET = [
    'alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta', 'theta',
    'iota', 'kappa', 'lambda', 'mu', 'nu', 'xi', 'omicron', 'pi', 'rho',
    'sigma', 'tau', 'upsilon', 'phi', 'chi', 'psi', 'omega'
]

STATE_FILE = os.path.expanduser("~/.gran_state")


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {"last_index": -1}


def save_state(index):
    with open(STATE_FILE, 'w') as f:
        json.dump({"last_index": index}, f)


def get_prefix(index):
    base = len(GREEK_ALPHABET)
    if index < base:
        return GREEK_ALPHABET[index]

    # Convert index to base-n using greek letters
    prefix_parts = []
    while index >= 0:
        prefix_parts.append(GREEK_ALPHABET[index % base])
        index = index // base - 1
    return ''.join(reversed(prefix_parts))


def generate_project_name(index, keywords, suffix):
    prefix = get_prefix(index)
    words = "-".join([*keywords, suffix]) if suffix else "-".join(keywords)
    return f"{prefix}-{words}"


def main():
    parser = argparse.ArgumentParser(description="Generador de nombres de proyecto estilo GRAN")
    parser.add_argument("-i", "--inputs", required=True, help="Palabras clave separadas por coma")
    parser.add_argument("-s", "--suffix", help="Sufijo del nombre (ej: books)")
    parser.add_argument("-d", "--directory", required=True, help="Directorio destino")

    args = parser.parse_args()
    keywords = [k.strip() for k in args.inputs.split(",") if k.strip()]
    suffix = args.suffix.strip() if args.suffix else ""

    state = load_state()
    index = state["last_index"] + 1

    project_name = generate_project_name(index, keywords, suffix)
    save_state(index)

    full_path = os.path.join(args.directory, project_name)
    os.makedirs(full_path, exist_ok=True)

    print(f"Nombre del proyecto: {project_name}")
    print(f"Directorio creado: {full_path}")


if __name__ == "__main__":
    main()