import PyPDF2
import nltk
from nltk.tokenize import word_tokenize
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QPushButton, QVBoxLayout
import sys

nltk.download('punkt')
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text
def split_text_into_30min_chunks(text, words_per_chunk=6000):
    words = word_tokenize(text)
    chunks = []
    current_chunk = []

    for word in words:
        current_chunk.append(word)
        if len(current_chunk) >= words_per_chunk:  # Once we hit ~6000 words, create a chunk
            chunks.append(' '.join(current_chunk))
            current_chunk = []

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks
class CourseApp(QWidget):
    def __init__(self, chunks):
        super().__init__()
        self.chunks = chunks
        self.current_day = 0  # This will track the day/session
        self.init_ui()
        self.load_chunk()

    def init_ui(self):
        self.setWindowTitle('Daily Course Material')

        self.layout = QVBoxLayout()

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.layout.addWidget(self.text_edit)

        self.next_button = QPushButton('Next Day', self)
        self.next_button.clicked.connect(self.load_chunk)
        self.layout.addWidget(self.next_button)

        self.setLayout(self.layout)
        self.show()

    def load_chunk(self):
        if self.current_day < len(self.chunks):
            self.text_edit.setText(self.chunks[self.current_day])
            self.current_day += 1
        else:
            self.text_edit.setText("No more content.")
            self.next_button.setEnabled(False)

def main():
    pdf_path = 'DP-900.pdf'
    full_text = extract_text_from_pdf(pdf_path)
    chunks = split_text_into_30min_chunks(full_text)

    print(f"Total chunks created: {len(chunks)}")

    app = QApplication(sys.argv)
    ex = CourseApp(chunks)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
