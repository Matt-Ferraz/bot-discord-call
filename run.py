import asyncio
from bot import main

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot desligado pelo usuário.")
    except Exception as e:
        print(f"Erro fatal: {e}")