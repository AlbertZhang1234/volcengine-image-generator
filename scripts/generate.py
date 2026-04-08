import sys
import json
import os
from dotenv import load_dotenv
from volcenginesdkarkruntime import Ark

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python generate.py '<json_payload>'"}), file=sys.stderr)
        sys.exit(1)
        
    payload_str = sys.argv[1]
    
    try:
        payload = json.loads(payload_str)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON payload: {e}"}), file=sys.stderr)
        sys.exit(1)
        
    if "model" not in payload or "prompt" not in payload:
        print(json.dumps({"error": "Missing required fields: 'model' and 'prompt'"}), file=sys.stderr)
        sys.exit(1)
        
    # Load .env explicitly if present
    load_dotenv()
    
    api_key = os.getenv("ARK_API_KEY")
    if not api_key:
        print(json.dumps({"error": "ARK_API_KEY environment variable is missing"}), file=sys.stderr)
        sys.exit(1)
        
    client = Ark(api_key=api_key)
    
    try:
        # Call the official SDK generate method unpacking all provided payload parameters
        response = client.images.generate(**payload)
        
        # Process the response into a JSON-serializable format
        results = []
        if getattr(response, "data", None):
            for img_data in response.data:
                img_obj = {}
                if getattr(img_data, "url", None):
                    img_obj["url"] = img_data.url
                if getattr(img_data, "b64_json", None):
                    img_obj["b64_json"] = img_data.b64_json
                if getattr(img_data, "size", None):
                    img_obj["size"] = img_data.size
                    
                # Handle error if any specific image failed
                if getattr(img_data, "error", None):
                    img_obj["error"] = {
                        "code": getattr(img_data.error, "code", None),
                        "message": getattr(img_data.error, "message", None)
                    }
                results.append(img_obj)
                
        # Handle overall token usage stats
        usage_obj = {}
        if getattr(response, "usage", None):
            usage_obj = {
                "generated_images": getattr(response.usage, "generated_images", 0),
                "output_tokens": getattr(response.usage, "output_tokens", 0),
                "total_tokens": getattr(response.usage, "total_tokens", 0)
            }
            # Handle tool usage
            tool_usage = getattr(response.usage, "tool_usage", None)
            if tool_usage:
                usage_obj["tool_usage"] = {
                    "web_search": getattr(tool_usage, "web_search", 0)
                }

        # Output the successful results as JSON
        output = {
            "status": "success", 
            "data": results,
            "usage": usage_obj,
            "model": getattr(response, "model", payload.get("model")),
            "created": getattr(response, "created", 0)
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
