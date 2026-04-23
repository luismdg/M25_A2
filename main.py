import argparse

from presentation import handle_prompt, handle_presentacion
from negocio import (
    get_db_description,
    describe_table,
    preview_schema,
    get_column_info
)
from data import get_all_data, get_limited_data
from persistencia import ejecutar_query
from prompt import ejemplo_prompts


def print_help():
    print("\n===== SISTEMA CLI POR CAPAS =====\n")

    print("📌 COMANDOS DISPONIBLES:\n")

    print("1) 🔵 PRESENTACIÓN (flujo completo con LLM)")
    print('   python main.py --prompt "Dame 10 accidentes"\n')

    print("2) 🟡 PRESENTACIÓN SIMPLE (sin procesamiento)")
    print('   python main.py --presentacion "Hola mundo"\n')

    print("3) 🟢 NEGOCIO (estructura de datos)")
    print("   python main.py --negocio all        → Descripción general")
    print("   python main.py --negocio describe   → Tipo DESCRIBE SQL")
    print("   python main.py --negocio preview    → Preview de datos")
    print("   python main.py --negocio column State  → Info de columna\n")

    print("4) 🟣 DATA (acceso directo)")
    print("   python main.py --data all")
    print("   python main.py --data 5\n")

    print("5) 🔴 PERSISTENCIA (query directa)")
    print('   python main.py --query "SELECT * FROM accidentes LIMIT 5"\n')

    print("💡 EJEMPLOS DE PROMPTS:")
    for p in ejemplo_prompts():
        print(f"   - {p}")

    print("\n====================================\n")


def main():
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument("--prompt", type=str)
    parser.add_argument("--presentacion", type=str)
    parser.add_argument("--negocio", nargs="+")
    parser.add_argument("--data", type=str)
    parser.add_argument("--query", type=str)

    args = parser.parse_args()

    print("\n===== SISTEMA CLI POR CAPAS =====")

    # ==== PRESENTACION (FULL FLOW) ====
    if args.prompt:
        result = handle_prompt(args.prompt)

        print("\n=== FLUJO COMPLETO (PROMPT) ===")
        print(f"\n🧠 Prompt: {result['prompt']}")
        print(f"\n📄 Query generado:\n{result['query_generado']}")
        print(f"\n📊 Resultado:\n{result['resultado']}")

    # ==== PRESENTACION SIMPLE ====
    elif args.presentacion:
        result = handle_presentacion(args.presentacion)

        print("\n=== CAPA PRESENTACION ===")
        print(result)

    # ==== NEGOCIO ====
    elif args.negocio:
        print("\n=== CAPA NEGOCIO ===")

        cmd = args.negocio

        if cmd[0] == "all":
            print("\n📘 DESCRIPCIÓN GENERAL:\n")
            print(get_db_description())

        elif cmd[0] == "describe":
            print("\n📘 DESCRIBE TABLE:\n")
            for col in describe_table():
                print(col)

        elif cmd[0] == "preview":
            print("\n📘 PREVIEW (5 filas):\n")
            print(preview_schema())

        elif cmd[0] == "column":
            if len(cmd) < 2:
                print("❌ Debes especificar una columna")
            else:
                print(f"\n📘 INFO COLUMNA ({cmd[1]}):\n")
                print(get_column_info(cmd[1]))

        else:
            print("❌ Comando de negocio no válido")

    # ==== DATA ====
    elif args.data:
        print("\n=== CAPA DATA ===")

        if args.data == "all":
            print(get_all_data())
        else:
            try:
                n = int(args.data)
                print(get_limited_data(n))
            except:
                print("❌ Valor inválido para --data")

    # ==== PERSISTENCIA ====
    elif args.query:
        print("\n=== CAPA PERSISTENCIA ===")
        print(f"\n📄 Query: {args.query}")

        result = ejecutar_query(args.query)
        print("\n📊 Resultado:\n", result)

    # ==== HELP ====
    else:
        print_help()


if __name__ == "__main__":
    main()