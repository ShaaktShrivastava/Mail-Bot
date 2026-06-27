"""MailPilot - AI Email Management Agent"""
import os
from dotenv import load_dotenv
from agent import MailPilotAgent
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

load_dotenv()

console = Console()

def main():
    console.print(Panel.fit(
        "[bold cyan]MailPilot[/bold cyan] 📧\n"
        "AI-Powered Email Management Agent",
        border_style="cyan"
    ))
    
    if not os.path.exists('credentials.json'):
        console.print("[red]Error: credentials.json not found![/red]")
        console.print("Please set up Google OAuth credentials first.")
        console.print("See README.md for instructions.")
        return
    
    if not os.getenv('GEMINI_API_KEY'):
        console.print("[red]Error: GEMINI_API_KEY not set![/red]")
        console.print("Please create a .env file with your Gemini API key.")
        return
    
    console.print("\n[green]Initializing MailPilot...[/green]\n")
    
    try:
        agent = MailPilotAgent()
        console.print("[green]✓ Connected to Gmail[/green]")
        console.print("[green]✓ LLM initialized[/green]\n")
    except Exception as e:
        console.print(f"[red]Initialization failed: {e}[/red]")
        return
    
    console.print("[yellow]Example commands:[/yellow]")
    console.print("  • My name is John Smith (set your name for signatures)")
    console.print("  • Show me unread emails")
    console.print("  • Summarize my inbox")
    console.print("  • Send email to john@example.com about the meeting")
    console.print("  • Search for emails with attachments")
    console.print("  • Star email ID [xyz]")
    console.print("  • Type 'exit' to quit\n")
    
    while True:
        try:
            user_input = console.input("[bold blue]You:[/bold blue] ")
            
            if not user_input.strip():
                continue
            
            if user_input.lower() in ['exit', 'quit', 'q']:
                console.print("\n[cyan]Goodbye! 👋[/cyan]")
                break
            
            console.print()
            response = agent.process_request(user_input)
            
            console.print(Panel(
                Markdown(response),
                title="[bold cyan]MailPilot[/bold cyan]",
                border_style="cyan"
            ))
            console.print()
            
        except KeyboardInterrupt:
            console.print("\n\n[cyan]Goodbye! 👋[/cyan]")
            break
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]\n")

if __name__ == "__main__":
    main()
