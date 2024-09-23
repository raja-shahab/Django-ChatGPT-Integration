import os
import openai
from django.http import JsonResponse
from django.shortcuts import render
from openai import OpenAIError
from chatgpt_implementation import settings

openai.api_key = settings.OPENAI_API_KEY

def get_completion(prompt):
    try:
        print(f"Received prompt: {prompt}")
        query = openai.Completion.create(
            engine="gpt-4",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        response = query.choices[0].text.strip()
        print(f"Response: {response}")
        return response
    except OpenAIError as e:
        print(f"OpenAI API error: {e}")
        return "An error occurred while processing your request."
    except Exception as e:
        print(f"Unexpected error: {e}")
        return "An unexpected error occurred."


def query_view(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        if not prompt:
            return JsonResponse({'error': 'No prompt provided'}, status=400)

        response = get_completion(prompt)
        return JsonResponse({'response': response})

    return render(request, 'index.html')