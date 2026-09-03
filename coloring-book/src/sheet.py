"""Contact sheet of rendered preview pages, for reviewing several at once."""
import os
import sys
from PIL import Image

PV = os.environ.get("CB_PREVIEW",
                    "/tmp/claude-0/-home-user-portfolio/7b845276-1413-51e0-90b5-d4e4d121fac0/scratchpad/preview")
nums = [int(a) for a in sys.argv[1:]]
w = 470 if len(nums) <= 2 else 330
ims = []
for i in nums:
    im = Image.open(os.path.join(PV, "page-%02d.png" % i)).convert("RGB")
    im = im.resize((w, int(w * im.height / im.width)))
    ims.append(im)
H = max(i.height for i in ims)
out = Image.new("RGB", (sum(i.width + 8 for i in ims), H), "white")
x = 0
for im in ims:
    out.paste(im, (x, 0))
    x += im.width + 8
out.save(os.path.join(PV, "sheet.png"))
print(os.path.join(PV, "sheet.png"))
