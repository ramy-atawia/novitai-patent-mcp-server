# Tool Input/Output Schema Comparison

## Complete Schema Reference

### Tool 1: web_search

#### Input Schema
| Parameter | Type | Required | Default | Constraints | Description |
|-----------|------|----------|---------|-------------|-------------|
| `query` | string | ✅ Yes | - | minLength: 2 | Search query |
| `max_results` | integer | No | 10 | min: 1, max: 10 | Maximum number of results |

#### Output Schema
```json
{
  "type": "object",
  "properties": {
    "result": {
      "type": "string"
    }
  },
  "required": ["result"]
}
```
**Actual Return**: Markdown-formatted search results string

---

### Tool 2: prior_art_search

#### Input Schema
| Parameter | Type | Required | Default | Constraints | Description |
|-----------|------|----------|---------|-------------|-------------|
| `query` | string | ✅ Yes | - | minLength: 3, maxLength: 1000 | Search query describing the invention or technology |
| `max_results` | integer | No | 20 | min: 1, max: 100 | Maximum number of results to return |
| `context` | string or null | No | null | - | Additional context from document or conversation |
| `conversation_history` | string or null | No | null | - | Conversation history for context |

#### Output Schema
```json
{
  "type": "object",
  "properties": {
    "result": {
      "type": "string"
    }
  },
  "required": ["result"]
}
```
**Actual Return**: Comprehensive prior art analysis report (markdown string)

---

### Tool 3: claim_drafting

#### Input Schema
| Parameter | Type | Required | Default | Constraints | Description |
|-----------|------|----------|---------|-------------|-------------|
| `user_query` | string | ✅ Yes | - | minLength: 10 | Description of the invention or feature to draft claims for |
| `context` | string or null | No | null | - | Additional context from document |
| `conversation_history` | string or null | No | null | - | Conversation history for context |

#### Output Schema
```json
{
  "type": "object",
  "properties": {
    "result": {
      "type": "string"
    }
  },
  "required": ["result"]
}
```
**Actual Return**: AI-generated patent claims in markdown format

**Service Mapping:**
- Tool param `conversation_history` → Service param `conversation_context`
- Tool param `context` → Service param `document_reference`
- Service returns: `(Dict, List)` → Tool extracts `Dict['drafting_report']`

---

### Tool 4: claim_analysis

#### Input Schema
| Parameter | Type | Required | Default | Constraints | Description |
|-----------|------|----------|---------|-------------|-------------|
| `claims` | array[Claim] | ✅ Yes | - | minItems: 1 | List of claims to analyze |
| `analysis_type` | string | No | "basic" | - | Type of analysis: 'basic' or 'detailed' |
| `focus_areas` | array[string] | No | [] | - | Specific areas to focus analysis on |
| `context` | string or null | No | null | - | Additional context for analysis |

#### Claim Schema (nested)
| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `claim_text` | string | ✅ Yes | The text of the patent claim |

#### Output Schema
```json
{
  "type": "object",
  "properties": {
    "result": {
      "type": "string"
    }
  },
  "required": ["result"]
}
```
**Actual Return**: Comprehensive claim analysis report (markdown string)

**Service Mapping:**
- Service expects: List[Dict] with `{'claim_text': str}`
- Service returns: `(Dict, List)` → Tool extracts `Dict['analysis_report']`

---

## Summary Table

| Tool | Required Inputs | Optional Inputs | Output Type | Actual Value |
|------|-----------------|-----------------|-------------|--------------|
| **web_search** | `query` (str) | `max_results` (int) | string | Markdown search results |
| **prior_art_search** | `query` (str) | `max_results` (int), `context` (str), `conversation_history` (str) | string | Prior art analysis report |
| **claim_drafting** | `user_query` (str) | `context` (str), `conversation_history` (str) | string | Patent claims (markdown) |
| **claim_analysis** | `claims` (array) | `analysis_type` (str), `focus_areas` (array), `context` (str) | string | Analysis report (markdown) |

## Schema Validation Status

✅ **All tools**: Input and output schemas are properly validated
✅ **All tools**: Return string type as advertised
✅ **All tools**: Pass FastMCP schema validation
✅ **Parameter mapping**: Correctly mapped between tool and service layers

## Key Points

1. **Common Output Pattern**: All tools return `{"result": "string"}` via `x-fastmcp-wrap-result: true`
2. **Markdown Format**: All outputs are markdown-formatted strings
3. **Optional Parameters**: Most tools have optional context/conversation parameters
4. **Array Parameters**: `claim_analysis` accepts array of Claim objects
5. **String Constraints**: All required string parameters have minLength/maxLength

