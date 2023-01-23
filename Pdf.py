import PyPDF2

Docname = "Tarea-22.01.2023-1.docx"
with open(Docname, 'rb') as f:
    # Leer el archivo de word
    reader = PyPDF2.PdfReader(f)
    # Crear un objeto PdfFileWriter
    writer = PyPDF2.PdfWriter()
    # Añadir cada página del archivo word al nuevo pdf
    for page in range(reader.numPages):
        writer.addPage(reader.getPage(page))
    # Guardar el archivo pdf
    
    with open(Docname, 'wb') as pdf:
        writer.write(pdf)
