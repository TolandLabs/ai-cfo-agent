import os
from openai import OpenAI

def commentary(analysis, client=None):
    if client is None:
        if not os.getenv('OPENAI_API_KEY'):
            raise ValueError('Set OPENAI_API_KEY to enable optional commentary')
        client = OpenAI()
    summary = {key: analysis[key] for key in ('revenue', 'expense', 'operating_result', 'budget_result')}
    summary['findings'] = [{'month': f.month, 'department': f.department, 'type': f.kind, 'amount': f.amount} for f in analysis['findings'][:10]]
    response = client.chat.completions.create(model='gpt-4.1-mini', messages=[{'role': 'system', 'content': 'Summarize only supplied financial facts. Do not invent causes. Identify items needing verification.'}, {'role': 'user', 'content': str(summary)}])
    return response.choices[0].message.content
