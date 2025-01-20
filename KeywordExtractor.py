from transformers import Tool

class KeywordExtractor(Tool):
    name = "KeywordExtractor"
    description = '''This tool is expert in extracting keywords, it STRICTLY gives results in the following format: ```JSON{{[keyword1, keyword2, ...]}}```'''

    inputs = {
        "keywords": {"type": "string", "description": "keywords present in resume in string format strictly seperated by comma"}
    }
    # input_type = "string"
    outputs = { 
        "keywords": {"type": "string", "description": "keywords present in resume in string format strictly seperated by comma"}
    }
    output_type = "string"

    def forward(self, keywords: str) -> str:
        return keywords