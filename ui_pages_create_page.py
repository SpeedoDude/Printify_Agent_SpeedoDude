# ui/pages/create_page.py

import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLabel, 
    QLineEdit, QPushButton, QTextBrowser, QFileDialog, QHBoxLayout
)
from PyQt6.QtCore import Qt

# Import the backend agent
from seo_agent import SEOAgent

class CreatePage(QWidget):
    """
    A page for creating products, now with an integrated SEO content generator.
    """
    def __init__(self):
        super().__init__()

        # --- Main Layout ---
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # =====================================================================
        # SEO Content Generation Section
        # =====================================================================
        seo_group_label = QLabel("Step 1: Generate SEO Content")
        seo_group_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 10px;")

        seo_form_layout = QFormLayout()
        self.keyword_input = QLineEdit()
        self.keyword_input.setPlaceholderText("e.g., 'Vintage Surfing Poster'")
        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("e.g., 'T-shirt' or 'Mug'")
        self.brand_input = QLineEdit()
        self.brand_input.setPlaceholderText("(Optional) e.g., 'SpeedoDude'")
        self.tone_input = QLineEdit()
        self.tone_input.setPlaceholderText("(Optional) e.g., 'Humorous, Retro'")
        
        seo_form_layout.addRow("Primary Keyword:", self.keyword_input)
        seo_form_layout.addRow("Product Category:", self.category_input)
        seo_form_layout.addRow("Brand Name:", self.brand_input)
        seo_form_layout.addRow("Style/Tone:", self.tone_input)

        self.seo_button = QPushButton("✨ Generate SEO Title & Description")
        self.seo_button.clicked.connect(self.run_seo_generation)
        self.seo_button.setMinimumHeight(35)

        self.seo_results_display = QTextBrowser()
        self.seo_results_display.setPlaceholderText("Generated SEO content will appear here...")
        self.seo_results_display.setMinimumHeight(200)

        # =====================================================================
        # Product Creation Section
        # =====================================================================
        product_group_label = QLabel("Step 2: Define Product Details & Create")
        product_group_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 20px;")
        
        product_form_layout = QFormLayout()
        self.blueprint_input = QLineEdit()
        self.provider_input = QLineEdit()
        self.csv_input = QLineEdit()
        self.image_folder_input = QLineEdit()

        self.generate_button = QPushButton("🚀 Generate Products")
        self.generate_button.clicked.connect(self.generate_products)
        self.generate_button.setMinimumHeight(35)

        # File/Folder selection buttons
        csv_button = QPushButton("Select CSV")
        csv_button.clicked.connect(self.select_csv_file)
        image_button = QPushButton("Select Folder")
        image_button.clicked.connect(self.select_image_folder)

        # Use QHBoxLayout for inputs with buttons
        csv_layout = QHBoxLayout()
        csv_layout.addWidget(self.csv_input)
        csv_layout.addWidget(csv_button)
        
        image_layout = QHBoxLayout()
        image_layout.addWidget(self.image_folder_input)
        image_layout.addWidget(image_button)

        product_form_layout.addRow("Blueprint ID:", self.blueprint_input)
        product_form_layout.addRow("Print Provider ID:", self.provider_input)
        product_form_layout.addRow("Data CSV File:", csv_layout)
        product_form_layout.addRow("Image Folder:", image_layout)

        # --- Add all widgets to the main layout ---
        main_layout.addWidget(seo_group_label)
        main_layout.addLayout(seo_form_layout)
        main_layout.addWidget(self.seo_button)
        main_layout.addWidget(self.seo_results_display)
        
        main_layout.addWidget(product_group_label)
        main_layout.addLayout(product_form_layout)
        main_layout.addWidget(self.generate_button)

    def select_csv_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Data CSV", "", "CSV Files (*.csv)")
        if file_name:
            self.csv_input.setText(file_name)

    def select_image_folder(self):
        folder_name = QFileDialog.getExistingDirectory(self, "Select Image Folder")
        if folder_name:
            self.image_folder_input.setText(folder_name)

    def run_seo_generation(self):
        """
        Gets user inputs, runs the SEO agent, and displays the formatted results.
        """
        primary_keyword = self.keyword_input.text()
        product_category = self.category_input.text()

        if not primary_keyword or not product_category:
            self.seo_results_display.setText("🚨 Please provide a Primary Keyword and a Product Category.")
            return

        self.seo_button.setEnabled(False)
        self.seo_button.setText("Generating...")
        self.seo_results_display.setText("🧠 Calling Gemini API... Please wait.")
        QApplication.processEvents() # Ensure UI updates

        try:
            agent = SEOAgent()
            content = agent.generate_seo_content(
                primary_keyword=primary_keyword,
                product_category=product_category,
                brand_name=self.brand_input.text(),
                style_tone=self.tone_input.text()
            )

            if content and content.get('titles'):
                html_output = "<h3>✅ SEO Content Generated</h3><h4>Titles:</h4><ul>"
                for title in content.get('titles', []):
                    html_output += f"<li>{title}</li>"
                html_output += "</ul><h4>Description:</h4>"
                html_output += f"<p>{content.get('description', 'No description generated.')}</p>"
                self.seo_results_display.setHtml(html_output)
            else:
                self.seo_results_display.setText("❌ Failed to generate content. Check console for errors.")
        except Exception as e:
            self.seo_results_display.setText(f"An error occurred: {e}")
        finally:
            self.seo_button.setEnabled(True)
            self.seo_button.setText("✨ Generate SEO Title & Description")

    def generate_products(self):
        """Placeholder for the final product generation logic."""
        print("--- Initiating Product Generation ---")
        print(f"Blueprint ID: {self.blueprint_input.text()}")
        print(f"Provider ID: {self.provider_input.text()}")
        print(f"CSV File: {self.csv_input.text()}")
        print(f"Image Folder: {self.image_folder_input.text()}")
        print("\n--- Using SEO Content ---")
        # You can now access the generated content for your next steps
        print(self.seo_results_display.toPlainText())

# This is for standalone testing of the page
if __name__ == '__main__':
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = CreatePage()
    window.setWindowTitle("Create Page Test")
    window.show()
    sys.exit(app.exec())
