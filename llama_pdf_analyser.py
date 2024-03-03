import os
os.environ['REPLICATE_API_TOKEN'] = "r8_ebs5HbiSwpgAHtrPTQPnRRfx7b2LLOb3K2QJZ"
import replicate
import PyPDF2


def qa_session(question, text_to_be_summarized):
    print("inside qa session")
    answer_txt = ""
    answer = replicate.run("meta/llama-2-70b-chat:2d19859030ff705a87c746f7e96eea03aefb71f166725aee39692f1476566d48", # LLM model
                        input={"prompt": f"text: {text_to_be_summarized} . based on the above text, answer this question :  {question} Assistant: ", # Prompts
                        "temperature":0.1, "top_p":0.9, "max_length":128, "repetition_penalty":1})
   
    for txt in answer:
        answer_txt += txt
    print("done")
    print(answer_txt)
    return answer_txt
   

def summarize_pdf(text_to_be_summarized):
  print("insisde pdf summarizer")
  final_summarised_txt = ""
  summarized_text_itr = replicate.run("meta/llama-2-70b-chat:2d19859030ff705a87c746f7e96eea03aefb71f166725aee39692f1476566d48", # LLM model
                        input={"prompt": f" summarize the below text in 5 lines :  {text_to_be_summarized} Assistant: ", # Prompts
                        "temperature":0.1, "top_p":0.9, "max_length":128, "repetition_penalty":1})
  
  for txt in summarized_text_itr:
    final_summarised_txt += txt
  print("done")
  print(final_summarised_txt)
  return final_summarised_txt


def read_pdf2(file_path="/content/ramayan.pdf"):
    pdf_text = ""
    with open(file_path, 'rb') as file:
        reader_obj = PyPDF2.PdfReader(file)

        num_pages = len(reader_obj.pages)
        print(num_pages)
        for page_num in range(0, num_pages):

            page_obj = reader_obj.pages[page_num]

            # Extract text from the page
            text = page_obj.extract_text()

            pdf_text += text

    return pdf_text

def read_pdf(file):
    pdf_text = ""
    
    reader_obj = PyPDF2.PdfReader(file)

    num_pages = len(reader_obj.pages)
    print(num_pages)
    for page_num in range(0, num_pages):

        page_obj = reader_obj.pages[page_num]

        # Extract text from the page
        text = page_obj.extract_text()

        pdf_text += text
    
    lines = pdf_text.splitlines()
    proper_pdf_txt = ' '.join(lines)
    return proper_pdf_txt

# pdf_txt = read_pdf()

# print(summarize_pdf(pdf_txt))

