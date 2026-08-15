#import "theme.typ": *

#head("肆", "個資保護", "AI DRAFTS · CLINICIANS DECIDE", 5)
#place(left + top, dx: 4in, dy: 0.55in)[
  #box(width: 4.35in, fill: blush, radius: 17pt, inset: (x: 10pt, y: 5pt))[
    #align(center)[
      #text(size: 14pt, weight: "bold", fill: wine)[個資法第六條｜依實際資料流逐案審查]
    ]
  ]
]
#place(left + top, dx: margin-x, dy: 1.7in)[
  #deck-grid(columns: (1fr, 1fr, 1fr, 1fr), gutter: gap,
    ..(("01", "即時轉錄", "完成轉錄後，原始音訊即時銷毀避免資料竊取。"),
       ("02", "本地端去識別", "AI 輔助去識別，僅保留必要的心理風險線索。"),
       ("03", "判斷約束", "限定僅從話題中判斷心理風險，避免不必要的個資推論。"),
       ("04", "輔助決策", "工具僅作為輔助，臨床判斷仍由專業人員負責，保證安全問題。"))
    .map(((num, title, body)) => panel([#text(size: 29pt, weight: "bold", fill: wine)[#num] #v(0.008in) #text(size: 18pt, weight: "bold")[#title] #v(0.0014in) #text(size: 13.5pt, fill: muted)[#body]], fill: white, height: 2.55in)))
]
#place(left + top, dx: margin-x, dy: 4.52in)[
  #deck-grid(columns: (1fr, 1fr), gutter: gap,
    panel([#text(size: 30pt, weight: "bold", fill: wine)[系統會做] #v(-0.12in) #bullet[整理已出現的心理風險線索] #v(0.08in) #bullet[明確指出原文判斷依據]], fill: blush, height: 2.08in),
    panel([#text(size: 30pt, weight: "bold")[系統不會做] #v(-0.12in) #bullet[自行診斷或判定自殺意圖] #v(0.08in) #bullet[將病患對話直接傳輸給外部 API]], fill: sand, height: 2.08in)
  )
]
#footer(5)
#pagebreak()
