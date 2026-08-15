#import "theme.typ": *

#head("壹", "現況分析", "THE SIGNALS ARE ALREADY IN THE CONVERSATION", 2)
#place(left + top, dx: margin-x, dy: content-y)[
  #deck-grid(columns: (1fr, 1fr, 1fr), gutter: gap,
    ..(("1", "低報風險", "防衛、污名或缺乏信任，讓真正的困擾不一定出現在量表上。"),
       ("2", "時間有限", "醫療人員同時要建立關係、理解主訴，也要辨識心理風險。"),
       ("3", "線索分散", "失眠、易怒、自我否定常藏在自然敘述裡，容易被匆忙略過。"))
    .map(((num, title, body)) => panel([
      #align(center)[
        #circle(radius: 15pt, fill: ink)[#align(center + horizon)[#text(fill: white, weight: "bold")[#num]]]
        #v(0.45in)
        #text(size: 21pt, weight: "bold")[#title]
        #v(0.2in)
        #text(size: 14.5pt, fill: muted)[#body]
      ]
    ], fill: white, height: 4.95in)))
]
#place(bottom + left, dx: margin-x, dy: -0.62in)[#text(size: 18pt, weight: "bold", fill: wine)[問題不是患者沒有說，而是重要訊號沒有被整理出來。]]
#footer(2)
#pagebreak()
