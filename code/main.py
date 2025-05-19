import tokenizer as tokenizer
import parser as parser
import interpreter as interpreter

if __name__ == "__main__":
    file = open("code/sample_test.txt", encoding="utf-8")
    whole_text_tokenized = tokenizer.segment_text(file.read())
    print(parser.parse_document(whole_text_tokenized))
