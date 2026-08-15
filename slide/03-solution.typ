#import "theme.typ": *

#head("貳", "解決方案", "LISTEN · STRUCTURE · REVIEW", 3)
#place(left + top, dx: margin-x, dy: content-y)[
  #deck-grid(columns: (1fr, 0.34in, 1fr, 0.34in, 1fr), gutter: 0.1in,
    panel([#tag("01") #v(0.3in) #text(size: 22pt, weight: "bold")[傾聽自然對話] #v(0.18in) #text(size: 14.5pt, fill: muted)[不打斷原有醫病互動，即時將語音轉成逐字稿。]], fill: white, height: 4.45in),
    align(center + horizon)[#text(size: 30pt, fill: wine)[→]],
    panel([#tag("02") #v(0.3in) #text(size: 22pt, weight: "bold")[整理心理線索] #v(0.18in) #text(size: 14.5pt, fill: muted)[依 BSRS-5 面向整理分數草稿、原話、理由與信心。]], fill: blush, height: 4.45in),
    align(center + horizon)[#text(size: 30pt, fill: wine)[→]],
    panel([#tag("03") #v(0.3in) #text(size: 22pt, weight: "bold")[交由專業確認] #v(0.18in) #text(size: 14.5pt, fill: muted)[資訊不足就標示缺漏；由醫療人員追問、修改與確認。]], fill: white, height: 4.45in)
  )
]
#place(bottom + left, dx: margin-x, dy: -0.72in)[#box(width: content-w, fill: wine, radius: 5pt, inset: 13pt)[#align(center)[#text(size: 17pt, weight: "bold", fill: white)[用傾聽取代填表，讓每個建議都能回到患者原話。]]]]
#footer(3)
#pagebreak()
