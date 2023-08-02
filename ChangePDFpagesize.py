import os
import PyPDF2
import tkinter as tk
from tkinter import filedialog
from PyPDF2 import PdfFileReader, PdfFileWriter

def file_select():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    file_entry.delete(0, tk.END)
    file_entry.insert(tk.END, file_path)

def resize_pdf(input_file):
    output_file = input_file[:-4] + "_resized.pdf"

    pdf = PdfFileReader(input_file, strict=False)
    out_pdf = PdfFileWriter()

    for page in range(pdf.getNumPages()):
        page_obj = pdf.getPage(page)
        width = page_obj.mediaBox.getWidth()
        height = page_obj.mediaBox.getHeight()

        if width > height:
            # Landscape page will be resized as landscape
            A4_WIDTH = 842.0
            A4_HEIGHT = 595.0
        else:
            # Portrait page will be resized as portrait
            A4_WIDTH = 595.0
            A4_HEIGHT = 842.0

        page_obj.scaleTo(A4_WIDTH, A4_HEIGHT)
        out_pdf.addPage(page_obj)

    with open(output_file, "wb") as fp:
        out_pdf.write(fp)

    return output_file

def display_message(message):
    result_label.config(text=message)
    error_text.config(state=tk.NORMAL)
    error_text.delete("1.0", tk.END)
    error_text.insert(tk.END, message)
    error_text.config(state=tk.DISABLED)

def resize_and_save():
    input_file = file_entry.get()

    if os.path.exists(input_file):
        try:
            output_file = resize_pdf(input_file)
            display_message("Successfully resized the PDF. Saved to: " + output_file)
        except Exception as e:
            display_message("Error: " + str(e))
    else:
        display_message("Error: File not found.")

# GUI
root = tk.Tk()
root.title("PDF Resizer")
root.geometry("700x400")

file_label = tk.Label(text="Select PDF File:")
file_label.pack(pady=5)

file_entry = tk.Entry(width=70)
file_entry.pack(pady=5)

browse_button = tk.Button(text="Browse", command=file_select)
browse_button.pack(pady=5)

resize_button = tk.Button(text="Resize PDF", command=resize_and_save)
resize_button.pack(pady=10)

result_label = tk.Label(text="")
result_label.pack(pady=5)

error_text = tk.Text(width=80, height=5, state=tk.DISABLED)
error_text.pack(pady=5)

root.mainloop()
