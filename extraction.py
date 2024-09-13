from transformers import pipeline
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter, ImageFile
import fitz  # PyMuPDF
import zipfile
import re
import os
from langdetect import detect
from translate import Translator
from transformers import pipeline
from datetime import datetime 
from collections import Counter, defaultdict
from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration
import google.generativeai as genai
from dotenv import load_dotenv


# Function to extract text from an image file
def extract_text_from_image(image):
    try:
        # Convert image to grayscale and enhance contrast for better OCR
        gray_image = image.convert('L')
        enhancer = ImageEnhance.Contrast(gray_image)
        enhanced_image = enhancer.enhance(2)
        enhanced_image = enhanced_image.filter(ImageFilter.SHARPEN)
        
        # Extract text using Tesseract OCR
        #text = pytesseract.image_to_string(enhanced_image, lang='eng+ara+deu+spa+fra+ita+por+rus+chi_sim+chi_tra+jpn')
        text = pytesseract.image_to_string(enhanced_image, lang='eng')
        return text.strip() if text.strip() else 'None'
    except Exception as e:
        print(f"Error processing image: {e}")
        return 'None'


# Function to extract text from a PDF file
def extract_text_from_pdf(file_stream):
    try:
        doc = fitz.open(stream=file_stream.read(), filetype="pdf")
        text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text("text")
        doc.close()
        return text.strip() if text.strip() else 'None'
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return 'None'

# Function to clean extracted text
def clean_text(text):
  text = re.sub(r'\[.*?\]', '', text)  # Remove text within brackets
  text = re.sub(r'[-*]', ' ', text)  # Replace hyphens and asterisks with spaces
  text = re.sub(r'\s+', ' ', text).strip()  # Remove extra whitespace
  return text


def split_text(text, max_length):
        """
        Splits the input text into chunks of maximum `max_length` characters.
        """
        return [text[i:i + max_length] for i in range(0, len(text), max_length)]

def detect_and_translate(text):
    detected_language = detect(text)
    print(f"Detected Language: {detected_language}")

    translator = Translator(to_lang="en", from_lang=detected_language)
    text_chunks = split_text(text, 500)  # Translate in chunks of up to 500 characters

    translated_chunks = [translator.translate(chunk) for chunk in text_chunks]
    full_translation = ' '.join(translated_chunks)
    cleaned_translated_text = clean_text(full_translation)

    print(f"Cleaned Translated Text: {cleaned_translated_text}")
    return cleaned_translated_text

def config_genai(genaiapi=None):
    # Load environment variables from .env file
    load_dotenv()

    # Retrieve the Google API key from environment variables
    #GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    GOOGLE_API_KEY = 'AIzaSyDpCg46eGiCgS8CTzv1x4iQl7811MLAJOs'

    # Configure the generative AI model
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    return model

# Initialize the model
model = config_genai()
