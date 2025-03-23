import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import gradio as gr
from agents.myagent import ask_tariffwhisperer

################################################################################
# Description & Example queries
################################################################################

description = """
# TariffWhisperer
**AI-Powered HTS Classification Agent**  
Enter a product description below, and TariffWhisperer will return the most likely **10-digit HTS code**, a legal **justification**, and the relevant **CBP ruling** used for reference.

**Key Features**:
- Powered by Mistral-7B + FAISS RAG on official CBP Rulings  
- Trained on thousands of real customs rulings  
- Provides legal justification with references to official rulings  
"""

examples = [
    ["Wireless Bluetooth earbuds with microphone and charging case"],
    ["Men's 100% cotton t-shirts, short sleeve"],
    ["Plastic storage containers for food"],
    ["Smartwatch with heart rate monitoring and notifications"],
    ["Girls' toddler cotton knit sailor dress with matching panty"]
]

################################################################################
# Custom CSS for a modern, aesthetic look
################################################################################

css = """
/* Import a modern font from Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

/* Global body styling */
body {
    margin: 0;
    padding: 0;
    background: #f0f4f8;
    font-family: 'Poppins', sans-serif;
}

/* Main Gradio container */
.gradio-container {
    max-width: 1100px;
    margin: 40px auto !important;
    background: #ffffff;
    border-radius: 20px;
    box-shadow: 0px 15px 40px rgba(0, 0, 0, 0.1);
    padding: 30px;
}

/* Heading and subtext styling */
.gradio-container h1 {
    font-size: 2.2em;
    font-weight: 600;
    color: #2c3e50;
    text-align: center;
    margin-bottom: 0.3em;
}

.subtext {
    text-align: center;
    color: #34495e;
    margin-bottom: 1.5em;
    font-size: 1rem;
    line-height: 1.6;
}

/* Row and column styling */
.gr-row {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
}

.gr-column {
    flex: 1;
}

/* Labels for inputs/outputs */
label {
    font-weight: 500;
    margin-bottom: 6px;
    display: inline-block;
    color: #2c3e50;
}

/* Buttons */
button {
    background-color: #3498db;
    border: none;
    color: #fff;
    padding: 12px 25px;
    font-size: 1rem;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    margin-right: 10px;
}
button:hover {
    background-color: #2980b9;
}

/* Textboxes and text areas */
textarea, input[type="text"] {
    border-radius: 12px !important;
    border: 1px solid #dfe6e9 !important;
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05) !important;
}

/* Classification results box */
#results-box {
    background-color: #f7f9fc !important;
    resize: none !important;
    min-height: 300px !important;
}

/* Footer */
.footer {
    text-align: center;
    margin-top: 30px;
    font-size: 0.9em;
    color: #7f8c8d;
}

/* Logo */
#header-img {
    display: block;
    margin: 0 auto 20px;
    height: 80px;
}
"""

################################################################################
# Build the Gradio Interface
################################################################################

def build_interface():
    # Use Blocks, but skip theme=... for Gradio 3.37.0 compatibility
    demo = gr.Blocks(css=css)

    with demo:
        # Logo at the top
        gr.HTML("""
            <img id="header-img" src="https://img.icons8.com/fluency/96/customs.png" alt="Customs Icon">
        """)
        
        # Main headings
        gr.Markdown(description, elem_classes=["subtext"])
        
        # Layout
        with gr.Row():
            with gr.Column(scale=3):
                # User input
                query_input = gr.Textbox(
                    label="Product Description",
                    placeholder="Enter detailed product description (materials, function, components, etc.)",
                    lines=5
                )
                
                with gr.Row():
                    submit_btn = gr.Button("Classify Product")
                    clear_btn = gr.Button("Clear")
                
                # Examples
                gr.Markdown("### Example Queries")
                gr.Examples(
                    examples=examples,
                    inputs=query_input
                )
                
            with gr.Column(scale=4):
                gr.Markdown("### Classification Results")
                output = gr.Textbox(
                    label="",
                    placeholder="HTS classification results will appear here...",
                    lines=12,
                    elem_id="results-box"
                )
        
        # Tips section
        gr.Markdown("""
        ### Tips for Accurate Classification
        
        1. **Be specific** about materials (e.g., "100% cotton" rather than just "fabric").
        2. **Describe function** and intended use of the product.
        3. **Mention key components** and how they interact.
        4. **Include dimensions** when relevant to classification.
        5. **Specify end-use** (e.g., "for industrial use" vs "for retail sale").
        """)
        
        # Footer
        gr.HTML("""
        <div class="footer">
            <p>Powered by Mistral-7B and LangChain | Developed by Customs Intelligence</p>
        </div>
        """)

        # Button actions
        submit_btn.click(
            fn=ask_tariffwhisperer,
            inputs=query_input,
            outputs=output
        )
        
        # Clear both input and output
        clear_btn.click(
            fn=lambda: ("", ""),
            inputs=None,
            outputs=[query_input, output]
        )

    return demo

if __name__ == "__main__":
    interface = build_interface()
    interface.launch()
