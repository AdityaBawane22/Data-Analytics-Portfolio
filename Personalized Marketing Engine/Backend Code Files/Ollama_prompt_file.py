import ollama

def generate_ollama_message(cluster_id, selected_offer, segment_data, event_today=None):
    """
    Generates a short SMS marketing message for a given cluster/offer/event.
    """
    segment = segment_data['segment'].split('(')[0].strip()
    event_str = event_today if event_today else "Standard Promotion Day"

    prompt = f"""
You are a professional marketing copywriter.
Generate ONE short, classy, professional SMS (max 300 characters)
for the following:

Segment: {segment}
Current Event: {event_str}
Offer: {selected_offer}

Message Only: Output only the message text. Do not include any prefixes, intros, explanations, links, hashtags, or identifiers.

No Leading Text: Never start with phrases like “Here’s the message”, “Check this out”, “Here’s a draft message:”, or any similar introduction.

Uniqueness: Every message must be fully unique. Avoid repeating words, phrases, or sentence structures from previous messages. Each generation should feel fresh and original.

Character Limit: Keep the message under 300 characters, including spaces and punctuation.

Tone & Style:

Classy and professional – sound polished and premium.

Friendly and approachable – engage the recipient warmly.

Creative and attention-grabbing – use imaginative phrasing.

Personalization: Tailor the message specifically to the customer segment. Subtly mention the segment if appropriate.

Event Integration: Seamlessly integrate the current event or promotion as a sophisticated hook.

Action-Oriented: Encourage action gently but effectively. Avoid generic, pushy, or overly salesy language.

Variety: Use varied sentence structures, synonyms, and creative phrasing. Do not reuse the same patterns across messages.

Exclusivity & Value: Convey exclusivity, reward, or value (e.g., “special access”, “exclusive offer”).

Clarity & Brevity: Keep messages clear, concise, and easy to read. Avoid long-winded sentences.

Engagement: Aim for a message that motivates the recipient to act or feel positively about the brand.

No Brand or URL Mentions: Avoid including brand names, store names, shop URLs, or website links.

Strict Output: The response must only contain the final message text. No commentary, description, or meta-text about the SMS. Alos, once you start a message with 
some words, do not use the same word with and the same begining again. Do not mention anything about a brand. Do not make the message very short. 
Length of the message must be moderate. Do not include discount percentage.

Strict Note: Do not mention "Here is the message" before the message

"""

    try:
        response = ollama.chat(
            model="gemma3:1b",
            messages=[{"role": "user", "content": prompt}]
        )
        sms_copy = response["message"]["content"].strip()
        if len(sms_copy) > 300:
            sms_copy = sms_copy[:297] + "..."
        return {"sms_copy": sms_copy}

    except Exception as e:
        return {"error": f"Ollama call failed: {e}"}
