import asyncio
import tkinter as tk
from todo_app import TodoApp

async def main() -> None:
    """
    Main function to initialize and run the Todo application.
    """
    root = tk.Tk()
    app = TodoApp(root)
    await app.initialize_db()

    # Run the Tkinter main loop with asyncio compatibility
    while True:
        root.update()
        await asyncio.sleep(0.01)

if __name__ == "__main__":
    asyncio.run(main())
