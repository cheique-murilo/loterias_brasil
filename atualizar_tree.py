import os
import re

ICONS = {
    "folder": "📁",
    "file": "📄",
    "image": "🖼️",
}

IMAGE_EXT = {".png", ".jpg", ".jpeg", ".gif", ".svg"}


def icon_for(file):
    ext = os.path.splitext(file)[1].lower()
    if ext in IMAGE_EXT:
        return ICONS["image"]
    return ICONS["file"]


def gerar_tree(path, prefix=""):
    linhas = []
    items = sorted(os.listdir(path))
    items = [i for i in items if i not in {"__pycache__", ".git"}]

    for i, item in enumerate(items):
        full = os.path.join(path, item)
        connector = "└── " if i == len(items) - 1 else "├── "

        if os.path.isdir(full):
            linhas.append(prefix + connector + f"{ICONS['folder']} {item}")
            new_prefix = prefix + ("    " if i == len(items) - 1 else "│   ")
            linhas.extend(gerar_tree(full, new_prefix))
        else:
            linhas.append(prefix + connector + f"{icon_for(item)} {item}")

    return linhas


def atualizar_readme():
    tree = ["📁 projeto_loterias"] + gerar_tree(".")

    with open("README.md", "r", encoding="utf-8") as f:
        conteudo = f.read()

    novo_tree = "```\n" + "\n".join(tree) + "\n```"

    conteudo_atualizado = re.sub(
        r"<!-- TREE_START -->(.*?)<!-- TREE_END -->",
        f"<!-- TREE_START -->\n{novo_tree}\n<!-- TREE_END -->",
        conteudo,
        flags=re.DOTALL,
    )

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(conteudo_atualizado)

    print("README.md atualizado com sucesso!")


if __name__ == "__main__":
    atualizar_readme()
