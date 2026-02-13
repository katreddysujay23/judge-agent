# Judge Agent

A production-style evaluation service that analyzes text and video content across four dimensions:

- AI-generated vs Human-generated prediction  
- Virality score (0–100)  
- Distribution analysis (likely audiences + reasoning)  
- Structured explanation with confidence modeling  

The system is designed with strict schema validation, defensive engineering principles, and structured JSON contracts.

---

## API Contract

The Judge Agent exposes a single evaluation endpoint:

**POST** `/evaluate`

All inputs and outputs are strictly validated using **Pydantic (v2)**.  
Unexpected or malformed fields are rejected.

---

## Example Request

```json
{
  "type": "text",
  "content": "AI is transforming how startups build products.",
  "metadata": {
    "platform": "twitter",
    "duration_seconds": null
  }
}
