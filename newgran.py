#!/usr/bin/env python3
import argparse
import os
import json

GREEK_ALPHABET = [
    'alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta', 'theta',
    'iota', 'kappa', 'lambda', 'mu', 'nu', 'xi', 'omicron', 'pi', 'rho',
    'sigma', 'tau', 'upsilon', 'phi', 'chi', 'psi', 'omega'
]

STATE_FILE = os.path.expanduser("~/.gran_state")

def load_states():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return []

def save_states(states):
    with open(STATE_FILE, 'w') as f:
        json.dump(states, f, indent=2)

def get_last_index_for_dir(states, current_dir):
    for entry in states:
        if entry["dir"] == current_dir:
            return entry["last_index"]
    return -1

def update_last_index_for_dir(states, current_dir, new_index):
    for entry in states:
        if entry["dir"] == current_dir:
            entry["last_index"] = new_index
            return states
    states.append({"dir": current_dir, "last_index": new_index})
    return states

def get_prefix(index):
    base = len(GREEK_ALPHABET)
    if index < base:
        return GREEK_ALPHABET[index]
    prefix_parts = []
    while index >= 0:
        prefix_parts.append(GREEK_ALPHABET[index % base])
        index = index // base - 1
    return ''.join(reversed(prefix_parts))

def generate_project_name(index, keywords, suffix):
    prefix = get_prefix(index)
    words = "-".join([*keywords, suffix]) if suffix else "-".join(keywords)
    return f"{prefix}-{words}"

def get_used_prefixes_in_dir(directory):
    dirs = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
    return set(d.split("-")[0] for d in dirs)

def main():
    parser = argparse.ArgumentParser(description="Generador de nombres de proyecto estilo GRAN")
    parser.add_argument("-i", "--inputs", required=True, help="Palabras clave separadas por coma")
    parser.add_argument("-s", "--suffix", help="Sufijo del nombre (ej: books)")
    parser.add_argument("-d", "--directory", help="Directorio destino (opcional, por defecto el actual)")
    args = parser.parse_args()

    keywords = [k.strip() for k in args.inputs.split(",") if k.strip()]
    suffix = args.suffix.strip() if args.suffix else ""
    target_dir = os.path.abspath(args.directory) if args.directory else os.getcwd()

    states = load_states()
    last_index = get_last_index_for_dir(states, target_dir)

    used_prefixes = get_used_prefixes_in_dir(target_dir)

    # Buscar primer índice no usado
    next_index = None
    for i in range(last_index + 1):
        test_prefix = get_prefix(i)
        # Generar nombre base sin palabras aún
        if test_prefix not in used_prefixes:
            next_index = i
            break

    if next_index is None:
        next_index = last_index + 1

    # Generar nombre final
    project_name = generate_project_name(next_index, keywords, suffix)
    full_path = os.path.join(target_dir, project_name)

    if os.path.exists(full_path):
        print(f"⚠️  El directorio ya existe: {full_path}")
        print(f"Nombre del proyecto ya fue usado: {project_name}")
        return

    os.makedirs(full_path)
    print(f"✅ Nombre del proyecto: {project_name}")
    print(f"📁 Directorio creado: {full_path}")

    # Guardar nuevo índice (el más alto generado)
    updated_states = update_last_index_for_dir(states, target_dir, max(last_index, next_index))
    save_states(updated_states)

if __name__ == "__main__":
    main()