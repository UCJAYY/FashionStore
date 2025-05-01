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

from django.db.models import Case, When, Value, IntegerField, Sum, Q
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json, re
from together import Together     # assuming Together SDK import
                                   # pip install together

def itemsdisplay_view(request):
    # ------------------------------------------------------------------
    # 1.  Base queryset
    # ------------------------------------------------------------------
    items = FashionItem.objects.all()

    # ------------------------------------------------------------------
    # 2.  Parse prompt with a stricter, gender-aware instruction
    # ------------------------------------------------------------------
    ai_prompt   = request.GET.get("ai_prompt", "").strip()
    raw_text    = ""
    ai_filters  = {}

    if ai_prompt:
        system_instruction = (
            "You are a fashion-filter extractor.\n"
            "Objective:\n"
            "  • Read the shopper’s sentence.\n"
            "  • Return ONLY valid JSON with a flat object.\n"
            "  • Allowed keys (all lowercase): ageRange, profession, gender, "
            "size, brand, budget, bodyType, occasion.\n"
            "  • If the text clearly points to a gender, the JSON MUST include "
            "the gender key with value \"male\" or \"female\". Never guess; "
            "omit the key if uncertain.\n"
            "  • Values must be plain strings, no nested objects.\n"
            "  • Output nothing except the JSON object.\n"
            "Example:\n"
            "User: ‘Need a black tuxedo for my best friend’s summer wedding, "
            "budget about 150 dollars.’\n"
            "Assistant: "
            "{\"gender\":\"male\",\"occasion\":\"wedding\",\"budget\":\"100-200\"}"
        )

        client = Together(api_key="YOUR_TOGETHER_API_KEY")
        resp   = client.chat.completions.create(
                    model="meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user",   "content": ai_prompt}
                    ],
                    stream=True, temperature=0.6, top_p=0.8
                )

        for chunk in resp:
            if chunk.choices:
                raw_text += chunk.choices[0].delta.content or ""

        try:
            ai_filters = json.loads(raw_text) if isinstance(json.loads(raw_text), dict) else {}
        except json.JSONDecodeError:
            ai_filters = {}

        # keywords override – acts as a safety net
        if re.search(r"\bdress\b", ai_prompt, re.I):
            ai_filters["gender"] = "female"
        if re.search(r"\bmen['’]?s?\s+wedding\s+suit\b", ai_prompt, re.I):
            ai_filters["gender"] = "male"

    # ------------------------------------------------------------------
    # 3.  Build a scoring query (gender first, score the rest)
    # ------------------------------------------------------------------
    def apply_scored_query(qs, filters):
        """
        Enforce gender (if present), then score matches for the remaining keys.
        The item with the highest score appears first.
        """
        gender_val = filters.get("gender")
        if gender_val:
            qs = qs.filter(gender__iexact=gender_val)
        else:
            # No gender in prompt ⇒ return nothing; requirement says gender must be correct.
            return qs.none()

        conds = []

        mapper = {
            "ageRange":   ("age_range__iexact", None),
            "profession": ("profession__iexact", None),
            "size":       ("size__iexact", None),
            "brand":      ("brand__iexact", None),
            "bodyType":   ("body_type__iexact", None),
            "occasion":   ("occasion__iexact", None),
        }

        # simple exact / icontains comparisons
        for key, (lookup, _) in mapper.items():
            val = filters.get(key)
            if val:
                conds.append(When(**{lookup: val}, then=Value(1)))

        # budget ranges
        budget = filters.get("budget")
        if budget:
            rng_map = {
                ("$0 - $50", "0-50", "0_50"):       Q(price__range=(0, 50)),
                ("$50 - $100", "50-100", "50_100"): Q(price__range=(50, 100)),
                ("$100 - $200", "100-200", "100_200"): Q(price__range=(100, 200)),
                ("$200+", "200+", "200_plus"):       Q(price__gte=200),
            }
            for keys, q in rng_map.items():
                if budget in keys:
                    conds.append(When(q, then=Value(1)))
                    break

        scored_qs = (
            qs.annotate(
                match_count=Sum(
                    Case(*conds, default=Value(0), output_field=IntegerField())
                )
            )
            .order_by("-match_count", "id")
        )
        return scored_qs

    # AI filters available
    if ai_filters:
        items = apply_scored_query(items, ai_filters)
    else:
        # ------------------------------------------------------------------
        # 4.  Manual GET parameters fall-back (same logic, OR for range keys)
        # ------------------------------------------------------------------
        get_filters = {
            "gender":     request.GET.get("gender"),
            "ageRange":   request.GET.get("ageRange"),
            "profession": request.GET.get("profession"),
            "size":       request.GET.get("size"),
            "brand":      request.GET.get("brand"),
            "budget":     request.GET.get("budget"),
            "bodyType":   request.GET.get("bodyType"),
            "occasion":   request.GET.get("occasion"),
        }
        # keep empty strings out
        get_filters = {k: v for k, v in get_filters.items() if v}

        if get_filters:
            items = apply_scored_query(items, get_filters)
        else:
            # no usable filters ⇒ show none; can be changed to `.all()` if preferred
            items = items.none()

    return render(
        request,
        "itemsdisplay.html",
        {
            "items":        items,
            "ai_prompt":    ai_prompt,
            "total_count":  items.count(),
        },
    )


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

from django.db.models import Case, When, Value, IntegerField, Sum, Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def my_recommendations(request):
    user = request.user          # instance of CustomUser

    # 1. Gender must match ‒ filter the base queryset first.
    qs = FashionItem.objects.all()
    if user.gender:                                      # if gender is set
        qs = qs.filter(gender=user.gender)               # drop every item with the wrong gender
    else:
        return render(request, "my_recommendations.html",
                      {"recommendations": qs.none()})    # nothing to show without a gender choice

    # 2. Build conditions for every *other* attribute (gender already enforced).
    conditions = []

    if user.age_range:
        conditions.append(When(age_range=user.age_range, then=Value(1)))

    if user.clothing_size:
        conditions.append(When(size=user.clothing_size, then=Value(1)))

    if user.body_type:
        conditions.append(When(body_type=user.body_type, then=Value(1)))

    if user.preferred_style:
        conditions.append(When(description__icontains=user.preferred_style, then=Value(1)))

    if user.budget:
        budget_map = {
            '0_50':  Q(price__range=(0, 50)),
            '50_100': Q(price__range=(50, 100)),
            '100_200': Q(price__range=(100, 200)),
            '200_plus': Q(price__gte=200),
        }
        budget_q = budget_map.get(user.budget)
        if budget_q:
            conditions.append(When(budget_q, then=Value(1)))

    if user.brand_preferences:
        conditions.append(When(brand=user.brand_preferences, then=Value(1)))

    # 3. Annotate with a score, keep items that match *at least one* extra filter,
    #    then rank by the number of matches (highest first).
    recommendations = (
        qs.annotate(
            match_count=Sum(
                Case(*conditions, default=Value(0), output_field=IntegerField())
            )
        )
        .filter(match_count__gte=1)          # gender + ≥1 more criterion  ⇒ ≥2 total matches
        .order_by("-match_count", "id")      # highest score first, stable tie-break with id
    )

    return render(request, "my_recommendations.html",
                  {"recommendations": recommendations})



