#import "theme.typ": *

#head("參", "安全架構", "AI DRAFTS · CLINICIANS DECIDE", 4)
#place(left + top, dx: margin-x, dy: content-y)[
  #deck-grid(columns: (1fr, 1fr, 1fr, 1fr), gutter: gap,
    ..(("01", "即時轉錄", "完成轉錄後，原始音訊即時銷毀。"),
       ("02", "本機去識別", "資料離開設備前，先移除可識別資訊。"),
       ("03", "證據約束", "沒有原話支持，就輸出資訊不足。"),
       ("04", "人工決策", "追問、評分與處置皆由專業人員完成。"))
    .map(((num, title, body)) => panel([#text(size: 29pt, weight: "bold", fill: wine)[#num] #v(0.18in) #text(size: 18pt, weight: "bold")[#title] #v(0.14in) #text(size: 13.5pt, fill: muted)[#body]], fill: white, height: 2.55in)))
]
#place(left + top, dx: margin-x, dy: 4.12in)[
  #deck-grid(columns: (1fr, 1fr), gutter: gap,
    panel([#text(size: 18pt, weight: "bold", fill: wine)[系統會做] #v(0.12in) #bullet[整理已出現的心理風險線索] #v(0.08in) #bullet[保留模型版本與人工修改紀錄]], fill: blush, height: 2.08in),
    panel([#text(size: 18pt, weight: "bold")[系統不會做] #v(0.12in) #bullet[自行診斷或判定自殺意圖] #v(0.08in) #bullet[用單一分數宣告安全或危險]], fill: sand, height: 2.08in)
  )
]
#footer(4)
#pagebreak()
