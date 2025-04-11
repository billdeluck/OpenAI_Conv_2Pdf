import json
from fpdf import FPDF

def convert_conversations_to_pdf(json_file_path, pdf_output_path="ChatGPT_Conversations.pdf"):
    """
    Converts ChatGPT conversations from a JSON file to a PDF.

    Args:
        json_file_path (str): The path to the conversations.json file.
        pdf_output_path (str, optional): The path where the PDF will be saved.
            Defaults to "ChatGPT_Conversations.pdf".
    """

    try:
        with open(json_file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found at {json_file_path}")
        return
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {json_file_path}")
        return

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="ChatGPT Conversations", ln=True, align='C')
    pdf.ln(10)

    # Handle different possible JSON structures
    if isinstance(data, dict) and "conversations" in data:
        conversations = data["conversations"]
    elif isinstance(data, list):
        conversations = data
    else:
        print("Error: Unexpected JSON structure. Please check the format of your JSON file.")
        return

    for chat in conversations:
        pdf.set_font("Arial", style='B', size=12)
        pdf.cell(200, 10, txt=f"Conversation {chat.get('id', '')}", ln=True)
        pdf.ln(5)

        messages = chat.get("messages", [])  # Safely get messages

        for msg in messages:
            author = "User" if msg.get("author") == "user" else "ChatGPT"
            pdf.set_font("Arial", style='B', size=11)
            pdf.cell(200, 8, txt=f"{author}:", ln=True)

            pdf.set_font("Arial", size=11)
            pdf.multi_cell(0, 8, msg.get("text", ""))  # Safely get text
            pdf.ln(3)

    pdf.output(pdf_output_path)
    print(f"PDF generated successfully: {pdf_output_path}")

# Example usage:
json_file_path = "chats/conversations.json"  # Corrected file path
convert_conversations_to_pdf(json_file_path)