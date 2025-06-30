import json
import ast

def generate_report(raw_response, verification_results):

    try:
        citations = ast.literal_eval(raw_response)
    except Exception as e:
        citations = [{"error": str(e)}]  #fixed closing quote

    report_lines = []
    report_lines.append("=== Citation Extraction Report ===\n")

    for i, citation in enumerate(citations):
        report_lines.append(f"Citation {i+1}:")
        for key, value in citation.items():
            report_lines.append(f"  {key}: {value}")
        report_lines.append("")

    report_lines.append("\n=== Verification Results ===\n")
    for result in verification_results:
        if "error" in result:
            report_lines.append(f"Error: {result['error']}")
        else:
            report_lines.append(json.dumps(result, indent=2))

    return "\n".join(report_lines)
