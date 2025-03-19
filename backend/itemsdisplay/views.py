from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import FashionItem
from .forms import FashionItemForm

# Create your views here.
# itemsdisplay/views.py
from django.shortcuts import render
from .models import FashionItem

# itemsdisplay/views.py
from django.shortcuts import render
from .models import FashionItem
import re
from django.shortcuts import render, redirect
from itemsdisplay.models import FashionItem
from together import Together

import re
import json
from django.db.models import Q
from django.shortcuts import render
from itemsdisplay.models import FashionItem
from together import Together

import re
import json
from django.db.models import Q
from django.shortcuts import render
from itemsdisplay.models import FashionItem
from together import Together

import re
import json
from django.db.models import Q
from django.shortcuts import render
from itemsdisplay.models import FashionItem
from together import Together

def itemsdisplay_view(request):
    items = FashionItem.objects.all()
    ai_prompt = request.GET.get("ai_prompt", "").strip()

    # For debugging or logging purposes, store raw AI response text.
    raw_ai_response = ""
    # Dictionary to store parsed filters.
    ai_filters = {}

    if ai_prompt:
        # 1) Instruct the LLM to return only valid JSON with these keys.
        system_instruction = (
            "You are an assistant that extracts relevant fashion filter data from user prompts. "
            "You must respond ONLY in valid JSON with any subset of these keys: "
            "'ageRange', 'profession', 'gender', 'size', 'brand', 'budget', 'bodyType', 'occasion'. "
            "Do NOT include additional commentary or text."
        )

        # 2) Call the Together AI API using your provided API key.
        client = Together(api_key="bdca72696af6269a18c32185d2fc63ddbe992ea1d25aaaedf7ee7b873525b5c4")
        response = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": ai_prompt}
            ],
            max_tokens=None,
            temperature=0.7,
            top_p=0.7,
            top_k=50,
            repetition_penalty=1,
            stop=["<|eot_id|>", "<|eom_id|>"],
            stream=True
        )

        # 3) Stream and concatenate the raw response.
        for token in response:
            if hasattr(token, 'choices') and token.choices:
                raw_ai_response += token.choices[0].delta.content

        # 4) Attempt to parse the JSON output from the model.
        try:
            ai_filters = json.loads(raw_ai_response)
            if not isinstance(ai_filters, dict):
                ai_filters = {}
        except json.JSONDecodeError:
            ai_filters = {}

        # 5) Override gender based on keywords in the prompt.
        if re.search(r"\bdress\b", ai_prompt, re.IGNORECASE):
            ai_filters["gender"] = "female"
        if re.search(r"\bmen['’]?s?\s+wedding\s+suit\b", ai_prompt, re.IGNORECASE):
            ai_filters["gender"] = "male"

    # 6) Apply filters based on AI output if available.
    if ai_filters:
        filter_q = Q()
        if "ageRange" in ai_filters and ai_filters["ageRange"]:
            filter_q |= Q(age_range__iexact=ai_filters["ageRange"])
        if "profession" in ai_filters and ai_filters["profession"]:
            filter_q |= Q(profession__iexact=ai_filters["profession"])
        if "gender" in ai_filters and ai_filters["gender"]:
            filter_q |= Q(gender__iexact=ai_filters["gender"])
        if "size" in ai_filters and ai_filters["size"]:
            filter_q |= Q(size__iexact=ai_filters["size"])
        if "brand" in ai_filters and ai_filters["brand"]:
            filter_q |= Q(brand__iexact=ai_filters["brand"])
        if "budget" in ai_filters and ai_filters["budget"]:
            budget_val = ai_filters["budget"]
            if budget_val in ["$0 - $50", "0-50", "0_50"]:
                filter_q |= Q(price__gte=0, price__lte=50)
            elif budget_val in ["$50 - $100", "50-100", "50_100"]:
                filter_q |= Q(price__gte=50, price__lte=100)
            elif budget_val in ["$100 - $200", "100-200", "100_200"]:
                filter_q |= Q(price__gte=100, price__lte=200)
            elif budget_val in ["$200+", "200+", "200_plus"]:
                filter_q |= Q(price__gte=200)
        if "bodyType" in ai_filters and ai_filters["bodyType"]:
            filter_q |= Q(body_type__iexact=ai_filters["bodyType"])
        if "occasion" in ai_filters and ai_filters["occasion"]:
            filter_q |= Q(occasion__iexact=ai_filters["occasion"])

        if filter_q:
            items = items.filter(filter_q)
    else:
        # 7) Otherwise, use manual filtering via GET parameters with OR logic.
        age_range = request.GET.get('ageRange')
        profession = request.GET.get('profession')
        size = request.GET.get('size')
        gender = request.GET.get('gender')
        brand = request.GET.get('brand')
        budget = request.GET.get('budget')
        body_type = request.GET.get('bodyType')
        occasion = request.GET.get('occasion')

        filter_q = Q()
        if age_range:
            filter_q |= Q(age_range=age_range)
        if profession:
            filter_q |= Q(profession=profession)
        if size:
            filter_q |= Q(size=size)
        if gender:
            filter_q |= Q(gender=gender)
        if brand:
            filter_q |= Q(brand=brand)
        if budget:
            if budget.strip() == "$200+":
                filter_q |= Q(price__gte=200)
            else:
                try:
                    parts = budget.split("-")
                    if len(parts) == 2:
                        lower = float(parts[0].replace("$", "").strip())
                        upper = float(parts[1].replace("$", "").strip())
                        filter_q |= Q(price__gte=lower, price__lte=upper)
                except:
                    pass
        if body_type:
            filter_q |= Q(body_type=body_type)
        if occasion:
            filter_q |= Q(occasion=occasion)

        if filter_q:
            items = items.filter(filter_q)

    context = {
        "items": items,
        "ai_prompt": ai_prompt,
        "total_count": items.count(),
    }
    return render(request, 'itemsdisplay.html', context)








