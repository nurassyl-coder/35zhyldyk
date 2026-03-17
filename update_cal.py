import re

filepath = "/Users/nurasylmuhambetaly/Desktop/35 жылдық/30 жылдық copy.html"
with open(filepath, "r", encoding="utf-8") as f:
    html = f.read()

# Replace texts for days 2-31 to become 1-30
for i in range(2, 32):
    pattern = r"(<div class='tn-atom' field='tn_text_\d+'>)\s*" + str(i) + r"\s*(</div>)"
    # count matches first to be sure
    count = len(re.findall(pattern, html))
    if count == 1:
        # replace
        html = re.sub(pattern, r"\g<1>" + str(i-1) + r"\2", html)
    elif count > 1:
        print(f"Warning: multiple blocks found for day {i}")
    else:
        print(f"Warning: no blocks found for day {i}")

# Box for element 1 (which turns into 31)
box_1_id = '1746967798962'
pattern_1 = r"(<div class='tn-atom' field='tn_text_" + box_1_id + r"'>)\s*1\s*(</div>)"
if re.search(pattern_1, html):
    html = re.sub(pattern_1, r"\g<1>31\2", html)
else:
    print("Warning: box 1 not found")

# Update box 1 mobile inline attributes
html = re.sub(r"(data-elem-id='" + box_1_id + r"'.*?data-field-top-res-320-value=[\"'])463([\"'])", r"\g<1>573\2", html, flags=re.DOTALL)
html = re.sub(r"(data-elem-id='" + box_1_id + r"'.*?data-field-left-res-320-value=[\"'])153([\"'])", r"\g<1>255\2", html, flags=re.DOTALL)

# Update box 1 mobile CSS
def repl_css(m):
    return m.group(1) + "573px" + m.group(3) + "255px" + m.group(5)

css_pattern = r"(#rec1037968211 \.tn-elem\[data-elem-id=\"" + box_1_id + r"\"\].*?top:\s*)463px(.*?(?:left|margin-left):\s*calc\([^+\-]+\s*[\+\-]\s*\d+px\s*\+\s*)153px(.*?\})"
html = re.sub(css_pattern, repl_css, html, flags=re.DOTALL)

# We also should update desktop CSS and desktop inline to match Row 5 (top 242px) and Col 7 (left 359px).
# Wait, for desktop, week 1 left is 359px for Sunday? Yes, earlier 4 had left 359px.
# But what about top? 242px ? Yes, 26 had top 242px.
# Box 1 default desktop inline top: 401px. Let's change it to 242px.
html = re.sub(r"(data-elem-id='" + box_1_id + r"'.*?data-field-top-value=[\"'])401([\"'])", r"\g<1>242\2", html, flags=re.DOTALL)
html = re.sub(r"(#rec1037968211 \.tn-elem\[data-elem-id=\"" + box_1_id + r"\"\][^{]*{[^}]*?top:\s*)401px(.*?\})", r"\g<1>242px\2", html, flags=re.DOTALL)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(html)
print("Updated successfully!")
