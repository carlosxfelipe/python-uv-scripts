import os
import subprocess
import sys


def run_command(command):
    print(f"\n➡️ Executando: {command}")
    subprocess.run(command, shell=True, check=True)


def main():
    print("🚀 Criador Automático de Projeto Django com UV\n")

    project_name = input("Digite o nome do projeto: ").strip()
    if not project_name:
        print("❌ Nome do projeto inválido.")
        return

    project_path = os.path.join(os.getcwd(), project_name)

    if os.path.exists(project_path) and os.listdir(project_path):
        print(f"❌ A pasta '{project_name}' já existe e não está vazia.")
        print("   Escolha outro nome ou remova/limpe a pasta.")
        return

    os.makedirs(project_path, exist_ok=True)
    os.chdir(project_path)
    print(f"📁 Pasta '{project_name}' criada em: {project_path}")

    python_version = (
        input("Informe a versão do Python (padrão: 3.12): ").strip() or "3.12"
    )
    run_command(f"uv init --python {python_version}")
    run_command("uv add django")
    run_command("uv run django-admin startproject config .")
    run_command("uv run python manage.py migrate")

    print("\n✅ Projeto criado com sucesso!")
    print("➡️ Agora entre na pasta do projeto antes de iniciar o servidor:")
    print(f"   cd {project_path}")
    print("➡️ Para iniciar o servidor de desenvolvimento, execute:")
    print("   uv run python manage.py runserver")
    print("\n🌐 Depois acesse: http://localhost:8000/")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Falha ao executar: {e.cmd}\nCódigo de saída: {e.returncode}")
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        print("\n🔚 Interrompido pelo usuário.")
        sys.exit(130)