def add_fashion_item(request):
    if request.method == 'POST':
        form = FashionItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('itemsdisplay')  # Redirect after successful save
    else:
        form = FashionItemForm()
    return render(request, 'fileupload.html', {'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from .models import FashionItem

def delete_item(request, item_id):
    item = get_object_or_404(FashionItem, id=item_id)
    if request.method == 'POST':
        item.delete()
        return redirect('itemsdisplay')
    return render(request, 'delete_item.html', {'item': item})



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import FashionItem

from django.contrib.auth.decorators import login_required
from django.db.models import IntegerField, Case, When, Value, Sum
from django.shortcuts import render
from itemsdisplay.models import FashionItem  # adjust the import as needed

from django.contrib.auth.decorators import login_required
from django.db.models import Case, When, Value, IntegerField, Sum
from django.shortcuts import render
from itemsdisplay.models import FashionItem  # adjust import if necessary

from django.contrib.auth.decorators import login_required
from django.db.models import Case, When, Value, IntegerField, Sum
from django.shortcuts import render
from itemsdisplay.models import FashionItem  # adjust the import as needed

@login_required
def my_recommendations(request):
    user = request.user  # Instance of CustomUser

    qs = FashionItem.objects.all()
    conditions = []

    # Each condition returns a 1 if the product matches the user's preference.
    if user.age_range:
        conditions.append(When(age_range=user.age_range, then=Value(1)))
    if user.gender:
        conditions.append(When(gender=user.gender, then=Value(1)))
    if user.clothing_size:
        conditions.append(When(size=user.clothing_size, then=Value(1)))
    if user.body_type:
        conditions.append(When(body_type=user.body_type, then=Value(1)))
    if user.preferred_style:
        # Assuming the product description contains style-related information.
        conditions.append(When(description__icontains=user.preferred_style, then=Value(1)))
    if user.budget:
        # Map the stored budget value to numeric ranges.
        if user.budget == '200_plus':
            conditions.append(When(price__gte=200, then=Value(1)))
        elif user.budget == '0_50':
            conditions.append(When(price__gte=0, price__lte=50, then=Value(1)))
        elif user.budget == '50_100':
            conditions.append(When(price__gte=50, price__lte=100, then=Value(1)))
        elif user.budget == '100_200':
            conditions.append(When(price__gte=100, price__lte=200, then=Value(1)))
    if user.brand_preferences:
        conditions.append(When(brand=user.brand_preferences, then=Value(1)))

    # Annotate each product with a match_count field and filter for at least 1 matching condition.
    recommendations = qs.annotate(
        match_count=Sum(Case(*conditions, default=Value(0), output_field=IntegerField()))
    ).filter(match_count__gte=1)

    context = {
        "recommendations": recommendations,
    }
    return render(request, "my_recommendations.html", context)


